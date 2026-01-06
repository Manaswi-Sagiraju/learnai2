from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---------------- Users ----------------
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True


# ---------------- Courses / Modules / Topics ----------------
class TopicBase(BaseModel):
    name: str
    content: Optional[str] = None
    difficulty: Optional[float] = 1.0
    module_id: int

class TopicCreate(TopicBase):
    pass

class Topic(TopicBase):
    id: int

    class Config:
        from_attributes = True


class ModuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    course_id: int

class ModuleCreate(ModuleBase):
    pass

class Module(ModuleBase):
    id: int
    topics: Optional[List[Topic]] = []

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    modules: Optional[List[Module]] = []

    class Config:
        from_attributes = True


# ---------------- Quiz Attempts ----------------
class QuizAttemptBase(BaseModel):
    user_id: int
    topic_id: int
    score: float
    attempt_number: Optional[int] = 1
    allow_retry: Optional[bool] = False

class QuizAttemptCreate(QuizAttemptBase):
    pass

class QuizAttempt(QuizAttemptBase):
    id: int
    completed_at: datetime

    class Config:
        from_attributes = True


# ---------------- Recommendations ----------------
class Recommendation(BaseModel):
    topic_id: int
    name: str
    score: Optional[float] = 0
    reason: str
