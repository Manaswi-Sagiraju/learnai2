from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import courses, quizzes, recommendations
from .database import init_db

app = FastAPI(title="AI-Based Personalized Learning Platform")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router)
app.include_router(quizzes.router)
app.include_router(recommendations.router)

@app.get("/")
def home():
    return {"message": "Learning Platform API Running"}
