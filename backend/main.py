from fastapi import FastAPI
from pydantic import BaseModel
import json
from backend.ranking import rank_candidates

app = FastAPI()   # 👈 THIS MUST EXIST

class JobRequest(BaseModel):
    job_description: str

@app.get("/")
def home():
    return {"message": "ATS Backend Running"}

@app.post("/rank")
def rank(job: JobRequest):

    with open("data/sample_candidates.json", "r", encoding="utf-8") as f:
        candidates = json.load(f)

    return rank_candidates(job.job_description, candidates)