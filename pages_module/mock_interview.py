"""
Mock Interview Simulator page
"""
import streamlit as st
import random
from datetime import datetime, date
from db.database import (
    add_mock_interview,
    get_mock_interviews,
    delete_mock_interview,
    log_progress,
    add_badge,
    get_user
)
from data.questions import DSA_TOPICS
from utils.styles import inject_css

def show_mock_interview():
    inject_css()
    uid = st.session_state.user["id"]
    
    st.markdown("""
    <h1>🎯 Mock Interview Simulator</h1>
    <p style="color:#94a3b8;">Practice interview questions, record your sessions, and track your progress!</p>
    """, unsafe_allow_html=True)
    
    # Random question generator
    st.markdown("### 🎲 Random Question Generator")
    
    companies = ["Google", "Meta", "Amazon", "Apple", "Netflix", "Microsoft", "Stripe"]
    roles = ["Software Engineer", "Senior SWE", "Backend Engineer", "Frontend Engineer", "Full Stack"]
    
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_company = st.selectbox("Target Company", companies)
    with col2:
        selected_role = st.selectbox("Role", roles)
    
    topic_list = list(DSA_TOPICS.keys())
    selected_topic = st.selectbox("Topic", ["Random"] + topic_list)
    
    if st.button("🎲 Generate Random Question", use_container_width=True):
        if selected_topic == "Random":
            random_topic = random.choice(topic_list)
        else:
            random_topic = selected_topic
        questions = DSA_TOPICS.get(random_topic, [])
        if questions:
            random_question = random.choice(questions)
            st.session_state.random_question = random_question
            st.session_state.random_topic = random_topic
            st.rerun()
    
    if "random_question" in st.session_state:
        q = st.session_state.random_question
        topic = st.session_state.random_topic
        st.markdown(f"""
        <div class="card card-blue">
            <h4 style="margin-top:0;">📝 {q['title']}</h4>
            <p style="color:#94a3b8; font-size:0.9rem;">
                <span style="display:inline-block; padding:2px 8px; border-radius:4px; background:{
                    '#10b981' if q['difficulty'] == 'Easy' else '#f59e0b' if q['difficulty'] == 'Medium' else '#ef4444'
                }; color:white; font-size:0.8rem; margin-right:8px;">{q['difficulty']}</span>
                Topic: {topic}
            </p>
            <p style="color:#f1f5f9;">{q.get('description', 'No description available')}</p>
            <div style="margin-top:8px;">
                <a href="{q['link']}" target="_blank" style="display:inline-block; padding:6px 12px; background:#6366f1; color:white; border-radius:6px; text-decoration:none; margin-right:8px;">🔗 View Problem</a>
                {"📹 " + q.get('solution', '') if q.get('solution') else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Record mock interview
    st.markdown("<br>### 📝 Record Mock Interview Session", unsafe_allow_html=True)
    with st.form("mock_interview_form"):
        company_input = st.text_input("Company", value=selected_company if 'selected_company' in locals() else "")
        role_input = st.text_input("Role", value=selected_role if 'selected_role' in locals() else "")
        date_input = st.date_input("Interview Date", value=date.today())
        duration_input = st.number_input("Duration (minutes)", min_value=15, max_value=180, value=45)
        score_input = st.slider("Score (1-10)", 1, 10, 7)
        feedback_input = st.text_area("Feedback & Notes", placeholder="What went well? What could be improved?")
        
        if st.form_submit_button("Save Interview Session", use_container_width=True):
            add_mock_interview(uid, company_input, role_input, str(date_input), duration_input, feedback_input, score_input)
            log_progress(uid, str(date.today()), "mock_interview")
            
            # Check and award badge if needed
            user = get_user(uid)
            import json
            current_badges = set(json.loads(user.get('badges', '[]')))
            if 'mock_interviewer' not in current_badges:
                add_badge(uid, 'mock_interviewer')
                st.balloons()
            
            st.success("Mock interview session saved!")
            st.rerun()
    
    # Past interviews
    st.markdown("<br>### 📊 Past Interview Sessions", unsafe_allow_html=True)
    past_interviews = get_mock_interviews(uid)
    if past_interviews:
        for interview in past_interviews:
            with st.expander(f"{interview['company']} - {interview['role']} ({interview['date']})", expanded=False):
                st.markdown(f"""
                <div style="display:flex; gap:10px; align-items:center; margin-bottom:10px;">
                    <span style="font-size:1.2rem;">⭐</span>
                    <strong>Score: {interview['score']}/10</strong>
                    <span style="color:#94a3b8;">• {interview['duration_minutes']} minutes</span>
                </div>
                """, unsafe_allow_html=True)
                if interview['feedback']:
                    st.markdown("**Feedback:**")
                    st.info(interview['feedback'])
                if st.button("Delete Session", key=f"del_interview_{interview['id']}"):
                    delete_mock_interview(interview['id'])
                    st.success("Session deleted!")
                    st.rerun()
    else:
        st.info("No mock interview sessions recorded yet!")
