import streamlit as st
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
def save_df(df, name): df.to_csv(DATA_DIR / name, index=False)

st.title("Team Dashboard — Monthly Update")
teams = pd.read_csv(DATA_DIR / "teams.csv")
kpis = pd.read_csv(DATA_DIR / "kpis.csv")
surveys = pd.read_csv(DATA_DIR / "surveys.csv")

team = st.selectbox("Select Team", teams['team_name'])
team_id = teams.loc[teams['team_name']==team, 'team_id'].iloc[0]

st.subheader("Update KPIs")
with st.form("kpi_form"):
    month = st.text_input("Month (YYYY-MM)", value="2025-10")
    on_time = st.slider("On-Time %", 0.0, 1.0, 0.85, 0.01)
    cycle = st.slider("Cycle Time Δ (negative is better)", -1.0, 1.0, -0.10, 0.01)
    autonomy = st.slider("Autonomy Index", 0.0, 1.0, 0.60, 0.01)
    sponsor_delta = st.slider("Sponsor Meeting Δ (negative is better)", -1.0, 1.0, -0.10, 0.01)
    innovation = st.slider("Innovation Hit %", 0.0, 1.0, 0.50, 0.01)
    health = st.slider("Team Health", 0.0, 1.0, 0.75, 0.01)
    submitted = st.form_submit_button("Save KPIs")
    if submitted:
        kpis = pd.concat([kpis, pd.DataFrame([{
            "month":month,"team_id":team_id,"on_time_pct":on_time,"cycle_time_delta":cycle,
            "autonomy_index":autonomy,"sponsor_meeting_delta":sponsor_delta,
            "innovation_hit_rate":innovation,"team_health":health
        }])], ignore_index=True)
        save_df(kpis, "kpis.csv")
        st.success("KPIs saved.")

st.subheader("2-Way Feedback (Team & Sponsor)")
with st.form("survey_form"):
    month2 = st.text_input("Survey Month (YYYY-MM)", value="2025-10")
    role = st.slider("Role Clarity (1–10)", 1.0, 10.0, 8.0, 0.1)
    decision = st.slider("Decision Clarity (1–10)", 1.0, 10.0, 8.0, 0.1)
    psych = st.slider("Psychological Safety (1–10)", 1.0, 10.0, 8.0, 0.1)
    sponsor_sup = st.slider("Sponsor Support (1–10)", 1.0, 10.0, 8.0, 0.1)
    sponsor_view = st.slider("Sponsor View of Team (1–10)", 1.0, 10.0, 8.0, 0.1)
    submitted2 = st.form_submit_button("Save Survey")
    if submitted2:
        surveys = pd.concat([surveys, pd.DataFrame([{
            "month":month2,"team_id":team_id,"role_clarity":role,"decision_clarity":decision,
            "psych_safety":psych,"sponsor_support":sponsor_sup,"sponsor_view_of_team":sponsor_view
        }])], ignore_index=True)
        save_df(surveys, "surveys.csv")
        st.success("Survey saved.")
