import sys
sys.path.append(r"E:\python_packages")

import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading model...")
model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

# Load candidates
with open(
    r"E:\india-runs-ai-ranking\data\sample_candidates.json",
    "r",
    encoding="utf-8"
) as f:
    candidates = json.load(f)

# Load job description
with open(
    r"E:\india-runs-ai-ranking\data\job_description.txt",
    "r",
    encoding="utf-8"
) as f:
    jd_text = f.read()

print("Encoding JD...")
jd_embedding = model.encode([jd_text])

results = []

print("Computing similarities...")

for candidate in candidates:

    text = (
        candidate["profile"]["headline"] + " " +
        candidate["profile"]["summary"] + " " +
        " ".join(skill["name"] for skill in candidate["skills"])
    )

    candidate_embedding = model.encode([text])

    similarity = cosine_similarity(
        jd_embedding,
        candidate_embedding
    )[0][0]

    results.append({
        "candidate_id": candidate["candidate_id"],
        "score": round(float(similarity), 4)
    })

# Sort descending
results = sorted(
    results,
    key=lambda x: x["score"],
    reverse=True
)

# Create DataFrame
submission = pd.DataFrame(results)

# Add rank column
submission["rank"] = range(1, len(submission) + 1)

# Keep only required columns
submission = submission[
    ["candidate_id", "rank"]
]

# Save CSV
submission.to_csv(
    r"E:\india-runs-ai-ranking\submission.csv",
    index=False
)

print("\nsubmission.csv created successfully!")
print(submission.head(10))