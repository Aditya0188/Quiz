from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True, nullable=False)
    topic = Column(String, index=True, nullable=False)
    year = Column(Integer, index=True, nullable=False)
    set_number = Column(String, nullable=True)
    question_type = Column(String, nullable=False) # MCQ, MSQ, NAT
    difficulty = Column(String, nullable=False) # easy, medium, hard
    marks = Column(Integer, nullable=False) # 1 or 2
    
    question_text = Column(String, nullable=False)
    options = Column(String, nullable=True) # JSON string
    correct_answer = Column(String, nullable=False)
    nat_tolerance = Column(Float, default=0.01)
    
    explanation = Column(String, nullable=True)
    is_pyq = Column(Boolean, default=True)
    source_pyq_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    tags = Column(String, nullable=True) # JSON string
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
