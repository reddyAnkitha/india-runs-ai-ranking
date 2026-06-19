import streamlit as st
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Candidate Ranking System", layout="wide")

st.title("🚀 AI-Powered Candidate Ranking System")
st.write("Hybrid AI model using Semantic + Skill + Experience scoring")

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

    candidate_text = profile["headline"] + " " + profile["summary"]
    cand_emb = model.encode([candidate_text])

    semantic_score = cosine_similarity(jd_emb, cand_emb)[0][0]

    jd_words = set(jd_text.lower().split())
    cand_words = set(candidate_text.lower().split())

    skill_score = len(jd_words.intersection(cand_words)) / (len(jd_words) + 1)

    experience = profile.get("experience_years", 0)
    exp_score = min(experience / 10, 1)

    final_score = 0.5 * semantic_score + 0.3 * skill_score + 0.2 * exp_score

    results.append({
        "Candidate ID": c["candidate_id"],
        "Semantic Score": round(semantic_score, 3),
        "Skill Score": round(skill_score, 3),
        "Experience Score": round(exp_score, 3),
        "Final Score": round(final_score, 3)
    })

df = pd.DataFrame(results).sort_values(by="Final Score", ascending=False)

st.subheader("🏆 Ranked Candidates")
st.dataframe(df)

st.subheader("📊 Top 5 Candidates")
st.bar_chart(df.set_index("Candidate ID")["Final Score"])