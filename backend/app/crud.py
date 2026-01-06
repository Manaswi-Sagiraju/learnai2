from sqlalchemy.orm import Session
from . import models

# --- Courses / Modules / Topics ---
def get_courses(db: Session):
    return db.query(models.Course).all()

def get_modules_by_course(db: Session, course_id: int):
    return db.query(models.Module).filter(models.Module.course_id==course_id).all()

def get_topics_by_module(db: Session, module_id: int):
    # If module_id=None, return all topics
    query = db.query(models.Topic)
    if module_id is not None:
        query = query.filter(models.Topic.module_id==module_id)
    return query.all()

# --- Quiz Attempts ---
def add_quiz_attempt(db: Session, user_id:int, topic_id:int, score:float, allow_retry:bool=False):
    attempts = db.query(models.QuizAttempt).filter_by(user_id=user_id, topic_id=topic_id).count()
    attempt_number = attempts + 1
    attempt = models.QuizAttempt(user_id=user_id, topic_id=topic_id, score=score, attempt_number=attempt_number, allow_retry=allow_retry)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

def get_quiz_attempts(db: Session, user_id:int, topic_id:int=None):
    query = db.query(models.QuizAttempt).filter_by(user_id=user_id)
    if topic_id:
        query = query.filter_by(topic_id=topic_id)
    return query.all()
