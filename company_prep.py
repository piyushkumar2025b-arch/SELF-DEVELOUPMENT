"""
FAANG Company Preparation page
"""
import streamlit as st
from data.questions import FAANG_COMPANY_DATA, DSA_TOPICS
from utils.styles import inject_css
from db.database import log_progress
from datetime import date

def show_company_prep():
    inject_css()
    uid = st.session_state.user["id"]

    st.markdown("""
    <h1>🏢 FAANG Company Preparation</h1>
    <p style="color:#94a3b8">Deep-dive guides for each top tech company. Know what they value, what they test.</p>
    """, unsafe_allow_html=True)

    # Company selector tabs
    companies = list(FAANG_COMPANY_DATA.keys())
    selected_company = st.selectbox(
        "Select Company",
        companies,
        format_func=lambda x: f"{FAANG_COMPANY_DATA[x]['icon']} {x}"
    )

    data = FAANG_COMPANY_DATA[selected_company]
    log_progress(uid, date.today().isoformat(), f"company_{selected_company.replace(' ','_')}")

    # Header
    st.markdown(f"""
    <div class="card" style="border-color:{data['color']}40; background:linear-gradient(135deg, rgba(0,0,0,0.3), {data['color']}10);">
      <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
        <span style="font-size:2.5rem;">{data['icon']}</span>
        <div>
          <h2 style="margin:0; color:#f1f5f9;">{selected_company}</h2>
          <p style="color:#94a3b8; margin:0;">{data['rounds']} interview rounds</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "💡 Tips & Strategy", "🎯 Hot Topics", "🔗 Resources"])

    with tab1:
        st.markdown("#### Focus Areas")
        cols = st.columns(len(data["focus"]))
        focus_colors = ["#6366f1","#3b82f6","#10b981","#f59e0b"]
        for i, (col, focus) in enumerate(zip(cols, data["focus"])):
            with col:
                c = focus_colors[i % len(focus_colors)]
                st.markdown(f"""
                <div class="card" style="text-align:center; border-color:{c}40;">
                  <div style="color:{c}; font-size:1.5rem; margin-bottom:5px;">{"🎯🔧💡🤝"[i]}</div>
                  <div style="font-weight:600; font-size:0.9rem;">{focus}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card card-blue" style="margin-top:1rem;">
          <strong>📊 Interview Structure</strong>
          <p style="color:#94a3b8; margin-top:0.5rem;">{selected_company} typically has <strong style="color:#60a5fa;">{data['rounds']} rounds</strong> 
          focusing on {', '.join(data['focus'][:2])} among other areas. Each round is approximately 45-60 minutes.</p>
        </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("#### Insider Tips")
        for i, tip in enumerate(data["tips"]):
            st.markdown(f"""
            <div class="q-item" style="margin:6px 0;">
              <div style="display:flex; align-items:center; gap:10px;">
                <span style="color:#6366f1; font-weight:800; font-family:monospace;">{i+1:02d}</span>
                <span>{tip}</span>
              </div>
            </div>""", unsafe_allow_html=True)

        # Interview timeline
        st.markdown("<br>#### 📅 Typical Interview Timeline")
        stages = ["📧 Recruiter Screen", "💻 OA / Coding", "📞 Phone Interview", "🏢 Onsite / Virtual Onsite", "🎉 Offer"]
        cols2 = st.columns(len(stages))
        for i, (col, stage) in enumerate(zip(cols2, stages)):
            with col:
                st.markdown(f"""
                <div style="text-align:center; padding:0.5rem;">
                  <div style="font-size:1.5rem;">{stage.split()[0]}</div>
                  <div style="font-size:0.7rem; color:#94a3b8; margin-top:3px;">{' '.join(stage.split()[1:])}</div>
                  {"<div style='color:#6366f1;font-size:0.7rem;'>→</div>" if i < len(stages)-1 else ""}
                </div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("#### 🔥 Most Tested Topics")
        topic_cols = st.columns(2)
        for i, topic in enumerate(data["hot_topics"]):
            with topic_cols[i % 2]:
                questions = DSA_TOPICS.get(topic, [])
                count = len(questions)
                st.markdown(f"""
                <div class="card card-blue">
                  <strong>📌 {topic}</strong>
                  <p style="color:#94a3b8; font-size:0.82rem; margin:4px 0;">{count} curated problems available</p>
                  <div>
                    {''.join(f'<span class="badge badge-{q["difficulty"].lower()}">{q["title"][:25]}{"…" if len(q["title"])>25 else ""}</span> ' for q in questions[:3])}
                  </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>#### System Design Tips")
        if selected_company in ["Google", "Meta (Facebook)", "Netflix"]:
            scale = {"Google": "1B+ users", "Meta (Facebook)": "3B+ users", "Netflix": "220M+ subscribers"}
            st.markdown(f"""
            <div class="card card-gold">
              <strong>⚙️ Design at {scale.get(selected_company, 'massive')} scale</strong>
              <ul style="color:#94a3b8; margin-top:0.5rem;">
                <li>Always start with requirements clarification</li>
                <li>Back-of-envelope estimation (QPS, storage, bandwidth)</li>
                <li>High-level design → Deep dive into bottlenecks</li>
                <li>Discuss trade-offs explicitly</li>
              </ul>
            </div>""", unsafe_allow_html=True)

    with tab4:
        st.markdown("#### 🌐 Preparation Resources")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown(f"""
            <div class="card">
              <strong>📊 Glassdoor Reviews</strong>
              <p style="color:#94a3b8; font-size:0.85rem; margin:6px 0;">Real interview experiences from candidates.</p>
              <a href="{data['glassdoor']}" target="_blank" class="link-btn">Open Glassdoor →</a>
            </div>""", unsafe_allow_html=True)
        with col_r2:
            st.markdown(f"""
            <div class="card">
              <strong>📘 Complete Prep Guide</strong>
              <p style="color:#94a3b8; font-size:0.85rem; margin:6px 0;">Step-by-step preparation roadmap.</p>
              <a href="{data['prep_guide']}" target="_blank" class="link-btn">Read Guide →</a>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>")
        st.markdown("""
        <div class="card">
          <strong>📚 Universal Resources</strong>
          <div style="margin-top:0.75rem; display:flex; flex-wrap:wrap; gap:8px;">
            <a href="https://neetcode.io" target="_blank" class="link-btn">NeetCode.io</a>
            <a href="https://www.techinterviewhandbook.org" target="_blank" class="link-btn">Tech Interview Handbook</a>
            <a href="https://interviewing.io" target="_blank" class="link-btn">Interviewing.io</a>
            <a href="https://www.pramp.com" target="_blank" class="link-btn">Pramp (Mock Interviews)</a>
            <a href="https://grokking.design" target="_blank" class="link-btn">Grokking System Design</a>
            <a href="https://www.youtube.com/@NeetCode" target="_blank" class="link-btn">NeetCode YouTube</a>
          </div>
        </div>""", unsafe_allow_html=True)
