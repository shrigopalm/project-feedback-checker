"""Small web API around the feedback function.

Run:  uvicorn app:app --reload
Docs: http://127.0.0.1:8000/docs  (FastAPI makes this page automatically)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from llm import get_feedback

app = FastAPI(title="Project Feedback Checker")


class ProjectIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/feedback")
def feedback(project: ProjectIn):
    text = f"Title: {project.title}\n\n{project.description}"
    try:
        return get_feedback(text)
    except RuntimeError as e:
        # 502 = our server is fine, the model behind it failed
        raise HTTPException(status_code=502, detail=str(e))
