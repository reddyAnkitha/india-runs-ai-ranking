from pydantic import BaseModel


class CandidateScore(BaseModel):
    candidate_id: str
    score: float
    match_percentage: float