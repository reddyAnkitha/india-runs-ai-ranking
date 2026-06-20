import streamlit as st
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="AI Candidate Ranking System", layout="wide")

st.title("🚀 AI-Powered Candidate Ranking System")
st.write("Hybrid AI model using Semantic + Skill + Experience scoring")

# ----------------------------
# MODEL (cached)
# ----------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ----------------------------
# LOAD DATA (relative paths only)
# ----------------------------
with open("data/job_description.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

with open("data/sample_candidates.json", "r", encoding="utf-8") as f:
    candidates = json.load(f)

# ----------------------------
# DEBUG (optional)
# ----------------------------
st.subheader("🔍 Sample Candidate")
st.write(candidates[0])

# ----------------------------
# JOB EMBEDDING (cached)
# ----------------------------
@st.cache_data
def get_embedding(text):
    return model.encode([text])

jd_emb = get_embedding(jd_text)

# ----------------------------
# SCORING LOGIC
# ----------------------------
results = []

for c in candidates:
    try:
        profile = c.get("profile", {})

        headline = profile.get("headline", "")
        summary = profile.get("summary", "")

        candidate_text = headline + " " + summary

        cand_emb = model.encode([candidate_text])

        # Semantic similarity
        semantic_score = cosine_similarity(jd_emb, cand_emb)[0][0]

        # Skill overlap score
        jd_words = set(jd_text.lower().split())
        cand_words = set(candidate_text.lower().split())
        skill_score = len(jd_words & cand_words) / (len(jd_words) + 1)

        # Experience score
        experience = profile.get("years_of_experience", 0)
        exp_score = min(experience / 10, 1)

        # Final score
        final_score = (
            0.5 * semantic_score +
            0.3 * skill_score +
            0.2 * exp_score
        )

        results.append({
            "Candidate ID": c.get("candidate_id", "UNKNOWN"),
            "Semantic Score": round(float(semantic_score), 3),
            "Skill Score": round(skill_score, 3),
            "Experience Score": round(exp_score, 3),
            "Final Score": round(final_score, 3)
        })

    except Exception as e:
        st.error(f"Error processing candidate: {c}")
        st.write(e)

# ----------------------------
# DATAFRAME
# ----------------------------
df = pd.DataFrame(results)

if not df.empty:
    df = df.sort_values(by="Final Score", ascending=False)

# ----------------------------
# OUTPUT
# ----------------------------
st.subheader("🏆 Ranked Candidates")

if not df.empty:
    st.dataframe(df)

    st.subheader("📊 Top 5 Candidates")

    top5 = df.head(5)

    st.bar_chart(top5.set_index("Candidate ID")["Final Score"])
else:
    st.error("No results generated. Check JSON structure or data format.")