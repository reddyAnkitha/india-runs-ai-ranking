import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Candidate Ranking System", layout="centered")

st.title("AI Candidate Ranking System")

job_desc = st.text_area("Enter Job Description")

if st.button("Rank Candidates"):

    if not job_desc:
        st.warning("Please enter job description")
    else:
        try:
            # 🔥 FIX: correct API call
            response = requests.post(
                "http://127.0.0.1:8000/rank",
                json={"job_description": job_desc}
            )

            # 🔥 FIX: prevent JSON error
            if response.status_code != 200:
                st.error("Backend Error")
                st.write(response.text)
            else:
                data = response.json()

                df = pd.DataFrame(data)

                st.subheader("Top 10 Candidates")
                st.dataframe(df)

                # =========================
                # 📊 BAR CHART FIX (IMPORTANT)
                # =========================
                st.subheader("Match Percentage Chart")

                fig, ax = plt.subplots()

                ax.bar(df["candidate_id"], df["match_percentage"], color="skyblue")

                ax.set_xlabel("Candidate ID")
                ax.set_ylabel("Match %")

                plt.xticks(rotation=90)

                st.pyplot(fig)

                # =========================
                # 📥 DOWNLOAD CSV
                # =========================
                csv = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "Download Results",
                    csv,
                    "ranked_candidates.csv",
                    "text/csv"
                )

        except Exception as e:
            st.error(f"Connection Error: {e}")