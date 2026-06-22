import os
import json
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Candidate Ranking System",
    layout="wide"
)

st.title("🚀 AI-Powered Candidate Ranking System")
st.write("Hybrid AI model using Semantic + Skill + Experience scoring")

# --------------------------------------------------
# MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-mpnet-base-v2")

model = load_model()

# --------------------------------------------------
# PATHS
# --------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

JD_PATH = os.path.join(BASE_DIR, "data", "job_description.txt")
CANDIDATES_PATH = os.path.join(BASE_DIR, "data", "sample_candidates.json")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
try:
    with open(JD_PATH, "r", encoding="utf-8") as f:
        jd_text = f.read()

    with open(CANDIDATES_PATH, "r", encoding="utf-8") as f:
        candidates = json.load(f)

except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

# --------------------------------------------------
# SKILLS SET
# --------------------------------------------------
jd_skills = {
    "python", "langchain", "faiss", "pinecone",
    "embeddings", "llm", "rag", "streamlit",
    "sql", "aws", "transformers", "machine learning"
}

# --------------------------------------------------
# EXPLANATION
# --------------------------------------------------
def explain_rank(profile, semantic_score, final_score, matched_skills):

    explanation = []

    if semantic_score >= 0.75:
        explanation.append("Strong semantic similarity.")
    elif semantic_score >= 0.55:
        explanation.append("Moderate semantic similarity.")
    else:
        explanation.append("Low semantic similarity.")

    skill_count = len(matched_skills)

    if skill_count >= 8:
        explanation.append(f"Excellent skill overlap ({skill_count}).")
    elif skill_count >= 5:
        explanation.append(f"Good skill overlap ({skill_count}).")
    else:
        explanation.append(f"Limited skill overlap ({skill_count}).")

    exp = profile.get("years_of_experience", 0)

    if exp >= 8:
        explanation.append(f"Senior experience ({exp} yrs).")
    elif exp >= 4:
        explanation.append(f"Mid-level experience ({exp} yrs).")
    else:
        explanation.append(f"Junior experience ({exp} yrs).")

    if final_score >= 0.75:
        explanation.append("Excellent candidate fit.")
    elif final_score >= 0.60:
        explanation.append("Strong candidate fit.")
    elif final_score >= 0.50:
        explanation.append("Good candidate fit.")
    else:
        explanation.append("Moderate candidate fit.")

    return " | ".join(explanation)

# --------------------------------------------------
# EMBEDDINGS
# --------------------------------------------------
jd_embedding = model.encode([jd_text])

results = []

# --------------------------------------------------
# RANKING ENGINE
# --------------------------------------------------
for candidate in candidates:

    profile = candidate.get("profile", {})

    candidate_skills = set()

    for skill in candidate.get("skills", []):
        if isinstance(skill, dict):
            candidate_skills.add(skill.get("name", "").lower())
        else:
            candidate_skills.add(skill.lower())

    candidate_text = (
        profile.get("headline", "") + " " +
        profile.get("summary", "") + " " +
        " ".join(candidate_skills)
    )

    candidate_embedding = model.encode([candidate_text])

    semantic_score = float(
        cosine_similarity(jd_embedding, candidate_embedding)[0][0]
    )

    matched_skills = sorted(jd_skills.intersection(candidate_skills))

    skill_score = len(matched_skills) / len(jd_skills)

    exp_years = profile.get("years_of_experience", 0)
    exp_score = min(exp_years / 10, 1)

    final_score = (
        0.60 * semantic_score +
        0.40 * skill_score +
        0.10 * exp_score
    )

    explanation = explain_rank(
        profile,
        semantic_score,
        final_score,
        matched_skills
    )

    results.append({
        "Candidate ID": candidate.get("candidate_id"),
        "Semantic Score": round(semantic_score, 3),
        "Skill Score": round(skill_score, 3),
        "Experience Score": round(exp_score, 3),
        "Final Score": round(final_score, 3),
        "Matched Skills": ", ".join(matched_skills),
        "Why This Rank": explanation
    })

# --------------------------------------------------
# DATAFRAME
# --------------------------------------------------
df = pd.DataFrame(results)

if not df.empty:
    df = df.sort_values(by="Final Score", ascending=False)

# --------------------------------------------------
# SEARCH
# --------------------------------------------------
st.sidebar.header("🔍 Search Candidate")
search_id = st.sidebar.text_input("Enter Candidate ID")

if search_id:
    filtered_df = df[df["Candidate ID"].str.contains(search_id, case=False, na=False)]
else:
    filtered_df = df

# --------------------------------------------------
# METRICS
# --------------------------------------------------
if not df.empty:
    c1, c2 = st.columns(2)
    c1.metric("Total Candidates", len(df))
    c2.metric("Top Score", round(df.iloc[0]["Final Score"], 3))

# --------------------------------------------------
# TABLE
# --------------------------------------------------
st.subheader("🏆 Ranked Candidates")
st.dataframe(filtered_df, use_container_width=True)

# --------------------------------------------------
# TOP 5 CHART
# --------------------------------------------------
if not df.empty:
    st.subheader("📊 Top 5 Candidates")
    st.bar_chart(df.head(5).set_index("Candidate ID")["Final Score"])

# --------------------------------------------------
# TOP CANDIDATE
# --------------------------------------------------
if not df.empty:

    top = df.iloc[0]

    st.subheader("🧠 Top Candidate Analysis")

    st.success(top["Why This Rank"])

    if top["Final Score"] >= 0.75:
        st.success("✅ Highly Recommended")
    elif top["Final Score"] >= 0.50:
        st.info("👍 Recommended")
    else:
        st.warning("⚠️ Needs Review")

    st.write("### Matching Skills")
    st.info(top["Matched Skills"])

    st.write("### Score Breakdown")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Semantic", f"{top['Semantic Score']:.3f}")
    c2.metric("Skill", f"{top['Skill Score']:.3f}")
    c3.metric("Experience", f"{top['Experience Score']:.3f}")
    c4.metric("Final", f"{top['Final Score']:.3f}")

    st.write("### Progress")

    st.progress(float(top["Semantic Score"]))
    st.progress(float(top["Skill Score"]))
    st.progress(float(top["Experience Score"]))
    st.progress(float(top["Final Score"]))

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------
st.download_button(
    "📥 Download CSV",
    df.to_csv(index=False),
    "candidate_rankings.csv",
    "text/csv"
)