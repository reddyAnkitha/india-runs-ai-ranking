import json

# Skills required for the role
required_skills = [
    "Python",
    "NLP",
    "Fine-tuning LLMs",
    "Milvus",
    "AWS"
]

with open(r"E:\india-runs-ai-ranking\data\sample_candidates.json",
          "r",
          encoding="utf-8") as f:
    candidates = json.load(f)


def calculate_score(candidate):
    score = 0

    # Experience
    score += candidate["profile"]["years_of_experience"] * 5

    # Open to work
    if candidate["redrob_signals"]["open_to_work_flag"]:
        score += 20

    # GitHub activity
    score += candidate["redrob_signals"]["github_activity_score"]

    # Interview completion rate
    score += candidate["redrob_signals"]["interview_completion_rate"] * 20

    # Skills score
    candidate_skills = [skill["name"] for skill in candidate["skills"]]

    matched_skills = set(candidate_skills).intersection(required_skills)

    score += len(matched_skills) * 10

    return round(score, 2)


for candidate in candidates:
    candidate["score"] = calculate_score(candidate)

ranked_candidates = sorted(
    candidates,
    key=lambda x: x["score"],
    reverse=True
)

print("\nTop 10 Candidates:\n")

for c in ranked_candidates[:10]:
    candidate_skills = [s["name"] for s in c["skills"]]

    matched_skills = set(candidate_skills).intersection(required_skills)

    print(
        c["candidate_id"],
        "Score =", c["score"],
        "Matched Skills =", list(matched_skills)
    )