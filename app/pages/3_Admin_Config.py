import streamlit as st
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
def save_df(df, name): df.to_csv(DATA_DIR / name, index=False)

st.title("Admin Config — Teams & Ladder Reviews")
teams = pd.read_csv(DATA_DIR / "teams.csv")
ladder = pd.read_csv(DATA_DIR / "ladder_history.csv")

st.subheader("Teams Registry")
st.dataframe(teams)
with st.form("add_team"):
    st.markdown("**Add / Update Team**")
    team_id = st.text_input("Team ID (short code)")
    team_name = st.text_input("Team Name")
    division = st.text_input("Division")
    level = st.selectbox("Current Level", ["L1","L2","L3"])
    notes = st.text_input("Notes")
    submit = st.form_submit_button("Save")
    if submit and team_id and team_name:
        teams = teams[teams['team_id'] != team_id]
        teams = pd.concat([teams, pd.DataFrame([{
            "team_id":team_id,"team_name":team_name,"division":division,"level":level,"notes":notes
        }])], ignore_index=True)
        save_df(teams, "teams.csv")
        st.success("Team saved.")

st.subheader("Quarterly Ladder Review")
with st.form("ladder_form"):
    quarter = st.text_input("Quarter (e.g., 2025Q2)", value="2025Q2")
    team = st.selectbox("Team", teams['team_name'])
    team_id = teams.loc[teams['team_name']==team,'team_id'].iloc[0]
    level = st.selectbox("Level Achieved", ["L1","L2","L3"])
    submit2 = st.form_submit_button("Record Review")
    if submit2:
        ladder = pd.concat([ladder, pd.DataFrame([{
            "quarter":quarter,"team_id":team_id,"level":level
        }])], ignore_index=True)
        save_df(ladder, "ladder_history.csv")
        teams.loc[teams['team_id']==team_id,'level'] = level
        save_df(teams, "teams.csv")
        st.success("Ladder review saved and team level updated.")
