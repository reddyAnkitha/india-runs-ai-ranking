# 🚀 AI-Powered Candidate Ranking System (INDIA.RUNS Hackathon)

## 📌 Problem Statement
Recruiters spend huge time manually screening resumes. Keyword-based systems miss context and hidden talent.

## 💡 Solution
We built an AI system that ranks candidates using:

- Semantic similarity (SentenceTransformers)
- Skill matching
- Experience scoring
- Hybrid weighted ranking model

## ⚙️ Tech Stack
- Python
- FastAPI
- Streamlit
- SentenceTransformers
- Pandas, NumPy

## 🧠 Workflow
1. Job Description Input
2. Candidate Dataset Loading
3. Text Embeddings
4. Similarity Calculation
5. Skill Matching
6. Final Weighted Score
7. Ranked Output

## 📊 Scoring Formula
Final Score =
0.5 × Semantic Score +
0.3 × Skill Score +
0.2 × Experience Score

## 🚀 How to Run

### Backend
```bash
uvicorn backend.main:app --reload