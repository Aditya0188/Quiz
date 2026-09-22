from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from database import Base

class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    config = Column(String, nullable=False) # JSON
    
    total_questions = Column(Integer, nullable=False)
    time_limit_minutes = Column(Integer, nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    score = Column(Float, default=0.0)
    max_score = Column(Float, default=0.0)
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)
    unanswered_count = Column(Integer, default=0)
    
    responses = Column(String, nullable=True) # JSON - {question_id: {answer, time_spent, marked_for_review}}
    questions_order = Column(String, nullable=True) # JSON - list of question IDs
