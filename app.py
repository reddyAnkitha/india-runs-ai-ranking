import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Candidate Ranking System")

st.title("AI Candidate Ranking System")

job_description = st.text_area("Enter Job Description")

if st.button("Rank Candidates"):

    if job_description.strip() == "":
        st.warning("Please enter job description")
    else:
        response = requests.post(
            "http://127.0.0.1:8000/rank",
            json={"job_description": job_description}
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Top 10 Candidates")

            df = pd.DataFrame(data)
            df["match_percentage"] = df["score"] * 100

            st.dataframe(df)

            # BAR CHART
            st.subheader("Match Percentage Chart")

            fig, ax = plt.subplots()
            ax.bar(df["candidate_id"], df["match_percentage"])
            plt.xticks(rotation=90)

            st.pyplot(fig)

            # DOWNLOAD CSV
            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download CSV",
                csv,
                "candidates.csv",
                "text/csv"
            )

        else:
            st.error("Backend API error")