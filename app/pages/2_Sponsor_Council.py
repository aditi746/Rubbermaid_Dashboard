import streamlit as st, pandas as pd
from pathlib import Path
DATA = Path(__file__).resolve().parents[2] / "data"
def save(df,name): df.to_csv(DATA/name, index=False)

st.title("Sponsor Council — Decisions & Escalations")
teams = pd.read_csv(DATA/"teams.csv")
decisions = pd.read_csv(DATA/"decisions.csv")
escalations = pd.read_csv(DATA/"escalations.csv")

st.subheader("Log Decision")
with st.form("dec"):
    date = st.date_input("Date")
    team = st.selectbox("Team", teams['team_name'])
    tid = teams.loc[teams['team_name']==team,'team_id'].iloc[0]
    decision = st.text_area("Decision / Guidance")
    sla = st.number_input("SLA (days)", min_value=1, value=5)
    resolved = st.number_input("Resolved in (days)", min_value=0, value=3)
    dtype = st.selectbox("Type", ["Approval","Unblock","Fast-Track","Review","Other"])
    if st.form_submit_button("Save Decision"):
        decisions.loc[len(decisions)] = [str(date), tid, decision, sla, resolved, dtype]
        save(decisions, "decisions.csv"); st.success("Saved.")

st.subheader("Escalation Log")
with st.form("esc"):
    date2 = st.date_input("Date ", key="d2")
    team2 = st.selectbox("Team ", teams['team_name'], key="t2")
    tid2 = teams.loc[teams['team_name']==team2,'team_id'].iloc[0]
    issue = st.text_input("Issue")
    owner = st.text_input("Owner (function)")
    status = st.selectbox("Status", ["Open","Closed"])
    res_days = st.number_input("Resolution days", min_value=0, value=0)
    if st.form_submit_button("Save Escalation"):
        escalations.loc[len(escalations)] = [str(date2), tid2, issue, owner, status, (None if res_days==0 else res_days)]
        save(escalations, "escalations.csv"); st.success("Saved.")
