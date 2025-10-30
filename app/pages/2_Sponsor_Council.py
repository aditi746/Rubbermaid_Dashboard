import streamlit as st
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
def save_df(df, name): df.to_csv(DATA_DIR / name, index=False)

st.title("Sponsor Council — Decisions & Escalations")
teams = pd.read_csv(DATA_DIR / "teams.csv")
decisions = pd.read_csv(DATA_DIR / "decisions.csv")
escalations = pd.read_csv(DATA_DIR / "escalations.csv")

st.subheader("Log a Decision")
with st.form("decision_form"):
    date = st.date_input("Date")
    team = st.selectbox("Team", teams['team_name'], key="team_sel")
    team_id = teams.loc[teams['team_name']==team,'team_id'].iloc[0]
    decision = st.text_area("Decision / Guidance")
    sla = st.number_input("SLA (days)", min_value=1, value=5)
    resolved = st.number_input("Resolved in (days)", min_value=0, value=3)
    dtype = st.selectbox("Type", ["Approval","Unblock","Fast-Track","Review","Other"])
    submit_dec = st.form_submit_button("Save Decision")
    if submit_dec:
        decisions = pd.concat([decisions, pd.DataFrame([{
            "date":str(date),"team_id":team_id,"decision":decision,
            "sla_days":sla,"resolved_days":resolved,"type":dtype
        }])], ignore_index=True)
        save_df(decisions, "decisions.csv")
        st.success("Decision saved.")

st.subheader("Escalation Log")
with st.form("esc_form"):
    date2 = st.date_input("Date ", key="d2")
    team2 = st.selectbox("Team ", teams['team_name'], key="team2")
    team2_id = teams.loc[teams['team_name']==team2,'team_id'].iloc[0]
    issue = st.text_input("Issue")
    owner = st.text_input("Owner (function)")
    status = st.selectbox("Status", ["Open","Closed"])
    res_days = st.number_input("Resolution days", min_value=0, value=0)
    submit_esc = st.form_submit_button("Save Escalation")
    if submit_esc:
        escalations = pd.concat([escalations, pd.DataFrame([{
            "date":str(date2),"team_id":team2_id,"issue":issue,"owner":owner,
            "status":status,"resolution_days":None if res_days==0 else res_days
        }])], ignore_index=True)
        save_df(escalations, "escalations.csv")
        st.success("Escalation saved.")
