import streamlit as st, pandas as pd
from pathlib import Path
DATA = Path(__file__).resolve().parents[2] / "data"
def save(df,name): df.to_csv(DATA/name, index=False)

st.title("Team Dashboard — Monthly Update")
teams = pd.read_csv(DATA/"teams.csv")
kpis = pd.read_csv(DATA/"kpis.csv"); surveys = pd.read_csv(DATA/"surveys.csv")

team = st.selectbox("Team", teams['team_name'])
tid = teams.loc[teams['team_name']==team,'team_id'].iloc[0]

st.subheader("Update KPIs")
with st.form("kpis"):
    month = st.text_input("Month (YYYY-MM)", value="2025-10")
    on_time = st.slider("On-Time %", 0.0, 1.0, 0.85, 0.01)
    cycle = st.slider("Cycle Time Δ (negative is better)", -1.0, 1.0, -0.10, 0.01)
    autonomy = st.slider("Autonomy Index", 0.0, 1.0, 0.60, 0.01)
    sponsor_delta = st.slider("Sponsor Meeting Δ (negative is better)", -1.0, 1.0, -0.10, 0.01)
    innovation = st.slider("Innovation Hit %", 0.0, 1.0, 0.50, 0.01)
    health = st.slider("Team Health", 0.0, 1.0, 0.75, 0.01)
    if st.form_submit_button("Save KPIs"):
        kpis.loc[len(kpis)] = [month, tid, on_time, cycle, autonomy, sponsor_delta, innovation, health]
        save(kpis, "kpis.csv"); st.success("Saved.")

st.subheader("2-Way Feedback (Team & Sponsor)")
with st.form("survey"):
    month2 = st.text_input("Survey Month (YYYY-MM)", value="2025-10")
    role = st.slider("Role Clarity (1–10)", 1.0, 10.0, 8.0, 0.1)
    decision = st.slider("Decision Clarity (1–10)", 1.0, 10.0, 8.0, 0.1)
    psych = st.slider("Psych Safety (1–10)", 1.0, 10.0, 8.0, 0.1)
    sponsor_sup = st.slider("Sponsor Support (1–10)", 1.0, 10.0, 8.0, 0.1)
    sponsor_view = st.slider("Sponsor View of Team (1–10)", 1.0, 10.0, 8.0, 0.1)
    if st.form_submit_button("Save Survey"):
        surveys.loc[len(surveys)] = [month2, tid, role, decision, psych, sponsor_sup, sponsor_view]
        save(surveys, "surveys.csv"); st.success("Saved.")
