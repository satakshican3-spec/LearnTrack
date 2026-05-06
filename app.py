import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="LearnTrack 8-12")

st.sidebar.title("LearnTrack 8-12")
page = st.sidebar.radio("Go to:", ["Dashboard", "Study Timer", "Grade Predictor"])

if page == "Dashboard":
  st.title("Your Academic Dashboard")
  st.write("Target: MIT Class of 2031")

  if 'total_study_time' not in st.session_state:
      st.session_state.total_study_time = 0

  st.metric("Minutes Studied This Session", f"{st.session_state.total_study_time} mins")
  st.info("Tip: Consistency is key for Grade 8-12 success!")

elif page == "Study Timer":
    st.title("Focus Timer")
    subject = st.selectbox("Subject", ["Math", "Science", "English", "French", "Coding"])
    duration = st.number_input("Study Minutes", min_value=1, value=25)

    if st.button("Start Timer"):
        progress_text = st.empty()
        bar = st.progress(0)
        for i in range(100):
            time.sleep((duration * 60) / 100)
            bar.progress(i + 1)
            progress_text.text(f"Studying {subject}: {100-i}% remaining")

        st.session_state.total_study_time += duration
        st.balloons()
        st.success(f"Great job! You logged {duration} minutes of {subject}.")

elif page == "Grade Predictor":
    st.title("Grade Predictor")
    st.write("Know exactly what you need on your next test.")

    curr_grade = st.number_input("Current Grade (%)", 0, 100, 85)
    target_grade = st.number_input("Target Final Grade (%)", 0, 100, 90)
    final_weight = st.number_input("Final Exam Weight (%)", 0, 100, 30)

    if st.button("Calculate Needed Score"):
        needed = (target_grade - (curr_grade * (1 - (final_weight/100)))) / (final_weight/100)

        if needed > 100:
            st.error(f"You need a {needed:.1f}%... that's a tough climb!")
        else:
            st.success(f"To hit {target_grade}%, you need a {needed:.1f}% on the final.")
