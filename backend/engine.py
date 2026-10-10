from pathlib import Path
import json, re

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)

class MentorEngine:
    def __init__(self):
        self.faqs = load_json("knowledge_base.json")
        self.case_studies = load_json("case_studies.json")
        self.interns = load_json("interns.json")
        self.feedback = load_json("feedback.json")
        self.chunks = []
        for item in self.faqs:
            self.chunks.append({"title": item["question"], "text": item["answer"], "source": "FAQ",
                                "terms": self.terms(item["question"] + " " + item["answer"])})
        for item in self.case_studies:
            text = item["summary"] + " Requirements: " + ", ".join(item["requirements"])
            self.chunks.append({"title": item["title"], "text": text, "source": "Case Study",
                                "terms": self.terms(item["title"] + " " + text)})

    @staticmethod
    def terms(text):
        return set(re.findall(r"[a-zA-Z0-9+#.-]+", text.lower()))

    def retrieve(self, question, limit=3):
        qterms = self.terms(question)
        found = []
        for chunk in self.chunks:
            overlap = len(qterms & chunk["terms"])
            if overlap:
                found.append((overlap / max(1, len(qterms)), chunk))
        found.sort(key=lambda x: x[0], reverse=True)
        return [{"title": c["title"], "text": c["text"], "source": c["source"], "score": round(s, 3)}
                for s, c in found[:limit]]

    def answer(self, question, intern_id=None):
        if not question.strip():
            return {"answer": "Please enter a question.", "sources": [], "confidence": 0.0}
        results = self.retrieve(question)
        if not results:
            return {"answer": "I could not find a sufficiently relevant answer in the local internship knowledge base. Please check the official portal or ask your mentor rather than relying on a guess.", "sources": [], "confidence": 0.15}
        top = results[0]
        answer = f"Based on **{top['title']}** ({top['source']}): {top['text']}"
        if len(results) > 1:
            answer += "\n\nRelated context:\n" + "\n".join(f"- {r['title']}: {r['text']}" for r in results[1:])
        if intern_id:
            intern = self.get_intern(intern_id)
            if intern:
                answer += f"\n\nYour sample profile shows track **{intern['track']}** and progress **{intern['progress']}%**."
        return {"answer": answer, "sources": results, "confidence": min(0.95, round(top["score"] + 0.35, 2))}

    def get_intern(self, intern_id):
        return next((x for x in self.interns if x["intern_id"] == intern_id), None)

    def mentor_summary(self):
        summaries = []
        for intern in self.interns:
            feedback = [f for f in self.feedback if f["intern_id"] == intern["intern_id"]]
            known = {s.lower() for s in intern["skills"]}
            gaps = [s for s in intern["required_skills"] if s.lower() not in known]
            risk = "High" if intern["progress"] < 35 else "Medium" if intern["progress"] < 65 else "Low"
            summaries.append({**intern, "skill_gaps": gaps, "risk_level": risk,
                              "latest_feedback": feedback[-1]["comment"] if feedback else "No feedback recorded"})
        return summaries

    def learning_plan(self, intern_id):
        intern = self.get_intern(intern_id)
        if not intern:
            return None
        known = {s.lower() for s in intern["skills"]}
        gaps = [s for s in intern["required_skills"] if s.lower() not in known]
        plan = [{"week": i, "focus": skill,
                 "milestone": f"Complete one beginner exercise and document what you learned about {skill}."}
                for i, skill in enumerate(gaps[:4], start=1)]
        if not plan:
            plan = [{"week": 1, "focus": "Portfolio improvement",
                     "milestone": "Improve README, add a small test, and request mentor review."}]
        return {"intern": intern, "skill_gaps": gaps, "plan": plan}
