from fastapi import FastAPI
from pydantic import BaseModel
from backend.ranking import rank_candidates

app = FastAPI()

class JobRequest(BaseModel):
    job_description: str


@app.get("/")
def home():
    return {"message": "Backend Running"}


@app.post("/rank")
def rank(job: JobRequest):
    return rank_candidates(job.job_description)