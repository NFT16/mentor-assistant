# API Documentation

Start backend with `python -m uvicorn backend.main:app --reload`. Swagger UI: `http://127.0.0.1:8000/docs`.

- `GET /health` — service status.
- `GET /interns` — sample intern profiles.
- `GET /knowledge` — available FAQ titles.
- `POST /chat` — request JSON such as `{"question":"How should I submit an internship task?","intern_id":"INT-001"}`; returns answer, retrieved sources, and heuristic confidence.
- `GET /mentor/dashboard` — progress, feedback, skill gaps, and rule-based risk flags.
- `GET /interns/{intern_id}/learning-plan` — skill gaps and weekly milestones.
