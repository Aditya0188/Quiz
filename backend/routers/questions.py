import json
from typing import Optional
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.question import Question
from services.quiz_service import normalize_subject

router = APIRouter(tags=["questions"])

@router.get("/api/subjects")
def list_subjects(db: Session = Depends(get_db)):
    subjects = db.query(Question.subject).distinct().all()
    res = []
    for (subj,) in subjects:
        topics_count = db.query(func.count(func.distinct(Question.topic))).filter(Question.subject == subj).scalar()
        q_count = db.query(func.count(Question.id)).filter(Question.subject == subj).scalar()
        easy = db.query(func.count(Question.id)).filter(Question.subject == subj, Question.difficulty == "easy").scalar()
        medium = db.query(func.count(Question.id)).filter(Question.subject == subj, Question.difficulty == "medium").scalar()
        hard = db.query(func.count(Question.id)).filter(Question.subject == subj, Question.difficulty == "hard").scalar()
        
        res.append({
            "subject": subj,
            "topic_count": topics_count,
            "question_count": q_count,
            "difficulty_breakdown": {"easy": easy, "medium": medium, "hard": hard}
        })
    return res

@router.get("/api/subjects/{subject}/topics")
def list_topics(subject: str, db: Session = Depends(get_db)):
    norm_subj = normalize_subject(subject)
    topics = db.query(Question.topic).filter(Question.subject == norm_subj).distinct().all()
    res = []
    for (top,) in topics:
        q_count = db.query(func.count(Question.id)).filter(Question.subject == norm_subj, Question.topic == top).scalar()
        min_yr = db.query(func.min(Question.year)).filter(Question.subject == norm_subj, Question.topic == top).scalar()
        max_yr = db.query(func.max(Question.year)).filter(Question.subject == norm_subj, Question.topic == top).scalar()
        res.append({
            "topic": top,
            "question_count": q_count,
            "year_range": (min_yr, max_yr)
        })
    # Sort topics alphabetically
    res.sort(key=lambda x: x["topic"])
    return res

@router.get("/api/questions/stats")
def overall_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Question.id)).scalar()
    
    by_type = dict(db.query(Question.question_type, func.count(Question.id)).group_by(Question.question_type).all())
    by_diff = dict(db.query(Question.difficulty, func.count(Question.id)).group_by(Question.difficulty).all())
    by_subj = dict(db.query(Question.subject, func.count(Question.id)).group_by(Question.subject).all())
    
    min_yr = db.query(func.min(Question.year)).scalar()
    max_yr = db.query(func.max(Question.year)).scalar()
    
    return {
        "total_questions": total,
        "by_type": by_type,
        "by_difficulty": by_diff,
        "year_range": (min_yr, max_yr),
        "by_subject": by_subj
    }

# =========================================================================
# PAPER ANALYSIS ENDPOINTS (1991 - 2025 Comprehensive Analysis)
# =========================================================================

@router.get("/api/paper-analysis/overview")
def paper_analysis_overview(db: Session = Depends(get_db)):
    """Overall statistics across 35 years of GATE papers."""
    total_q = db.query(func.count(Question.id)).scalar()
    total_marks = db.query(func.sum(Question.marks)).scalar() or 0
    min_year = db.query(func.min(Question.year)).scalar() or 1991
    max_year = db.query(func.max(Question.year)).scalar() or 2025

    # Subject weightage breakdown
    subjects_data = []
    subject_groups = db.query(
        Question.subject,
        func.count(Question.id).label("q_count"),
        func.sum(Question.marks).label("total_m"),
        func.count(func.distinct(Question.topic)).label("topics_count")
    ).group_by(Question.subject).all()

    for s, qc, tm, tc in subject_groups:
        subjects_data.append({
            "subject": s,
            "question_count": qc,
            "total_marks": tm or 0,
            "topics_count": tc,
            "weightage_pct": round((tm / total_marks * 100) if total_marks else 0, 1)
        })

    subjects_data.sort(key=lambda x: x["total_marks"], reverse=True)

    return {
        "total_questions": total_q,
        "total_marks": total_marks,
        "year_range": [min_year, max_year],
        "subject_breakdown": subjects_data
    }

@router.get("/api/paper-analysis/years")
def paper_analysis_years(db: Session = Depends(get_db)):
    """List of all past years with high-level question and marks distribution."""
    years = db.query(Question.year).filter(Question.year != None).distinct().order_by(Question.year.desc()).all()
    results = []

    for (yr,) in years:
        qs = db.query(Question).filter(Question.year == yr).all()
        if not qs:
            continue

        total_marks = sum(q.marks for q in qs)
        one_mark = sum(1 for q in qs if q.marks == 1)
        two_mark = sum(1 for q in qs if q.marks == 2)

        type_counts = defaultdict(int)
        subj_counts = defaultdict(int)
        subj_marks = defaultdict(int)

        for q in qs:
            type_counts[q.question_type] += 1
            subj_counts[q.subject] += 1
            subj_marks[q.subject] += q.marks

        results.append({
            "year": yr,
            "total_questions": len(qs),
            "total_marks": total_marks,
            "one_mark_count": one_mark,
            "two_mark_count": two_mark,
            "question_types": dict(type_counts),
            "subject_question_counts": dict(subj_counts),
            "subject_marks": dict(subj_marks)
        })

    return results

