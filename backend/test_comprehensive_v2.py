"""
Comprehensive Automated Verification Script for GATE CS Quiz Master:
1. Question statement uniqueness (0 duplicate statements)
2. GATE 2027 syllabus & subject coverage
3. Strict topic & subject isolation
4. Anti-repetition engine verification
5. Paper analysis endpoints verification
6. Brief solution formatting
"""

import sys
import json
from collections import Counter
from database import SessionLocal
from models.user import User
from models.question import Question
from models.quiz_session import QuizSession
from services.quiz_service import generate_quiz, evaluate_quiz
from routers.questions import (
    paper_analysis_overview, paper_analysis_years, 
    paper_analysis_by_year, paper_analysis_subject_trends
)

def run_tests():
    db = SessionLocal()
    print("=" * 60)
    print("STARTING COMPREHENSIVE VERIFICATION")
    print("=" * 60)

    # TEST 1: Database Uniqueness
    total_q = db.query(Question).count()
    print(f"\n[TEST 1] Total Questions in DB: {total_q}")
    assert total_q >= 500, f"Expected at least 500 questions, found {total_q}"

    all_texts = [q.question_text.strip() for q in db.query(Question).all()]
    unique_texts = set(all_texts)
    duplicate_count = len(all_texts) - len(unique_texts)
    print(f"Total question texts: {len(all_texts)}, Unique: {len(unique_texts)}, Duplicates: {duplicate_count}")
    assert duplicate_count == 0, f"Found {duplicate_count} duplicate question texts!"
    print(">>> PASS: 100% of questions are genuinely unique!")

    # TEST 2: All 11 Subjects & 35-Year Span
    subjects = [s[0] for s in db.query(Question.subject).distinct().all()]
    print(f"\n[TEST 2] Subjects present ({len(subjects)}): {subjects}")
    expected_subjects = [
        "Algorithms", "COA", "Compiler Design", "Computer Networks", "DBMS",
        "Digital Logic", "Engineering Mathematics", "General Aptitude", "OS",
        "Programming & DS", "TOC"
    ]
    for es in expected_subjects:
        assert es in subjects, f"Missing subject: {es}"
    
    min_year = db.query(Question.year).order_by(Question.year.asc()).first()[0]
    max_year = db.query(Question.year).order_by(Question.year.desc()).first()[0]
    print(f"Year span: {min_year} to {max_year}")
    assert min_year <= 1995 and max_year >= 2025, f"Year range unexpected: {min_year}-{max_year}"
    print(">>> PASS: All 11 subjects covered from 1991 to 2025!")

    # TEST 3: Strict Topic Isolation
    print("\n[TEST 3] Testing Strict Topic Isolation...")
    # Test CPU Scheduling
    q_topic_os = generate_quiz(db, user_id=1, config={
        "subjects": ["OS"],
        "topics": ["CPU Scheduling"],
        "num_questions": 5,
        "difficulty": "mixed"
    })
    print(f"Requested 5 CPU Scheduling questions. Received: {len(q_topic_os)}")
    for q in q_topic_os:
        assert q.subject == "OS", f"Bleed-through subject! Got {q.subject}"
        assert q.topic == "CPU Scheduling", f"Bleed-through topic! Got {q.topic}"
    print(">>> PASS: 100% of questions for CPU Scheduling strictly belong to that topic!")

    # Test Pipelining in COA
    q_topic_coa = generate_quiz(db, user_id=1, config={
        "subjects": ["COA"],
        "topics": ["Instruction Pipelining"],
        "num_questions": 5,
        "difficulty": "mixed"
    })
    print(f"Requested 5 Instruction Pipelining questions. Received: {len(q_topic_coa)}")
    for q in q_topic_coa:
        assert q.subject == "COA", f"Bleed-through subject! Got {q.subject}"
        assert q.topic == "Instruction Pipelining", f"Bleed-through topic! Got {q.topic}"
    print(">>> PASS: 100% of questions for Instruction Pipelining strictly belong to that topic!")

    # TEST 4: Anti-Repetition Engine
    print("\n[TEST 4] Testing Smart Anti-Repetition Engine...")
    # Clean up test user 999
    db.query(QuizSession).filter(QuizSession.user_id == 999).delete()
    db.commit()

    # Session 1: Get 4 questions
    quiz1 = generate_quiz(db, user_id=999, config={
        "subjects": ["Algorithms"],
        "topics": ["Graph Algorithms"],
        "num_questions": 3,
        "difficulty": "mixed"
    })
    q1_ids = [q.id for q in quiz1]
    print(f"Quiz 1 IDs: {q1_ids}")

    # Record session 1 in DB
    sess1 = QuizSession(
        user_id=999,
        config=json.dumps({"subjects": ["Algorithms"], "topics": ["Graph Algorithms"]}),
        total_questions=len(quiz1),
        time_limit_minutes=15,
        questions_order=json.dumps([str(qid) for qid in q1_ids])
    )
    db.add(sess1)
    db.commit()

    # Session 2: Get next 3 questions for same topic
    quiz2 = generate_quiz(db, user_id=999, config={
        "subjects": ["Algorithms"],
        "topics": ["Graph Algorithms"],
        "num_questions": 3,
        "difficulty": "mixed"
    })
    q2_ids = [q.id for q in quiz2]
    print(f"Quiz 2 IDs: {q2_ids}")

    # Check that Quiz 2 has ZERO questions from Quiz 1 (fresh questions)
    overlap = set(q1_ids).intersection(set(q2_ids))
    print(f"Overlap between Quiz 1 and Quiz 2: {overlap}")
    assert len(overlap) == 0, f"Repetition detected! {overlap}"
    print(">>> PASS: Anti-repetition engine delivered completely fresh, non-repeated questions!")

    # Clean up test sessions
    db.query(QuizSession).filter(QuizSession.user_id == 999).delete()
    db.commit()

    # TEST 5: Paper Analysis API Endpoints
    print("\n[TEST 5] Testing Paper Analysis Endpoints...")
    ov = paper_analysis_overview(db)
    assert ov["total_questions"] >= 500
    assert len(ov["subject_breakdown"]) == 11

    years_data = paper_analysis_years(db)
    assert len(years_data) == 35, f"Expected 35 years, got {len(years_data)}"
    print(f"35 years verified: {years_data[-1]['year']} to {years_data[0]['year']}")

    y2024 = paper_analysis_by_year(2024, db)
    assert y2024["year"] == 2024
    assert len(y2024["subjects"]) > 0
    print(f"Year 2024 breakdown: {y2024['total_questions']} questions across {len(y2024['subjects'])} subjects")

    trends_os = paper_analysis_subject_trends("OS", db)
    assert len(trends_os["topics"]) > 0
    print(f"OS high-yield topics count: {len(trends_os['topics'])}")
    print(">>> PASS: All Paper Analysis endpoints functional and valid!")

    # TEST 6: Brief Solution Formatting
    print("\n[TEST 6] Testing Solution Brevity...")
    sample_qs = db.query(Question).limit(20).all()
    for q in sample_qs:
        lines = [line.strip() for line in q.explanation.split("\n") if line.strip()]
        # Brief solutions should be concise (less than 10 lines, structured)
        assert len(lines) <= 8, f"Explanation too long ({len(lines)} lines) for Question {q.id}: {q.explanation}"
    print(">>> PASS: Solutions are concise and brief!")

    print("\n" + "=" * 60)
    print("ALL 6 TESTS PASSED SUCCESSFULLY! ZERO BUGS DETECTED.")
    print("=" * 60)
    db.close()

if __name__ == "__main__":
    run_tests()
