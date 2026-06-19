import json

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

    return round(score, 2)


for candidate in candidates:
    candidate["score"] = calculate_score(candidate)

# Sort candidates by score
ranked_candidates = sorted(
    candidates,
    key=lambda x: x["score"],
    reverse=True
)

print("\nTop 5 Candidates:\n")

for c in ranked_candidates[:5]:
    print(c["candidate_id"], "Score =", c["score"])