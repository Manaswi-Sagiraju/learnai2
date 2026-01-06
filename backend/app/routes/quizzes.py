from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel   # ✅ ADD THIS LINE
from .. import crud, database, utils, schemas
import pandas as pd

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class QuizSubmitRequest(schemas.QuizAttemptBase):
    pass

class QuizSubmitResponse(BaseModel):
    attempt: int
    weak_topics: list
    status: str

@router.post("/quiz/submit", response_model=dict)
def submit_quiz(user_id:int, topic_id:int, score:float, db: Session = Depends(get_db)):
    # Save attempt
    attempt = crud.add_quiz_attempt(db, user_id, topic_id, score)
    
    # Get all attempts for this topic
    attempts = crud.get_quiz_attempts(db, user_id, topic_id)
    df = pd.DataFrame([{'topic_id': a.topic_id, 'score': a.score, 'attempts': a.attempt_number} for a in attempts])
    
    # Detect weak topics
    weak_topics = utils.detect_knowledge_gap(df)
    
    return {
        "attempt": attempt.id,
        "weak_topics": weak_topics.to_dict('records') if not weak_topics.empty else [],
        "status": "Completed" if score >=50 else "Needs Improvement"
    }
