"""
Study Schedule/Planner page
"""
import streamlit as st
from datetime import datetime, date
from db.database import (
    add_schedule_task,
    get_schedule_tasks,
    update_schedule_task,
    delete_schedule_task,
    log_progress,
    add_badge,
    get_user
)
from utils.styles import inject_css

def show_study_planner():
    inject_css()
    uid = st.session_state.user["id"]
    
    st.markdown("""
    <h1>📅 Study Planner & Schedule</h1>
    <p style="color:#94a3b8;">Organize your study sessions, track tasks, and stay on top of your prep goals!</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ➕ Add New Task")
        task_date = st.date_input("Task Date", value=date.today())
        task_text = st.text_area("Task Description", placeholder="e.g., Solve 2 LeetCode medium problems, Study DP patterns")
        priority = st.selectbox("Priority", ["low", "medium", "high"])
        
        if st.button("Add Task", use_container_width=True):
            if task_text:
                add_schedule_task(uid, str(task_date), task_text, priority)
                log_progress(uid, str(date.today()), "study_schedule")
                
                # Check and award badge if needed
                user = get_user(uid)
                import json
                current_badges = set(json.loads(user.get('badges', '[]')))
                if 'study_planner' not in current_badges:
                    add_badge(uid, 'study_planner')
                    st.balloons()
                
                st.success("Task added successfully!")
                st.rerun()
            else:
                st.error("Please enter a task description.")
    
    with col2:
        st.markdown("### 📋 Your Schedule")
        view_date = st.date_input("View Schedule For", value=date.today())
        
        tasks = get_schedule_tasks(uid, str(view_date))
        
        if tasks:
            for task in tasks:
                priority_color = {"low": "#818cf8", "medium": "#f59e0b", "high": "#ef4444"}.get(task["priority"], "#94a3b8")
                
                with st.expander(f"{task['task'][:60]}{'...' if len(task['task'])>60 else ''}", expanded=True):
                    st.markdown(f"""
                    <div style="display:flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.8rem; color:{priority_color}; font-weight: bold;">{task['priority'].upper()} Priority</span>
                        <span style="font-size: 0.8rem; color:#94a3b8;">Created: {task['created_at'].split('T')[0]}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"**Task:** {task['task']}")
                    
                    col_a, col_b, col_c = st.columns([1,1,1])
                    
                    with col_a:
                        if st.checkbox("Completed", value=bool(task["completed"]), key=f"chk_{task['id']}"):
                            update_schedule_task(task["id"], completed=1)
                        else:
                            update_schedule_task(task["id"], completed=0)
                    
                    with col_b:
                        if st.button("Delete", key=f"del_{task['id']}", use_container_width=True):
                            delete_schedule_task(task["id"])
                            st.success("Task deleted!")
                            st.rerun()
        else:
            st.info("No tasks scheduled for this day!")
    
    # Weekly overview
    st.markdown("<br>### 📊 Weekly Overview", unsafe_allow_html=True)
    all_tasks = get_schedule_tasks(uid)
    
    if all_tasks:
        completed = sum(1 for t in all_tasks if t["completed"])
        total = len(all_tasks)
        progress = completed / total if total > 0 else 0
        st.progress(progress, text=f"Overall Completion: {completed}/{total} tasks completed!")
    else:
        st.info("No tasks added yet!")

