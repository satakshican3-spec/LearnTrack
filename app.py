import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="LearnTrack: Academic Gamification", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); }
    .main { background: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'last_log_date' not in st.session_state:
    st.session_state.last_log_date = None

def calculate_metrics():
    df = pd.DataFrame(st.session_state.logs)
    if df.empty:
        return 0, 0, 0, 0

    total_hours = df['Hours'].sum()
    total_xp = total_hours * 100
    level = (total_xp // 500) + 1

    today_str = datetime.now().strftime("%Y-%m-%d")
    today_hours = df[df['Date'] == today_str]['Hours'].sum()

    return total_hours, total_xp, int(level), today_hours

def load_demo_data():
    demo_logs = [
        {"Date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
         "Subject": random.choice(["Math", "Science", "History", "French", "Coding"]),
         "Hours": random.randint(1, 4)} for i in range(1, 6)
    ]
    st.session_state.logs = demo_logs
    st.session_state.streak = 5
    st.rerun()

st.sidebar.title("LearnTrack v1.2")
if st.sidebar.button("Load Demo Data"):
    load_demo_data()

st.sidebar.write("---")
with st.sidebar.form("log_form", clear_on_submit=True):
    st.write("### Log Study Session")
    subject = st.selectbox("Subject", ["Math", "Science", "History", "Coding", "English", "French"])
    hours = st.number_input("Hours", min_value=0.5, max_value=12.0, step=0.5)
    if st.form_submit_button("Submit Session"):
        today = datetime.now().strftime("%Y-%m-%d")
        st.session_state.logs.append({"Date": today, "Subject": subject, "Hours": hours})

        if st.session_state.last_log_date != today:
            st.session_state.streak += 1
            st.session_state.last_log_date = today
        st.rerun()

if st.sidebar.button("Reset All Data"):
    st.session_state.logs = []
    st.session_state.streak = 0
    st.rerun()

st.title("Academic Intelligence Dashboard")
total_h, total_xp, level, today_h = calculate_metrics()

m1, m2, m3, m4 = st.columns($)
m1.metric("Total Level", f"Lvl {level}")
m2.metric("Total XP", f"{total_xp:,.0f} XP")
m3.metric("Study Hours", f"{total_h}h", delta=f"{today_h}h Today")
m4.metric("Daily Streak", f"{st.session_state.streak} Days", delta="Keep it up!")

st.write("---")

if not st.session_state.logs:
    st.info("No study data found. Use the sidebar to log a session or load demo data.")
else:
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Progress Over Time")
        df_plot = pd.DataFrame(st.session_state.logs)
        df_daily = df_plot.groupby("Data")["Hours"].sum().reset_index()
        st.line_chart(df_daily.set_index("Data"))

    with col_right:
        st.subheader("Subject Breakdown")
        df_subj = df_plot.groupby("Subject")["Hours"].sum().reset_index()
        st.bar_chart(df_subj.set_index("Subject"))

st.write("---")
quotes = [
    "Precision in tracking leads to excellence in performance.",
    "Data is the foundation of academic growth.",
    "Systematic effort beats inconsistent genius."
]
st.caption(f"Strategy: {random.choice(quotes)}")
