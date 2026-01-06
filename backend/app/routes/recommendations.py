from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database, utils, schemas
import pandas as pd
from typing import List

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/recommendations/{user_id}", response_model=List[schemas.Recommendation])
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    # --- Fetch attempts ---
    attempts_db = crud.get_quiz_attempts(db, user_id=user_id, topic_id=None)
    df_attempts = pd.DataFrame([{
        'topic_id': a.topic_id,
        'score': a.score,
        'attempts': a.attempt_number
    } for a in attempts_db])

    # --- Fetch all topics ---
    topics_db = crud.get_topics_by_module(db, module_id=None)
    df_topics = pd.DataFrame([{
        'topic_id': t.id,
        'difficulty': t.difficulty,
        'name': t.name
    } for t in topics_db])

    # --- Generate recommendations ---
    recommended = utils.recommend_topics(df_attempts, df_topics, top_n=5)

    # --- Add score and reason ---
    attempts_records = df_attempts.to_dict('records')
    for r in recommended:
        attempt = next((a for a in attempts_records if a['topic_id'] == r['topic_id']), None)
        r['score'] = attempt['score'] if attempt else 0
        if attempt and attempt['score'] < 50:
            r['reason'] = "Low score in previous quiz"
        elif attempt and attempt['attempts'] > 1:
            r['reason'] = "Multiple failed attempts"
        else:
            r['reason'] = "Next topic based on difficulty similarity"

    return recommended
