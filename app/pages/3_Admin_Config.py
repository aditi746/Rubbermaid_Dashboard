import streamlit as st, pandas as pd
from pathlib import Path
DATA = Path(__file__).resolve().parents[2] / "data"
def save(df,name): df.to_csv(DATA/name, index=False)

st.title("Admin Config — Teams & Ladder Reviews")
teams = pd.read_csv(DATA/"teams.csv"); ladder = pd.read_csv(DATA/"ladder_history.csv")

st.subheader("Teams Registry")
st.dataframe(teams)
with st.form("add_team"):
    st.markdown("**Add / Update Team**")
    team_id = st.text_input("Team ID (short)")
    team_name = st.text_input("Team Name")
    division = st.text_input("Division")
    level = st.selectbox("Current Level", ["L1","L2","L3"])
    notes = st.text_input("Notes")
    if st.form_submit_button("Save"):
        teams = teams[teams['team_id'] != team_id]
        teams.loc[len(teams)] = [team_id, team_name, division, level, notes]
        save(teams, "teams.csv"); st.success("Saved.")

st.subheader("Quarterly Ladder Review")
with st.form("ladder_form"):
    quarter = st.text_input("Quarter (e.g., 2025Q2)", value="2025Q2")
    team = st.selectbox("Team", teams['team_name'])
    tid = teams.loc[teams['team_name']==team,'team_id'].iloc[0]
    level = st.selectbox("Level Achieved", ["L1","L2","L3"])
    if st.form_submit_button("Record Review"):
        ladder.loc[len(ladder)] = [quarter, tid, level]
        save(ladder, "ladder_history.csv")
        teams.loc[teams['team_id']==tid,'level'] = level; save(teams, "teams.csv")
        st.success("Saved & team level updated.")
