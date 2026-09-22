from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import User
from models.question import Question
from services.auth_service import get_current_user
from services.ai_service import generate_similar_questions

router = APIRouter(prefix="/api/ai", tags=["ai"])

class GenerateRequest(BaseModel):
    question_id: int
    count: int = 1

@router.post("/generate")
def generate_questions(req: GenerateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = db.query(Question).filter(Question.id == req.question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
        
    if req.count > 5:
        raise HTTPException(status_code=400, detail="Cannot generate more than 5 questions at once")
        
    new_qs = generate_similar_questions(q, req.count)
    if not new_qs:
        raise HTTPException(status_code=500, detail="Failed to generate questions. Check API key.")
        
    for new_q in new_qs:
        db.add(new_q)
    db.commit()
    
    return [
        {
            "id": nq.id,
            "question_text": nq.question_text
        } for nq in new_qs
    ]
