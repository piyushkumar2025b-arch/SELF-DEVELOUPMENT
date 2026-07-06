"""
DSA Preparation page — dropdown topics, clickable LeetCode + solution links
"""
import streamlit as st
from data.questions import DSA_TOPICS
from utils.styles import inject_css
from db.database import log_progress, add_badge
from datetime import date

def show_dsa():
    inject_css()
    uid = st.session_state.user["id"]

    st.markdown("""
    <h1>📊 DSA Preparation Hub</h1>
    <p style="color:#94a3b8">Curated questions from top FAANG companies. Click any topic to expand.</p>
    """, unsafe_allow_html=True)

    # Stats row
    total_q = sum(len(v) for v in DSA_TOPICS.values())
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="stat-chip">
          <div class="num" style="color:#6366f1">{len(DSA_TOPICS)}</div>
          <div class="label">Topics</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stat-chip">
          <div class="num" style="color:#10b981">{total_q}</div>
          <div class="label">Problems</div></div>""", unsafe_allow_html=True)
    with col3:
        easy = sum(1 for qs in DSA_TOPICS.values() for q in qs if q["difficulty"]=="Easy")
        st.markdown(f"""<div class="stat-chip">
          <div class="num" style="color:#10b981">{easy}</div>
          <div class="label">Easy</div></div>""", unsafe_allow_html=True)
    with col4:
        hard = sum(1 for qs in DSA_TOPICS.values() for q in qs if q["difficulty"]=="Hard")
        st.markdown(f"""<div class="stat-chip">
          <div class="num" style="color:#ef4444">{hard}</div>
          <div class="label">Hard</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filters
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        search = st.text_input("🔍 Search problems", placeholder="e.g. Two Sum, Graph...")
    with col_f2:
        diff_filter = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])

    st.markdown("<br>", unsafe_allow_html=True)

    visited_topics = set()
    for topic, questions in DSA_TOPICS.items():
        # Filter
        filtered = questions
        if diff_filter != "All":
            filtered = [q for q in filtered if q["difficulty"] == diff_filter]
        if search:
            filtered = [q for q in filtered if search.lower() in q["title"].lower()]
        if not filtered:
            continue

        icon_map = {
            "Arrays & Hashing": "🗂️", "Two Pointers": "👉", "Sliding Window": "🪟",
            "Stack": "📚", "Binary Search": "🔍", "Trees": "🌳",
            "Dynamic Programming": "💡", "Graphs": "🕸️", "Linked List": "🔗",
            "Heap / Priority Queue": "⛰️", "Intervals": "📅", "Bit Manipulation": "🔢",
            "Math & Geometry": "📐", "Backtracking": "♟️", "Tries": "🔤",
            "Greedy": "🎯", "Strings": "📝", "Sorting & Searching": "🔀",
            "Design & Simulation": "🏗️", "Union-Find & Advanced Graphs": "🌐",
            "Divide & Conquer": "✂️", "Matrix & Grid": "🧮",
            "Monotonic Stack & Queue": "📈", "Recursion & Memoization": "🔁",
            "Advanced Trees & BST": "🌲", "Advanced Dynamic Programming": "🧩",
            "BFS & DFS Patterns": "🗺️", "Object-Oriented Design": "🏛️",
        }
        icon = icon_map.get(topic, "📌")

        with st.expander(f"{icon} {topic}  ({len(filtered)} problems)", expanded=False):
            visited_topics.add(topic)
            log_progress(uid, date.today().isoformat(), f"dsa_{topic.replace(' ','_')}")

            for q in filtered:
                # Difficulty color
                diff_color = {"Easy": "#10b981", "Medium": "#f59e0b", "Hard": "#ef4444"}.get(q["difficulty"], "#94a3b8")
                companies_html = "".join(f'<span class="company-tag">{c}</span>' for c in q.get("company", []))

                st.markdown(f"""
                <div class="q-item">
                  <div>
                    <span style="font-weight:600; color:#f1f5f9; font-size:0.95rem;">{q['title']}</span>
                    <span class="badge badge-{q['difficulty'].lower()}" style="margin-left:8px;">{q['difficulty']}</span>
                    <div style="margin-top:5px;">{companies_html}</div>
                    <div style="color:#64748b; font-size:0.78rem; margin-top:4px;">💡 {q.get('note','')}</div>
                  </div>
                  <div style="display:flex; gap:8px; flex-shrink:0;">
                    <a href="{q['lc']}" target="_blank" class="link-btn">🔗 LeetCode</a>
                    <a href="{q['solution']}" target="_blank" class="link-btn" style="background:rgba(16,185,129,0.12);border-color:rgba(16,185,129,0.25);color:#6ee7b7;">▶ Solution</a>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    if len(visited_topics) >= len(DSA_TOPICS):
        add_badge(uid, "code_ninja")

    # Study tips
    st.markdown("---")
    st.markdown("### 🎯 How to Use This Section")
    cols = st.columns(3)
    tips = [
        ("1️⃣ Learn the Pattern", "Don't just memorize solutions. Understand the underlying pattern (sliding window, two pointer, etc.)"),
        ("2️⃣ Code Without Help", "After watching a solution, close it and re-implement from scratch within 24 hours."),
        ("3️⃣ Time Yourself", "Practice under real interview conditions. 20 min for Easy, 30 for Medium, 45 for Hard."),
    ]
    for col, (title, desc) in zip(cols, tips):
        with col:
            st.markdown(f"""
            <div class="card">
              <strong>{title}</strong>
              <p style="color:#94a3b8; font-size:0.85rem; margin-top:0.5rem;">{desc}</p>
            </div>""", unsafe_allow_html=True)
