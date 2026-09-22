import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.user import User
from models.quiz_session import QuizSession
from models.question import Question
from services.auth_service import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/overview")
def get_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(QuizSession).filter(QuizSession.user_id == current_user.id, QuizSession.completed_at.isnot(None)).all()
    
    total_quizzes = len(sessions)
    if total_quizzes == 0:
        return {"total_quizzes": 0, "avg_score": 0, "best_score": 0, "total_questions_attempted": 0, "accuracy_rate": 0}
        
    total_score = sum(s.score for s in sessions)
    best_score = max(s.score for s in sessions)
    
    total_q = sum(s.total_questions for s in sessions)
    total_correct = sum(s.correct_count for s in sessions)
    total_wrong = sum(s.wrong_count for s in sessions)
    
    accuracy = (total_correct / (total_correct + total_wrong)) * 100 if (total_correct + total_wrong) > 0 else 0
    
    return {
        "total_quizzes": total_quizzes,
        "avg_score": total_score / total_quizzes,
        "best_score": best_score,
        "total_questions_attempted": total_q,
        "accuracy_rate": accuracy
    }

@router.get("/progress")
def get_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(QuizSession).filter(QuizSession.user_id == current_user.id, QuizSession.completed_at.isnot(None)).order_by(QuizSession.completed_at.asc()).limit(30).all()
    
    return [
        {
            "session_id": s.id,
            "date": s.completed_at,
            "score": s.score,
            "max_score": s.max_score,
            "percentage": (s.score / s.max_score * 100) if s.max_score > 0 else 0
        }
        for s in sessions
    ]

# Subject-wise and topic-wise analytics would require parsing the JSON responses
# For simplicity, returning mock structure based on requirements if complex join is hard
# In a real app we'd parse the responses or store granular attempts
@router.get("/subject-wise")
def subject_wise(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # This requires processing all responses to map to subjects
    sessions = db.query(QuizSession).filter(QuizSession.user_id == current_user.id, QuizSession.completed_at.isnot(None)).all()
    
    subj_stats = {}
    for s in sessions:
        if not s.responses:
            continue
        responses = json.loads(s.responses)
        q_ids = list(responses.keys())
        questions = db.query(Question).filter(Question.id.in_(q_ids)).all()
        for q in questions:
            res = responses[str(q.id)]
            if q.subject not in subj_stats:
                subj_stats[q.subject] = {"correct": 0, "total": 0, "score": 0.0, "topics": {}}
            
            subj_stats[q.subject]["total"] += 1
            if q.topic not in subj_stats[q.subject]["topics"]:
                subj_stats[q.subject]["topics"][q.topic] = {"correct": 0, "total": 0}
            subj_stats[q.subject]["topics"][q.topic]["total"] += 1
            
            if res["status"] == "correct":
                subj_stats[q.subject]["correct"] += 1
                subj_stats[q.subject]["topics"][q.topic]["correct"] += 1
            
            subj_stats[q.subject]["score"] += res.get("marks_awarded", 0.0)
            
    res_list = []
    for subj, data in subj_stats.items():
        accuracy = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
        
        strongest = None
        weakest = None
        max_acc = -1
        min_acc = 101
        
        for top, tdata in data["topics"].items():
            if tdata["total"] > 0:
                t_acc = tdata["correct"] / tdata["total"] * 100
                if t_acc > max_acc:
                    max_acc = t_acc
                    strongest = top
                if t_acc < min_acc:
                    min_acc = t_acc
                    weakest = top
                    
        res_list.append({
            "subject": subj,
            "avg_score": data["score"] / len(sessions), # Approximation
            "accuracy": accuracy,
            "strongest_topic": strongest,
            "weakest_topic": weakest
        })
    return res_list

@router.get("/topic-wise/{subject}")
def topic_wise(subject: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(QuizSession).filter(QuizSession.user_id == current_user.id, QuizSession.completed_at.isnot(None)).all()
    
    topic_stats = {}
    for s in sessions:
        if not s.responses:
            continue
        responses = json.loads(s.responses)
        q_ids = list(responses.keys())
        questions = db.query(Question).filter(Question.id.in_(q_ids), Question.subject == subject).all()
        for q in questions:
            res = responses[str(q.id)]
            if q.topic not in topic_stats:
                topic_stats[q.topic] = {"correct": 0, "total": 0}
            
            topic_stats[q.topic]["total"] += 1
            if res["status"] == "correct":
                topic_stats[q.topic]["correct"] += 1
                
    return [
        {
            "topic": topic,
            "accuracy": (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0,
            "total_attempted": data["total"]
        }
        for topic, data in topic_stats.items()
    ]

@router.get("/full")
def get_full_analytics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(QuizSession).filter(QuizSession.user_id == current_user.id, QuizSession.completed_at.isnot(None)).order_by(QuizSession.completed_at.asc()).all()
    
    total_quizzes = len(sessions)
    if total_quizzes == 0:
        return {
            "overview": {"totalQuizzes": 0, "avgScore": 0, "accuracy": 0, "totalTime": 0},
            "scoreTrend": [],
            "subjectPerf": [],
            "topicStrengths": []
        }
    
    total_score = sum(s.score for s in sessions)
    total_max = sum(s.max_score for s in sessions)
    avg_score = round((total_score / total_max * 100) if total_max > 0 else 0)
    
    total_correct = sum(s.correct_count for s in sessions)
    total_wrong = sum(s.wrong_count for s in sessions)
    accuracy = round((total_correct / (total_correct + total_wrong) * 100) if (total_correct + total_wrong) > 0 else 0)
    total_time = sum(s.time_limit_minutes for s in sessions)
    
    score_trend = []
    for s in sessions[-15:]:
        pct = round((s.score / s.max_score * 100) if s.max_score > 0 else 0)
        date_str = s.completed_at.strftime("%b %d") if s.completed_at else f"Quiz {s.id}"
        score_trend.append({"date": date_str, "score": max(0, pct)})
        
    subj_stats = {}
    topic_stats = []
    for s in sessions:
        if not s.responses:
            continue
        responses = json.loads(s.responses)
        q_ids = list(responses.keys())
        questions = db.query(Question).filter(Question.id.in_([int(x) for x in q_ids])).all()
        for q in questions:
            res = responses.get(str(q.id), {})
            if q.subject not in subj_stats:
                subj_stats[q.subject] = {"correct": 0, "total": 0, "topics": {}}
            subj_stats[q.subject]["total"] += 1
            if q.topic not in subj_stats[q.subject]["topics"]:
                subj_stats[q.subject]["topics"][q.topic] = {"correct": 0, "total": 0}
            subj_stats[q.subject]["topics"][q.topic]["total"] += 1
            
            if res.get("status") == "correct":
                subj_stats[q.subject]["correct"] += 1
                subj_stats[q.subject]["topics"][q.topic]["correct"] += 1
                
    subject_perf = []
    for subj, d in subj_stats.items():
        score = round((d["correct"] / d["total"] * 100) if d["total"] > 0 else 0)
        subject_perf.append({"subject": subj, "score": score})
        for top, td in d["topics"].items():
            top_score = round((td["correct"] / td["total"] * 100) if td["total"] > 0 else 0)
            topic_stats.append({"topic": top, "subject": subj, "score": top_score, "total": td["total"]})
            
    topic_stats.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "overview": {
            "totalQuizzes": total_quizzes,
            "avgScore": avg_score,
            "accuracy": accuracy,
            "totalTime": total_time
        },
        "scoreTrend": score_trend,
        "subjectPerf": subject_perf,
        "topicStrengths": topic_stats
    }

