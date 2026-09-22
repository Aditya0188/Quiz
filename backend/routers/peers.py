import json
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database import get_db
from models.user import User
from models.quiz_session import QuizSession
from models.question import Question
from services.auth_service import get_current_user

router = APIRouter(prefix="/api/peers", tags=["peers"])


def _compute_user_stats(db: Session, user_id: int):
    sessions = (
        db.query(QuizSession)
        .filter(QuizSession.user_id == user_id, QuizSession.completed_at.isnot(None))
        .all()
    )

    total_quizzes = len(sessions)
    if total_quizzes == 0:
        return {
            "total_quizzes": 0,
            "avg_score": 0.0,
            "accuracy_rate": 0.0,
            "total_questions_attempted": 0,
            "best_score": 0.0,
            "last_active": None,
            "subject_stats": {}
        }

    total_score = sum(s.score for s in sessions)
    total_max = sum(s.max_score for s in sessions)
    avg_score_pct = round((total_score / total_max * 100) if total_max > 0 else 0, 1)
    best_score = round(max((s.score for s in sessions), default=0.0), 1)
    total_q = sum(s.total_questions for s in sessions)
    total_correct = sum(s.correct_count for s in sessions)
    total_wrong = sum(s.wrong_count for s in sessions)
    accuracy = round(
        (total_correct / (total_correct + total_wrong) * 100)
        if (total_correct + total_wrong) > 0
        else 0,
        1
    )
    last_active = max(s.completed_at for s in sessions)

    # Subject breakdown
    subj_map = {}
    for s in sessions:
        if not s.responses:
            continue
        try:
            resp_dict = json.loads(s.responses)
        except Exception:
            continue

        q_ids = [int(qid) for qid in resp_dict.keys() if qid.isdigit()]
        if not q_ids:
            continue

        questions = db.query(Question).filter(Question.id.in_(q_ids)).all()
        for q in questions:
            s_name = q.subject
            if s_name not in subj_map:
                subj_map[s_name] = {"correct": 0, "total": 0}
            subj_map[s_name]["total"] += 1
            item = resp_dict.get(str(q.id), {})
            if item.get("status") == "correct":
                subj_map[s_name]["correct"] += 1

    subject_accuracy = {}
    for subj, val in subj_map.items():
        acc = round((val["correct"] / val["total"] * 100) if val["total"] > 0 else 0, 1)
        subject_accuracy[subj] = {
            "accuracy": acc,
            "total_attempted": val["total"]
        }

    return {
        "total_quizzes": total_quizzes,
        "avg_score": avg_score_pct,
        "accuracy_rate": accuracy,
        "total_questions_attempted": total_q,
        "best_score": best_score,
        "last_active": last_active.isoformat() if last_active else None,
        "subject_stats": subject_accuracy
    }


@router.get("/list")
def list_peers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all registered students with summary metrics."""
    users = db.query(User).all()
    results = []
    for u in users:
        stats = _compute_user_stats(db, u.id)
        results.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "is_self": (u.id == current_user.id),
            "total_quizzes": stats["total_quizzes"],
            "avg_score": stats["avg_score"],
            "accuracy_rate": stats["accuracy_rate"],
            "best_score": stats["best_score"],
            "last_active": stats["last_active"]
        })
    # Sort by total quizzes or activity
    results.sort(key=lambda x: (x["total_quizzes"], x["accuracy_rate"]), reverse=True)
    return results


@router.get("/compare")
def compare_peer(
    buddy_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Side-by-side comparison between the current user and their study buddy."""
    # Find buddy
    if buddy_id and buddy_id != current_user.id:
        buddy = db.query(User).filter(User.id == buddy_id).first()
    else:
        # Pick the most active other user
        buddy = (
            db.query(User)
            .filter(User.id != current_user.id)
            .first()
        )

    user_stats = _compute_user_stats(db, current_user.id)
    buddy_stats = _compute_user_stats(db, buddy.id) if buddy else None

    # All standard subjects
    all_subjects = [
        "Operating Systems",
        "Computer Organization & Architecture",
        "Programming & Data Structures",
        "Algorithms",
        "Theory of Computation",
        "Compiler Design",
        "Databases",
        "Computer Networks",
        "Digital Logic",
        "Engineering Mathematics",
        "General Aptitude"
    ]

    subject_comparison = []
    u_subj = user_stats["subject_stats"]
    b_subj = buddy_stats["subject_stats"] if buddy_stats else {}

    for subj in all_subjects:
        u_val = u_subj.get(subj, {"accuracy": 0, "total_attempted": 0})
        b_val = b_subj.get(subj, {"accuracy": 0, "total_attempted": 0})
        subject_comparison.append({
            "subject": subj,
            "user_accuracy": u_val["accuracy"],
            "user_attempted": u_val["total_attempted"],
            "buddy_accuracy": b_val["accuracy"],
            "buddy_attempted": b_val["total_attempted"]
        })

    return {
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "stats": user_stats
        },
        "buddy": {
            "id": buddy.id,
            "name": buddy.name,
            "email": buddy.email,
            "stats": buddy_stats
        } if buddy else None,
        "subject_comparison": subject_comparison
    }


