import json

# Load candidates
with open(r"E:\india-runs-ai-ranking\data\sample_candidates.json",
          "r",
          encoding="utf-8") as f:
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
        set(candidate_skills)
        &
        set(required_skills)
    )

    score = len(matched)

    results.append(
        {
            "candidate_id": candidate["candidate_id"],
            "score": score,
            "matched_skills": matched
        }
    )

results.sort(
    key=lambda x: x["score"],
    reverse=True
)

print("\nTop 10 Candidates\n")

for r in results[:10]:
    print(r)