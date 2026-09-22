import json
import google.generativeai as genai
from config import settings
from models.question import Question

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_similar_questions(question: Question, count: int) -> list:
    if not settings.GEMINI_API_KEY:
        return []
        
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    You are an expert GATE Computer Science exam creator.
    Generate {count} similar questions based on the following original question.
    
    Original Question Details:
    Subject: {question.subject}
    Topic: {question.topic}
    Type: {question.question_type}
    Difficulty: {question.difficulty}
    Marks: {question.marks}
    Text: {question.question_text}
    Options: {question.options}
    Correct Answer: {question.correct_answer}
    Explanation: {question.explanation}
    
    Generate {count} new questions with the EXACT same difficulty level and testing the same underlying concept but with different values, scenarios, or phrasing.
    Return ONLY a JSON array of objects with the following schema:
    [
      {{
        "question_text": "string",
        "options": "JSON string of options (if MCQ/MSQ) else null",
        "correct_answer": "string (A/B/C/D for MCQ, A,B for MSQ, numeric for NAT)",
        "nat_tolerance": float (default 0.01),
        "explanation": "string",
        "question_type": "{question.question_type}",
        "marks": {question.marks},
        "difficulty": "{question.difficulty}"
      }}
    ]
    Do not include markdown formatting like ```json in the output, just the raw JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        
        parsed = json.loads(text)
        new_questions = []
        for item in parsed:
            new_q = Question(
                subject=question.subject,
                topic=question.topic,
                year=2025, # Mark as new
                question_type=item["question_type"],
                difficulty=item["difficulty"],
                marks=item["marks"],
                question_text=item["question_text"],
                options=item.get("options"),
                correct_answer=item["correct_answer"],
                nat_tolerance=item.get("nat_tolerance", 0.01),
                explanation=item["explanation"],
                is_pyq=False,
                source_pyq_id=question.id
            )
            new_questions.append(new_q)
        return new_questions
    except Exception as e:
        print(f"Error generating AI questions: {e}")
        return []
