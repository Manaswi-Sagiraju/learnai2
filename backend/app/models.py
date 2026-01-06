from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    modules = relationship("Module", back_populates="course")

class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    name = Column(String)
    description = Column(String)
    course = relationship("Course", back_populates="modules")
    topics = relationship("Topic", back_populates="module")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    name = Column(String)
    content = Column(String)
    difficulty = Column(Float, default=1.0)
    module = relationship("Module", back_populates="topics")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    score = Column(Float)
    attempt_number = Column(Integer, default=1)
    completed_at = Column(DateTime, default=datetime.utcnow)
    allow_retry = Column(Boolean, default=False)