@router.get("/api/paper-analysis/year/{year}")
def paper_analysis_by_year(year: int, db: Session = Depends(get_db)):
    """Detailed topic-level breakdown of a specific year's paper."""
    qs = db.query(Question).filter(Question.year == year).all()
    if not qs:
        raise HTTPException(status_code=404, detail=f"No questions found for year {year}")

    total_marks = sum(q.marks for q in qs)
    one_mark = sum(1 for q in qs if q.marks == 1)
    two_mark = sum(1 for q in qs if q.marks == 2)

    diff_counts = {"easy": 0, "medium": 0, "hard": 0}
    type_counts = {"MCQ": 0, "MSQ": 0, "NAT": 0}

    # Group by subject and then topic
    subject_map = defaultdict(lambda: {
        "question_count": 0,
        "total_marks": 0,
        "topics": defaultdict(lambda: {"question_count": 0, "marks": 0})
    })

    questions_list = []

    for q in qs:
        diff_counts[q.difficulty] = diff_counts.get(q.difficulty, 0) + 1
        type_counts[q.question_type] = type_counts.get(q.question_type, 0) + 1

        s_entry = subject_map[q.subject]
        s_entry["question_count"] += 1
        s_entry["total_marks"] += q.marks
        s_entry["topics"][q.topic]["question_count"] += 1
        s_entry["topics"][q.topic]["marks"] += q.marks

        questions_list.append({
            "id": q.id,
            "subject": q.subject,
            "topic": q.topic,
            "marks": q.marks,
            "question_type": q.question_type,
            "difficulty": q.difficulty,
            "question_text": q.question_text,
            "options": json.loads(q.options) if q.options else None,
            "year": q.year,
            "set_number": q.set_number
        })

    formatted_subjects = []
    for subj_name, data in subject_map.items():
        topic_list = []
        for t_name, t_data in data["topics"].items():
            topic_list.append({
                "topic": t_name,
                "question_count": t_data["question_count"],
                "marks": t_data["marks"]
            })
        topic_list.sort(key=lambda x: x["marks"], reverse=True)
        formatted_subjects.append({
            "subject": subj_name,
            "question_count": data["question_count"],
            "total_marks": data["total_marks"],
            "topics": topic_list
        })

    formatted_subjects.sort(key=lambda x: x["total_marks"], reverse=True)

    return {
        "year": year,
        "total_questions": len(qs),
        "total_marks": total_marks,
        "one_mark_count": one_mark,
        "two_mark_count": two_mark,
        "difficulty_breakdown": diff_counts,
        "question_types": type_counts,
        "subjects": formatted_subjects,
        "questions": questions_list
    }

@router.get("/api/paper-analysis/subject-trends")
def paper_analysis_subject_trends(subject: Optional[str] = None, db: Session = Depends(get_db)):
    """35-year topic frequency ranking and average weightage."""
    query = db.query(Question)
    if subject and subject.upper() not in ["ALL", "MIX"]:
        norm_subj = normalize_subject(subject)
        query = query.filter(Question.subject == norm_subj)

    all_q = query.all()
    if not all_q:
        return {"subject": subject, "topics": []}

    topic_stats = defaultdict(lambda: {
        "subject": "",
        "question_count": 0,
        "total_marks": 0,
        "years": set(),
        "types": defaultdict(int),
        "difficulties": defaultdict(int)
    })

    for q in all_q:
        ts = topic_stats[q.topic]
        ts["subject"] = q.subject
        ts["question_count"] += 1
        ts["total_marks"] += q.marks
        if q.year:
            ts["years"].add(q.year)
        ts["types"][q.question_type] += 1
        ts["difficulties"][q.difficulty] += 1

    results = []
    total_exam_years = 35

    for topic_name, data in topic_stats.items():
        results.append({
            "topic": topic_name,
            "subject": data["subject"],
            "question_count": data["question_count"],
            "total_marks": data["total_marks"],
            "years_appeared_count": len(data["years"]),
            "appearance_frequency_pct": round((len(data["years"]) / total_exam_years) * 100, 1),
            "years": sorted(list(data["years"])),
            "question_types": dict(data["types"]),
            "difficulties": dict(data["difficulties"])
        })

    results.sort(key=lambda x: x["total_marks"], reverse=True)

    return {
        "subject": subject or "All Subjects",
        "total_topics": len(results),
        "topics": results
    }
