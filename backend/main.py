from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from backend.engine import MentorEngine

app = FastAPI(title="EEF AI-003 — AI Mentor Assistant", version="1.0.0",
              description="Lightweight retrieval-grounded internship mentoring prototype.")
engine = MentorEngine()

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    intern_id: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "AI Mentor Assistant"}

@app.get("/interns")
def get_interns():
    return engine.interns

@app.get("/knowledge")
def get_knowledge():
    return [{"question": x["question"]} for x in engine.faqs]

@app.post("/chat")
def chat(request: ChatRequest):
    return engine.answer(request.question, request.intern_id)

@app.get("/mentor/dashboard")
def mentor_dashboard():
    return {"interns": engine.mentor_summary()}

@app.get("/interns/{intern_id}/learning-plan")
def learning_plan(intern_id: str):
    result = engine.learning_plan(intern_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Intern ID not found")
    return result
