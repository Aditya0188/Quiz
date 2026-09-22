import sys
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models.user import User
from models.quiz_session import QuizSession

client = TestClient(app)

def run_tests():
    print("=== Testing Fixes for User Reported Issues ===\n")

    # 1. Setup a clean test user
    email = "repeat_test_user@gate.com"
    db = SessionLocal()
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        # Clean up previous test sessions
        db.query(QuizSession).filter(QuizSession.user_id == existing.id).delete()
        db.delete(existing)
        db.commit()
    db.close()

    res = client.post("/api/auth/register", json={
        "email": email,
        "name": "Repeat Test User",
        "password": "password123"
    })
    assert res.status_code == 200, f"Register failed: {res.text}"
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # -------------------------------------------------------------
    # TEST 1: SUBJECT ISOLATION (No miscellaneous questions)
    # -------------------------------------------------------------
    print("1. Testing Subject Isolation (selecting 'Operating Systems' / 'OS')...")
    res = client.post("/api/quiz/start", json={
        "subjects": ["Operating Systems"],
        "topics": [],
        "difficulty": "mixed",
        "num_questions": 10,
        "time_limit": 25,
        "question_types": ["MCQ", "MSQ", "NAT"],
        "year_range": [1991, 2025]
    }, headers=headers)
    assert res.status_code == 200, f"Start quiz failed: {res.text}"
    quiz1 = res.json()
    q_list1 = quiz1["questions"]
    assert len(q_list1) == 10, f"Expected 10 questions, got {len(q_list1)}"

    # Verify ALL questions belong STRICTLY to 'OS'
    for q in q_list1:
        assert q["subject"] == "OS", f"ERROR: Found miscellaneous question from subject '{q['subject']}' in OS quiz!"
    print(f"   [PASS] All {len(q_list1)} questions are strictly from 'OS'! Zero miscellaneous questions.")

    # -------------------------------------------------------------
    # TEST 2: CUSTOM TIMER & QUESTION COUNT
    # -------------------------------------------------------------
    print("\n2. Testing Custom Timer & Question Count (7 questions, 17 minutes)...")
    res = client.post("/api/quiz/start", json={
        "subjects": ["Algorithms"],
        "topics": [],
        "difficulty": "mixed",
        "num_questions": 7,
        "time_limit": 17,
        "question_types": ["MCQ", "MSQ", "NAT"],
        "year_range": [1991, 2025]
    }, headers=headers)
    assert res.status_code == 200, f"Start quiz failed: {res.text}"
    custom_quiz = res.json()
    assert len(custom_quiz["questions"]) == 7, f"Expected 7 questions, got {len(custom_quiz['questions'])}"
    assert custom_quiz["time_limit_minutes"] == 17, f"Expected 17 minutes, got {custom_quiz['time_limit_minutes']}"
    for q in custom_quiz["questions"]:
        assert q["subject"] == "Algorithms", f"Expected Algorithms, got {q['subject']}"
    print(f"   [PASS] Custom timer set to exactly 17 mins and exactly 7 questions received.")

    # -------------------------------------------------------------
    # TEST 3: ANTI-REPETITION (Fresh, separate questions each quiz)
    # -------------------------------------------------------------
    print("\n3. Testing Anti-Repetition across multiple consecutive quizzes for same subject...")
    # Quiz 1 for Computer Networks (10 questions)
    res = client.post("/api/quiz/start", json={
        "subjects": ["Computer Networks"],
        "num_questions": 10,
        "time_limit": 20
    }, headers=headers)
    q_set1_ids = {q["id"] for q in res.json()["questions"]}
    print(f"   Quiz 1 (Computer Networks): Got {len(q_set1_ids)} questions: {sorted(list(q_set1_ids))}")

    # Quiz 2 for Computer Networks (10 questions)
    res = client.post("/api/quiz/start", json={
        "subjects": ["Computer Networks"],
        "num_questions": 10,
        "time_limit": 20
    }, headers=headers)
    q_set2_ids = {q["id"] for q in res.json()["questions"]}
    print(f"   Quiz 2 (Computer Networks): Got {len(q_set2_ids)} questions: {sorted(list(q_set2_ids))}")

    # Check intersection between Quiz 1 and Quiz 2
    overlap_1_2 = q_set1_ids.intersection(q_set2_ids)
    assert len(overlap_1_2) == 0, f"FAILED: Found {len(overlap_1_2)} repeating questions between Quiz 1 and Quiz 2: {overlap_1_2}"
    print(f"   [PASS] ZERO overlapping questions between Quiz 1 and Quiz 2! (Overlap = {len(overlap_1_2)})")

    # Quiz 3 for Computer Networks (10 questions)
    res = client.post("/api/quiz/start", json={
        "subjects": ["Computer Networks"],
        "num_questions": 10,
        "time_limit": 20
    }, headers=headers)
    q_set3_ids = {q["id"] for q in res.json()["questions"]}
    print(f"   Quiz 3 (Computer Networks): Got {len(q_set3_ids)} questions: {sorted(list(q_set3_ids))}")

    # Check intersection with Quiz 1 and Quiz 2
    overlap_all = q_set3_ids.intersection(q_set1_ids.union(q_set2_ids))
    assert len(overlap_all) == 0, f"FAILED: Found {len(overlap_all)} repeating questions in Quiz 3: {overlap_all}"
    print(f"   [PASS] ZERO overlapping questions in Quiz 3 across all previous attempts! (Overlap = {len(overlap_all)})")
    print(f"   Total unique questions served across 3 consecutive quizzes: {len(q_set1_ids | q_set2_ids | q_set3_ids)} / 30")

    # -------------------------------------------------------------
    # TEST 4: CUSTOM MIX (All subjects)
    # -------------------------------------------------------------
    print("\n4. Testing 'Custom Mix' / 'MIX' parameter...")
    res = client.post("/api/quiz/start", json={
        "subjects": ["MIX"],
        "num_questions": 11,
        "time_limit": 30
    }, headers=headers)
    assert res.status_code == 200, f"MIX start failed: {res.text}"
    mix_questions = res.json()["questions"]
    mix_subjects = {q["subject"] for q in mix_questions}
    print(f"   [PASS] MIX quiz successfully generated with {len(mix_questions)} questions from {len(mix_subjects)} different subjects: {mix_subjects}")

    print("\n=== ALL 4 USER-REPORTED ISSUE TESTS PASSED 100%! ===")

if __name__ == "__main__":
    run_tests()
