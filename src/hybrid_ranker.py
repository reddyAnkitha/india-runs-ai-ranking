import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load data
with open(r"E:\india-runs-ai-ranking\data\job_description.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

with open(r"E:\india-runs-ai-ranking\data\sample_candidates.json", "r", encoding="utf-8") as f:
    candidates = json.load(f)

jd_emb = model.encode([jd_text])

results = []

for c in candidates:
    profile = c["profile"]

    # -------------------------
    # 1. Semantic Score
    # -------------------------
    candidate_text = profile["headline"] + " " + profile["summary"]
    cand_emb = model.encode([candidate_text])
    semantic_score = cosine_similarity(jd_emb, cand_emb)[0][0]

    # -------------------------
    # 2. Skill Score (simple overlap logic)
    # -------------------------
    jd_skills = set(jd_text.lower().split())
    cand_skills = set(candidate_text.lower().split())

    skill_score = len(jd_skills.intersection(cand_skills)) / (len(jd_skills) + 1)

    # -------------------------
    # 3. Experience Score (basic heuristic)
    # -------------------------
    experience = profile.get("experience_years", 0)
    exp_score = min(experience / 10, 1)   # normalize to 0–1

    # -------------------------
    # FINAL HYBRID SCORE
    # -------------------------
    final_score = (
        0.5 * semantic_score +
        0.3 * skill_score +
        0.2 * exp_score
    )

    results.append({
        "candidate_id": c["candidate_id"],
        "semantic_score": round(semantic_score, 4),
        "skill_score": round(skill_score, 4),
        "experience_score": round(exp_score, 4),
        "final_score": round(final_score, 4)
    })

# Sort by final score
results = sorted(results, key=lambda x: x["final_score"], reverse=True)

# Save output
df = pd.DataFrame(results)
df.to_csv(r"E:\india-runs-ai-ranking\output\final_rankings.csv", index=False)

print("\n TOP CANDIDATES (HYBRID MODEL)\n")
print(df.head(10))
print("\n File saved: output/final_rankings.csv")