import json

with open(r"E:\india-runs-ai-ranking\data\sample_candidates.json",
          "r",
          encoding="utf-8") as f:
    candidates = json.load(f)

candidate = candidates[0]

print("\n==== PROFILE ====")
print(candidate["profile"])

print("\n==== CAREER HISTORY ====")
print(candidate["career_history"])

print("\n==== SKILLS ====")
print(candidate["skills"])

print("\n==== REDROB SIGNALS ====")
print(candidate["redrob_signals"])