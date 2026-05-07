import streamlit as st
import time

st.set_page_config(page_title="LearnTrack 8-12", layout="wide")

if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

st.sidebar.title("Academic Progress")
level = (st.session_state.xp // 100) + 1
st.sidebar.write(f"Current Level: {level}")
st.sidebar.progress(min((st.session_state.xp % 100) / 100, 1.0))
st.sidebar.caption(f"{100 - (st.session_state.xp % 100)} XP until next level")

page = st.sidebar.radio("Navigation", ["Dashboard", "Task Manager", "Study Timer", "Grade Predictor"])

if page == "Dashboard":
    st.title("Student Dashboard")

    quotes = [
        "Mind and Hand: Learning by doing.",
        "Grit is passion and perseverance for long-term goals.",
        "The best way to predict the future is to invent it.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "The only way to do great work is to love what you do."
    ]
    st.write(f"*\"{random.choice(quotes)}\"*")

    st.write("---")
    st.write(f"Total XP Earned: {st.session_state.xp}")
    st.write("---")
    st.write("Academic Overview")
    st.info("Use the sidebar to navigate between your tasks, study timer, and grade predictor.")

elif page == "Task Manager":
    st.title("Daily Tasks")
    new_task = st.text_input("Enter a new task")
    if st.button("Add Task"):
        if new_task:
            st.session_state.tasks.append({"task": new_task, "done": False})

    if st.button("Clear Completed Tasks"):
        st.session_state.tasks = [t for t in st.session_state.tasks if not t["done"]]
        st.rerun()

    st.write("---")
    
    for i, task_obj in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([0.1, 0.9])
        is_done = st.checkbox(task_obj["task"], key=f"task_{i}", value=task_obj["done"])
        st.session_state.tasks[i]["done"] = is_done
        if is_done:
            col2.write(f"~~{task_obj['task']}~~")
        else:
            col2.write(task_obj["task"])

elif page == "Study Timer":
    st.title("Focus Timer")
    st.write("Deep work session for focused learning.")
    st.write("---")

    subject = st.selectbox("Select Subject", ["Math", "Science", "Social Studies", "ELA", "French", "Coding"])
    duration = st.number_input("Duration (Minutes)", min_value=1, value=25)

    if st.button("Start Session"):
        st.write(f"Currently focusing on {subject}...")
        bar = st.progress(0)
        for i in range(100):
            time.sleep((duration * 60) / 100)
            bar.progress(i + 1)

        earned_xp = duration * 2
        st.session_state.xp += earned_xp
        st.success(f"Session complete. You have earned {earned_xp} XP.")

elif page == "Grade Predictor":
    st.title("Grade Predictor")
    curr = st.number_input("Current Grade Percentage", 0, 100, 85)
    target = st.number_input("Target Garde Percentage", 0, 100, 90)
    weight = st.number_input("Final Assessment Weight (%)", 0, 100, 30)

    if st.button("Calculate Requirement"):
        needed = (target - (curr * (1 - (weight/100)))) / (weight/100)
        if needed > 100:
            st.error(f"Required Score: {needed:.1f}%. Additional study recommended.")
        else:
            st.success(f"Required Score: {needed:.1f}%")
