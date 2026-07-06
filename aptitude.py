"""
Aptitude training page — Quantitative, Logical, Verbal, Technical
"""
import streamlit as st
import random
from data.questions import APTITUDE_QUESTIONS
from utils.styles import inject_css
from db.database import log_progress, add_badge
from datetime import date

def show_aptitude():
    inject_css()
    uid = st.session_state.user["id"]

    st.markdown("""
    <h1>🧠 Aptitude Trainer</h1>
    <p style="color:#94a3b8">Practice quantitative, logical, verbal and technical aptitude for FAANG screening rounds.</p>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "apt_score" not in st.session_state:
        st.session_state.apt_score = 0
    if "apt_answered" not in st.session_state:
        st.session_state.apt_answered = {}
    if "apt_questions" not in st.session_state:
        st.session_state.apt_questions = APTITUDE_QUESTIONS.copy()
        random.shuffle(st.session_state.apt_questions)

    categories = ["All", "Quantitative", "Logical", "Verbal", "Technical"]
    cat_filter = st.selectbox("Category", categories)

    questions = st.session_state.apt_questions
    if cat_filter != "All":
        questions = [q for q in questions if q["category"] == cat_filter]

    # Stats
    total = len(questions)
    answered = len([k for k in st.session_state.apt_answered if k < total])
    correct  = sum(1 for i, q in enumerate(questions) if st.session_state.apt_answered.get(i) == q["answer"])

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        (str(total), "Questions", "#6366f1"),
        (str(answered), "Attempted", "#3b82f6"),
        (str(correct), "Correct", "#10b981"),
        (f"{int(correct/max(answered,1)*100)}%", "Accuracy", "#f59e0b"),
    ]
    for col, (num, label, color) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""<div class="stat-chip">
              <div class="num" style="color:{color}">{num}</div>
              <div class="label">{label}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Progress bar
    if total > 0:
        pct = answered / total
        st.progress(pct, text=f"Progress: {answered}/{total}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Reset button
    col_rst, _ = st.columns([1, 4])
    with col_rst:
        if st.button("🔄 Reset Quiz"):
            st.session_state.apt_answered = {}
            st.session_state.apt_score = 0
            random.shuffle(st.session_state.apt_questions)
            st.rerun()

    # Questions
    for i, q in enumerate(questions):
        cat_colors = {
            "Quantitative": "#6366f1", "Logical": "#3b82f6",
            "Verbal": "#10b981", "Technical": "#f59e0b"
        }
        color = cat_colors.get(q["category"], "#6366f1")
        is_answered = i in st.session_state.apt_answered

        with st.expander(
            f"Q{i+1}. {q['question'][:70]}{'…' if len(q['question'])>70 else ''}",
            expanded=not is_answered
        ):
            st.markdown(f'<span class="badge" style="background:rgba(99,102,241,0.15);color:{color};border:1px solid {color}40;">{q["category"]}</span>', unsafe_allow_html=True)
            st.markdown(f"**{q['question']}**")

            if is_answered:
                user_ans = st.session_state.apt_answered[i]
                correct_ans = q["answer"]
                for opt in q["options"]:
                    if opt == correct_ans:
                        st.markdown(f'✅ **{opt}** ← Correct Answer', unsafe_allow_html=False)
                    elif opt == user_ans:
                        st.markdown(f'❌ ~~{opt}~~ ← Your Answer', unsafe_allow_html=False)
                    else:
                        st.markdown(f'○ {opt}')
                st.info(f"💡 **Explanation:** {q['explanation']}")
                log_progress(uid, date.today().isoformat(), "aptitude_question")
            else:
                selected = st.radio(
                    "Choose your answer:",
                    q["options"],
                    key=f"apt_q_{i}",
                    index=None
                )
                if st.button("Submit Answer", key=f"apt_sub_{i}"):
                    if selected is None:
                        st.warning("Please select an answer first.")
                    else:
                        st.session_state.apt_answered[i] = selected
                        if selected == q["answer"]:
                            st.success("✅ Correct!")
                        else:
                            st.error(f"❌ Wrong! Correct: {q['answer']}")
                        st.rerun()

    # Badge check
    if answered == total and total > 0 and correct / total >= 0.7:
        add_badge(uid, "quiz_master")
        st.markdown("""
        <div class="notification">
          🏆 <strong>Quiz Master badge earned!</strong> You scored ≥70% on this aptitude test.
        </div>""", unsafe_allow_html=True)
