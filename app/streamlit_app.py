import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

@st.cache_data
def load_data():
    teams = pd.read_csv(DATA_DIR / "teams.csv")
    ladder = pd.read_csv(DATA_DIR / "ladder_history.csv")
    kpis = pd.read_csv(DATA_DIR / "kpis.csv")
    decisions = pd.read_csv(DATA_DIR / "decisions.csv")
    escalations = pd.read_csv(DATA_DIR / "escalations.csv")
    surveys = pd.read_csv(DATA_DIR / "surveys.csv")
    return teams, ladder, kpis, decisions, escalations, surveys

st.set_page_config(page_title="RLOS Dashboard", layout="wide")
teams, ladder, kpis, decisions, escalations, surveys = load_data()
st.title("Rubbermaid Leadership Operating System (RLOS) — Dashboard")

# ===== System Health Snapshot
st.subheader("System Health Snapshot")
col1, col2, col3, col4 = st.columns(4)
pct_l2 = (teams['level'].isin(['L2','L3']).mean()*100)
col1.metric("% Teams at Level 2+", f"{pct_l2:.0f}%")
decisions['met_sla'] = decisions['resolved_days'] <= decisions['sla_days']
sla_pct = (decisions['met_sla'].mean()*100 if len(decisions)>0 else 0)
col2.metric("Sponsor SLA Met", f"{sla_pct:.0f}%")
avg_health = (kpis['team_health'].mean()*100) if len(kpis)>0 else 0
col3.metric("Avg Team Health", f"{avg_health:.0f}%")
avg_resolve = decisions['resolved_days'].mean() if len(decisions)>0 else 0
col4.metric("Avg Decision Time (days)", f"{avg_resolve:.1f}")

st.divider()

# ===== Ladder Progress
st.subheader("Empowerment Ladder Progress")
ladder_pivot = ladder.pivot_table(index='team_id', columns='quarter', values='level', aggfunc='first')
st.dataframe(ladder_pivot)

# ===== Latest KPIs by Team
st.subheader("Key KPIs by Team (latest month)")
latest = kpis.sort_values('month').groupby('team_id').tail(1).merge(teams[['team_id','team_name','level']], on='team_id', how='left')
latest_display = latest[['team_name','level','on_time_pct','cycle_time_delta','autonomy_index','sponsor_meeting_delta','innovation_hit_rate','team_health']].rename(columns={
    'team_name':'Team','level':'Level','on_time_pct':'On-Time %',
    'cycle_time_delta':'Cycle Δ','autonomy_index':'Autonomy','sponsor_meeting_delta':'Sponsor Mtgs Δ',
    'innovation_hit_rate':'Innovation Hit %','team_health':'Team Health'
})
st.dataframe(latest_display.style.format({
    'On-Time %':'{:.0%}','Cycle Δ':'{:.0%}','Autonomy':'{:.0%}','Sponsor Mtgs Δ':'{:+.0%}',
    'Innovation Hit %':'{:.0%}','Team Health':'{:.0%}'
}))

# ===== Chart: On-time vs Autonomy
st.subheader("On-Time Delivery vs Autonomy Index")
chart = alt.Chart(latest).mark_circle(size=180).encode(
    x=alt.X('on_time_pct:Q', axis=alt.Axis(format='%'), title='On-Time Delivery'),
    y=alt.Y('autonomy_index:Q', axis=alt.Axis(format='%'), title='Autonomy Index'),
    color='level:N',
    tooltip=['team_id','on_time_pct','autonomy_index','team_health']
).properties(height=350)
st.altair_chart(chart, use_container_width=True)

# ===== Escalations & Resolution
st.subheader("Escalations & Resolution")
st.dataframe(escalations)

st.info("Use sidebar pages: Team Dashboard (updates), Sponsor Council (decisions), Admin Config (levels).")
