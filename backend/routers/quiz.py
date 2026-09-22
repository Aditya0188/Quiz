import json
from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import User
from models.quiz_session import QuizSession
from models.question import Question
from services.auth_service import get_current_user
from services.quiz_service import generate_quiz, evaluate_quiz

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

class QuizConfig(BaseModel):
    subjects: List[str]
    topics: Optional[List[str]] = []
    difficulty: str = "mixed"
    num_questions: int = 10
    time_limit: int = 30
    question_types: List[str] = ["MCQ", "MSQ", "NAT"]
    year_range: Optional[List[int]] = [1991, 2026]
    include_ai: bool = False
    source: Optional[str] = "all"

class SubmitAnswers(BaseModel):
    responses: Dict[str, dict]

@router.post("/start")
def start_quiz(config: QuizConfig, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cfg = config.dict()
    if config.year_range:
        cfg["year_range"] = tuple(config.year_range)
    questions = generate_quiz(db, current_user.id, cfg)
    if not questions:
        raise HTTPException(status_code=400, detail="No questions found matching your criteria. Try broadening your filters.")
        
    q_ids = [str(q.id) for q in questions]
    
    session = QuizSession(
        user_id=current_user.id,
        config=json.dumps(config.dict()),
        total_questions=len(questions),
        time_limit_minutes=config.time_limit,
        questions_order=json.dumps(q_ids)
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    ret_questions = []
    for q in questions:
        ret_questions.append({
            "id": q.id,
            "subject": q.subject,
            "topic": q.topic,
            "question_type": q.question_type,
            "marks": q.marks,
            "question_text": q.question_text,
            "options": json.loads(q.options) if q.options else None,
            "difficulty": q.difficulty,
            "year": q.year,
            "set_number": q.set_number
        })
        
    return {"session_id": session.id, "questions": ret_questions, "time_limit_minutes": session.time_limit_minutes}

# IMPORTANT: /history MUST be before /{session_id} to avoid route conflict
@router.get("/history")
def get_history(page: int = 1, per_page: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    offset = (page - 1) * per_page
    total = db.query(QuizSession).filter(QuizSession.user_id == current_user.id).count()
    sessions = db.query(QuizSession).filter(QuizSession.user_id == current_user.id).order_by(QuizSession.started_at.desc()).offset(offset).limit(per_page).all()
    
    res = []
    for s in sessions:
        config_data = json.loads(s.config) if s.config else {}
        res.append({
            "id": s.id,
            "started_at": s.started_at.isoformat() if s.started_at else None,
            "completed_at": s.completed_at.isoformat() if s.completed_at else None,
            "score": s.score,
            "max_score": s.max_score,
            "total_questions": s.total_questions,
            "correct_count": s.correct_count,
            "wrong_count": s.wrong_count,
            "subjects": config_data.get("subjects", []),
            "time_limit_minutes": s.time_limit_minutes
        })
    return {"history": res, "total": total, "page": page, "per_page": per_page}

@router.post("/{session_id}/submit")
def submit_quiz(session_id: int, payload: SubmitAnswers, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(QuizSession).filter(QuizSession.id == session_id, QuizSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Quiz session not found")
        
    if session.completed_at:
        raise HTTPException(status_code=400, detail="Quiz already submitted")
        
    evaluated = evaluate_quiz(db, session_id, payload.responses)
    
    return {
        "session_id": evaluated.id,
        "score": evaluated.score,
        "max_score": evaluated.max_score,
        "correct_count": evaluated.correct_count,
        "wrong_count": evaluated.wrong_count,
        "unanswered_count": evaluated.unanswered_count,
        "completed_at": evaluated.completed_at.isoformat() if evaluated.completed_at else None
    }

@router.get("/{session_id}")
def get_quiz_details(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(QuizSession).filter(QuizSession.id == session_id, QuizSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Quiz session not found")
        
    q_ids = json.loads(session.questions_order)
    questions = db.query(Question).filter(Question.id.in_([int(x) for x in q_ids])).all()
    q_dict = {str(q.id): q for q in questions}
    
    responses = json.loads(session.responses) if session.responses else {}
    
    ret_questions = []
    for qid in q_ids:
        q = q_dict.get(qid)
        if q:
            q_data = {
                "id": q.id,
                "subject": q.subject,
                "topic": q.topic,
                "question_type": q.question_type,
                "marks": q.marks,
                "question_text": q.question_text,
                "options": json.loads(q.options) if q.options else None,
                "difficulty": q.difficulty,
                "year": q.year,
                "set_number": q.set_number
            }
            if session.completed_at:
                q_data["correct_answer"] = q.correct_answer
                q_data["explanation"] = q.explanation
                q_data["user_response"] = responses.get(str(q.id), {})
            ret_questions.append(q_data)
            
    return {
        "session": {
            "id": session.id,
            "started_at": session.started_at.isoformat() if session.started_at else None,
            "completed_at": session.completed_at.isoformat() if session.completed_at else None,
            "score": session.score,
            "max_score": session.max_score,
            "correct_count": session.correct_count,
            "wrong_count": session.wrong_count,
            "unanswered_count": session.unanswered_count,
            "total_questions": session.total_questions,
            "time_limit_minutes": session.time_limit_minutes,
            "config": json.loads(session.config) if session.config else {}
        },
        "questions": ret_questions
    }
