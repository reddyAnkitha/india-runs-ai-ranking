import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")

def rank_candidates(job_description, candidates):

    jd_embedding = model.encode([job_description])

    results = []

    for c in candidates:
        profile = c.get("profile", {})

        text = profile.get("headline", "") + " " + profile.get("summary", "")

        cand_embedding = model.encode([text])

        score = cosine_similarity(jd_embedding, cand_embedding)[0][0]

        results.append({
            "candidate_id": c["candidate_id"],
            "score": round(float(score), 3),
            "match_percentage": round(float(score) * 100, 2)
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results