import sys
import json
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models.user import User

client = TestClient(app)

def test_full_flow():
    print("--- 1. Testing Root Endpoint ---")
    res = client.get("/")
    assert res.status_code == 200, f"Failed root: {res.text}"
    print("[PASS] Root endpoint working:", res.json())

    print("\n--- 2. Testing Registration ---")
    test_email = "teststudent@example.com"
    # Clean up if already exists
    db = SessionLocal()
    existing = db.query(User).filter(User.email == test_email).first()
    if existing:
        db.delete(existing)
        db.commit()
    db.close()

    res = client.post("/api/auth/register", json={
        "email": test_email,
        "name": "GATE Aspirant",
        "password": "password123"
    })
    assert res.status_code == 200, f"Register failed: {res.text}"
    auth_data = res.json()
    token = auth_data["access_token"]
    assert token, "Token not returned"
    print("[PASS] Registration successful. Token received.")

    headers = {"Authorization": f"Bearer {token}"}

    print("\n--- 3. Testing Login ---")
    res = client.post("/api/auth/login", json={
        "email": test_email,
        "password": "password123"
    })
    assert res.status_code == 200, f"Login failed: {res.text}"
    print("[PASS] Login successful.")

    print("\n--- 4. Testing /api/auth/me ---")
    res = client.get("/api/auth/me", headers=headers)
    assert res.status_code == 200, f"Get me failed: {res.text}"
    print("[PASS] Profile verified for user:", res.json()["name"])

    print("\n--- 5. Testing /api/subjects ---")
    res = client.get("/api/subjects")
    assert res.status_code == 200, f"Get subjects failed: {res.text}"
    subjects = res.json()
    assert len(subjects) > 0, "No subjects returned"
    print(f"[PASS] Retrieved {len(subjects)} subjects. Example: {subjects[0]['subject']} with {subjects[0]['question_count']} questions.")

    print("\n--- 6. Testing /api/questions/stats ---")
    res = client.get("/api/questions/stats")
    assert res.status_code == 200, f"Stats failed: {res.text}"
    stats = res.json()
    print(f"[PASS] Total questions in bank: {stats['total_questions']}, Year range: {stats['year_range']}")

    print("\n--- 7. Testing /api/quiz/start (Dynamic Quiz Generation) ---")
    quiz_config = {
        "subjects": ["Operating Systems", "Algorithms"],
        "topics": [],
        "difficulty": "mixed",
        "num_questions": 5,
        "time_limit": 20,
        "question_types": ["MCQ", "MSQ", "NAT"],
        "year_range": [1991, 2025],
        "include_ai": False
    }
    res = client.post("/api/quiz/start", json=quiz_config, headers=headers)
    assert res.status_code == 200, f"Start quiz failed: {res.text}"
    quiz_data = res.json()
    session_id = quiz_data["session_id"]
    questions = quiz_data["questions"]
    assert len(questions) == 5, f"Expected 5 questions, got {len(questions)}"
    print(f"[PASS] Generated Quiz Session #{session_id} with {len(questions)} randomized questions.")

    print("\n--- 8. Testing /api/quiz/{session_id}/submit (Scoring & Evaluation) ---")
    # Formulate responses for questions
    responses = {}
    for i, q in enumerate(questions):
        q_id = str(q["id"])
        # Provide sample answers: answer first question with 'A', leave some, provide numeric for NAT
        if q["question_type"] == "MCQ":
            responses[q_id] = {"answer": "A", "time_spent": 30}
        elif q["question_type"] == "NAT":
            responses[q_id] = {"answer": "10.0", "time_spent": 45}
        else:
            responses[q_id] = {"answer": "A,B", "time_spent": 40}

    res = client.post(f"/api/quiz/{session_id}/submit", json={"responses": responses}, headers=headers)
    assert res.status_code == 200, f"Submit quiz failed: {res.text}"
    result = res.json()
    print(f"[PASS] Quiz submitted successfully! Score: {result['score']}/{result['max_score']}, Correct: {result['correct_count']}, Wrong: {result['wrong_count']}")

    print("\n--- 9. Testing /api/quiz/{session_id} (Detailed Results & Explanations) ---")
    res = client.get(f"/api/quiz/{session_id}", headers=headers)
    assert res.status_code == 200, f"Get details failed: {res.text}"
    details = res.json()
    assert "questions" in details, "Questions not in details"
    first_q = details["questions"][0]
    assert "explanation" in first_q, "Explanation not returned after submission"
    print(f"[PASS] Verified detailed results with solutions and explanations.")

    print("\n--- 10. Testing /api/quiz/history ---")
    res = client.get("/api/quiz/history", headers=headers)
    assert res.status_code == 200, f"History failed: {res.text}"
    hist_data = res.json()
    assert hist_data["total"] >= 1, "History total is 0"
    print(f"[PASS] Quiz history retrieved successfully: {hist_data['total']} sessions recorded.")

    print("\n--- 11. Testing /api/analytics/full ---")
    res = client.get("/api/analytics/full", headers=headers)
    assert res.status_code == 200, f"Full analytics failed: {res.text}"
    analytics = res.json()
    assert "overview" in analytics, "Overview missing in analytics"
    assert "scoreTrend" in analytics, "ScoreTrend missing in analytics"
    print(f"[PASS] Analytics returned successfully: Overview: {analytics['overview']}")

    print("\nALL 11 BACKEND API TESTS PASSED SUCCESSFULLY! 100% WORKING!")

if __name__ == "__main__":
    test_full_flow()
