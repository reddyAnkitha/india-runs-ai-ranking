import os
from sentence_transformers import SentenceTransformer, util

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load model ONCE (important fix)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Sample candidate dataset
candidates = [
    {"id": "CAND_0000001", "skills": "python fastapi sql ml"},
    {"id": "CAND_0000002", "skills": "java spring boot backend"},
    {"id": "CAND_0000003", "skills": "python ml data science ai"},
    {"id": "CAND_0000004", "skills": "react frontend javascript html"},
    {"id": "CAND_0000005", "skills": "python django flask api"},
    {"id": "CAND_0000006", "skills": "aws devops docker kubernetes"},
]


def rank_candidates(job_description: str):

    job_embedding = model.encode(job_description, convert_to_tensor=True)

    results = []

    for c in candidates:
        cand_embedding = model.encode(c["skills"], convert_to_tensor=True)

        score = util.cos_sim(job_embedding, cand_embedding).item()
        match_percentage = round(score * 100, 2)

        results.append({
            "candidate_id": c["id"],
            "score": round(score, 3),
            "match_percentage": match_percentage
        })

    # sort
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results