import json

with open(r"E:\india-runs-ai-ranking\data\sample_candidates.json",
          "r",
          encoding="utf-8") as f:
    candidates = json.load(f)

print("Number of sample candidates:", len(candidates))

print("\nFirst Candidate:\n")
print(candidates[0])