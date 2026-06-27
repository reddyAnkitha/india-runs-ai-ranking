import json
import pandas as pd

# Load candidates
with open(
    r"E:\india-runs-ai-ranking\data\sample_candidates.json",
    "r",
    encoding="utf-8"
) as f:
    candidates = json.load(f)

required_skills = [
    "Python",
    "NLP",
    "Fine-tuning LLMs",
    "Milvus",
    "LoRA",
    "AWS"
]

results = []

for candidate in candidates:

    candidate_skills = [
        skill["name"]
        for skill in candidate["skills"]
    ]

    matched = list(
        set(candidate_skills) &
        set(required_skills)
    )

    skill_score = len(matched) * 10

    exp_score = candidate["profile"]["years_of_experience"]

    signals = candidate["redrob_signals"]

    open_score = 10 if signals["open_to_work_flag"] else 0

    profile_score = signals["profile_completeness_score"] / 10

    response_score = signals["recruiter_response_rate"] * 20

    github_score = signals["github_activity_score"]

    final_score = (
        skill_score
        + exp_score
        + open_score
        + profile_score
        + response_score
        + github_score
    )

    results.append({
        "candidate_id": candidate["candidate_id"],
        "score": round(final_score, 2),
        "matched_skills": ", ".join(matched)
    })

# Sort descending
results.sort(
    key=lambda x: x["score"],
    reverse=True
)

# Top 10
top10 = results[:10]

# Save CSV
df = pd.DataFrame(top10)

df.to_csv(
    "hackathon_final_rankings.csv",
    index=False
)

print("\nTOP 10 CANDIDATES\n")

for r in top10:
    print(r)

print("\nCSV created successfully!")