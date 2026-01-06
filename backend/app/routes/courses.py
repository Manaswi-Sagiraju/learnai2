from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database, schemas
from typing import List

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/courses", response_model=List[schemas.Course])
def read_courses(db: Session = Depends(get_db)):
    return crud.get_courses(db)

@router.get("/courses/{course_id}/modules", response_model=List[schemas.Module])
def read_modules(course_id: int, db: Session = Depends(get_db)):
    return crud.get_modules_by_course(db, course_id)

@router.get("/modules/{module_id}/topics", response_model=List[schemas.Topic])
def read_topics(module_id: int, db: Session = Depends(get_db)):
    return crud.get_topics_by_module(db, module_id)
