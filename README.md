# EEF AI-003 — AI Mentor Assistant & Internship Intelligence Platform

A simple Streamlit + FastAPI prototype demonstrating internship Q&A, local knowledge retrieval, sample intern progress summaries, skill-gap detection, mentor feedback context, and weekly learning plans.

## Features
- Student Q&A using FAQ and case-study knowledge chunks.
- Retrieved-source display and a heuristic confidence estimate.
- Optional intern context in chat.
- Mentor dashboard with progress, sample feedback, skill gaps, and basic risk flags.
- Personalized learning plan from missing required skills.
- FastAPI Swagger API docs.

## Scope and limitations
This is a demonstration, not a live Ezitech portal integration. Data in `data/` is synthetic. Retrieval is a lightweight keyword-overlap baseline, not transformer embeddings or an external vector database. It does not use an external LLM, Redis, Docker, or real GitHub/portal connectors. Those can be added later if required.

## Requirements
Python 3.10+ recommended.

## Windows setup
Open PowerShell in the project root.

1. Install backend dependencies:
   `python -m pip install -r backend/requirements.txt`
2. Install frontend dependencies:
   `python -m pip install -r frontend/requirements.txt`
3. Start backend in terminal 1:
   `python -m uvicorn backend.main:app --reload`
   API: `http://127.0.0.1:8000` · Docs: `http://127.0.0.1:8000/docs`
4. Start frontend in terminal 2:
   `python -m streamlit run frontend/app.py`
   Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Tests
`python -m pip install pytest`
`python -m pytest`

## Demo questions
- How should I submit an internship task?
- What should a project README contain?
- How do I ask for debugging help?
- What if the assistant does not know the answer?

## Folder structure
- `backend/`: API and recommendation logic
- `frontend/`: Streamlit UI
- `data/`: FAQs, case studies, sample interns, sample feedback
- `docs/`: architecture, API, evaluation, prompt policy
- `tests/`: basic automated checks

## Future improvements
1. Connect authenticated and approved portal data.
2. Add embeddings and FAISS/Chroma for semantic retrieval.
3. Add a grounded LLM and evaluation dataset.
4. Store session memory and feedback in SQLite/PostgreSQL.
5. Add authentication, audit logging, privacy controls, and mentor approval.
