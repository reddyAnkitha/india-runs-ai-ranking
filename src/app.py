import streamlit as st
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="AI Candidate Ranking System", layout="wide")

st.title("🚀 AI-Powered Candidate Ranking System")
st.write("Hybrid AI model using Semantic + Skill + Experience scoring")

# ----------------------------
# Load Model (cache recommended)
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# Load Data (IMPORTANT: relative paths)
# ----------------------------
with open("data/job_description.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

with open("data/sample_candidates.json", "r", encoding="utf-8") as f:
    candidates = json.load(f)

# Debug (remove later if you want)
st.subheader("🔍 Sample Candidate Data")
st.write(candidates[0])

# ----------------------------
# Encode Job Description
# ----------------------------
jd_emb = model.encode([jd_text])

results = []

# ----------------------------
# Ranking Logic
# ----------------------------
for c in candidates:
    try:
        # SAFE ACCESS (adjust if your JSON differs)
        profile = c.get("profile", c)

        headline = profile.get("headline", "")
        summary = profile.get("summary", "")
        candidate_text = headline + " " + summary

        cand_emb = model.encode([candidate_text])

        # Semantic score
        semantic_score = cosine_similarity(jd_emb, cand_emb)[0][0]

        # Skill score (simple overlap)
        jd_words = set(jd_text.lower().split())
        cand_words = set(candidate_text.lower().split())
        skill_score = len(jd_words.intersection(cand_words)) / (len(jd_words) + 1)

        # Experience score
        experience = profile.get("experience_years", 0)
        exp_score = min(experience / 10, 1)

        # Final score
        final_score = (
            0.5 * semantic_score +
            0.3 * skill_score +
            0.2 * exp_score
        )

        results.append({
            "Candidate ID": c.get("candidate_id", "UNKNOWN"),
            "Semantic Score": round(semantic_score, 3),
            "Skill Score": round(skill_score, 3),
            "Experience Score": round(exp_score, 3),
            "Final Score": round(final_score, 3)
        })

    except Exception as e:
        st.error(f"Error processing candidate: {c}")
        st.write(e)

# ----------------------------
# DataFrame
# ----------------------------
df = pd.DataFrame(results)

# Sort safely
if not df.empty:
    df = df.sort_values(by="Final Score", ascending=False)

# ----------------------------
# Output UI
# ----------------------------
st.subheader("🏆 Ranked Candidates")

if not df.empty:
    st.dataframe(df)

    st.subheader("📊 Top 5 Candidates")
    st.bar_chart(df.head(5).set_index("Candidate ID")["Final Score"])
else:
    st.error("No candidates found or processing failed. Check JSON structure.")