@router.get("/feed")
def get_shared_activity_feed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the recent activity stream of completed quizzes across peers."""
    sessions = (
        db.query(QuizSession, User)
        .join(User, QuizSession.user_id == User.id)
        .filter(QuizSession.completed_at.isnot(None))
        .order_by(desc(QuizSession.completed_at))
        .limit(30)
        .all()
    )

    feed = []
    for s, u in sessions:
        title = "GATE CS Practice Quiz"
        try:
            cfg = json.loads(s.config) if s.config else {}
            if cfg.get("subjects") and len(cfg["subjects"]) == 1:
                title = f"{cfg['subjects'][0]} Quiz"
            elif cfg.get("year_range") and cfg["year_range"][0] == cfg["year_range"][1]:
                title = f"GATE {cfg['year_range'][0]} Full Paper"
        except Exception:
            pass

        pct = round((s.score / s.max_score * 100) if s.max_score > 0 else 0, 1)
        accuracy = round(
            (s.correct_count / (s.correct_count + s.wrong_count) * 100)
            if (s.correct_count + s.wrong_count) > 0
            else 0,
            1
        )

        feed.append({
            "session_id": s.id,
            "user_id": u.id,
            "user_name": u.name,
            "is_self": (u.id == current_user.id),
            "quiz_title": title,
            "score": s.score,
            "max_score": s.max_score,
            "percentage": pct,
            "correct_count": s.correct_count,
            "wrong_count": s.wrong_count,
            "unanswered_count": s.unanswered_count,
            "total_questions": s.total_questions,
            "accuracy": accuracy,
            "completed_at": s.completed_at.isoformat() if s.completed_at else None
        })

    return feed


@router.get("/attempt/{session_id}")
def get_peer_attempt_details(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Inspect a peer's completed quiz attempt to learn from questions and solutions."""
    session = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Quiz session not found")

    user = db.query(User).filter(User.id == session.user_id).first()
    user_name = user.name if user else "Aspirant"

    responses = {}
    if session.responses:
        try:
            responses = json.loads(session.responses)
        except Exception:
            responses = {}

    questions_order = []
    if session.questions_order:
        try:
            questions_order = json.loads(session.questions_order)
        except Exception:
            pass

    if not questions_order and responses:
        questions_order = [int(k) for k in responses.keys() if str(k).isdigit()]

    questions = db.query(Question).filter(Question.id.in_(questions_order)).all()
    q_map = {q.id: q for q in questions}

    detailed_questions = []
    for qid in questions_order:
        q = q_map.get(qid)
        if not q:
            continue
        res = responses.get(str(qid), {})
        student_ans = res.get("answer")
        status = res.get("status", "unanswered")
        marks_awarded = res.get("marks_awarded", 0.0)

        options = None
        if q.options:
            try:
                options = json.loads(q.options)
            except Exception:
                options = q.options

        detailed_questions.append({
            "id": q.id,
            "question_text": q.question_text,
            "subject": q.subject,
            "topic": q.topic,
            "year": q.year,
            "question_type": q.question_type,
            "marks": q.marks,
            "options": options,
            "correct_answer": q.correct_answer,
            "student_answer": student_ans,
            "status": status,
            "marks_awarded": marks_awarded,
            "explanation": q.explanation
        })

    pct = round((session.score / session.max_score * 100) if session.max_score > 0 else 0, 1)

    return {
        "session_id": session.id,
        "user_id": session.user_id,
        "user_name": user_name,
        "is_self": (session.user_id == current_user.id),
        "score": session.score,
        "max_score": session.max_score,
        "percentage": pct,
        "correct_count": session.correct_count,
        "wrong_count": session.wrong_count,
        "unanswered_count": session.unanswered_count,
        "total_questions": session.total_questions,
        "completed_at": session.completed_at.isoformat() if session.completed_at else None,
        "questions": detailed_questions
    }


@router.delete("/user/{user_id}")
def delete_peer_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a test or unwanted peer account and their quiz sessions."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own active account from here.")

    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    target_name = target.name
    # Delete associated quiz sessions
    db.query(QuizSession).filter(QuizSession.user_id == user_id).delete()
    db.delete(target)
    db.commit()

    return {"message": f"User '{target_name}' and all associated test data deleted successfully."}
