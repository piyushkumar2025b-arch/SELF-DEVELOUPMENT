"""
AI Skills Corner page — how AI tools automate workflows, features and usage
"""
import streamlit as st
from data.questions import AI_WORKFLOWS
from utils.styles import inject_css

def show_ai_skills():
    inject_css()

    st.markdown("""
    <h1>🤖 AI Skills Corner</h1>
    <p style="color:#94a3b8">Learn how modern AI tools can supercharge your developer productivity and automate complex workflows.</p>
    """, unsafe_allow_html=True)

    # Categories filter
    categories = [
        "All", "Writing & Reasoning", "Code Generation", "Code Editing & Agents",
        "Productivity & Notes", "Research & Search", "Automation", "Meeting & Audio",
        "Visual Creation", "UI Generation", "AI for Learning", "Document & PDF",
        "DevOps & CLI", "Audio & Voice", "Video & Animation", "Interview Prep AI",
    ]
    sel_cat = st.selectbox("Filter by Category", categories)

    filtered_workflows = AI_WORKFLOWS
    if sel_cat != "All":
        filtered_workflows = [w for w in AI_WORKFLOWS if w["category"] == sel_cat]

    # Render workflows as cards
    for w in filtered_workflows:
        use_cases_html = "".join(f"<li>{uc}</li>" for uc in w["use_cases"])
        st.markdown(f"""
        <div class="card card-blue" style="margin-bottom: 1.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.75rem;">
            <div style="display:flex; align-items:center; gap:0.5rem;">
              <span style="font-size:1.8rem;">{w['icon']}</span>
              <h2 style="margin:0; font-size:1.4rem; color:#f1f5f9;">{w['tool']}</h2>
            </div>
            <span class="badge badge-medium">{w['category']}</span>
          </div>
          
          <div style="margin-top: 10px;">
            <strong style="color:#818cf8;">🚀 Top Use Cases:</strong>
            <ul style="color:#cbd5e1; margin-top:5px; padding-left: 20px;">
              {use_cases_html}
            </ul>
          </div>
          
          <div style="margin-top: 10px;">
            <strong style="color:#34d399;">⚡ Power Features:</strong>
            <p style="color:#cbd5e1; margin: 4px 0 0 0; font-size:0.9rem;">{w['power_features']}</p>
          </div>
          
          <div style="margin-top: 10px;">
            <strong style="color:#fbbf24;">⚙️ Suggested Workflow:</strong>
            <p style="color:#cbd5e1; margin: 4px 0 0 0; font-size:0.9rem; font-family:var(--mono); background:#0f1629; padding:8px; border-radius:6px; border:1px solid #1e2d52;">{w['workflow']}</p>
          </div>
          
          <div style="margin-top:15px; text-align:right;">
            <a href="{w['link']}" target="_blank" class="link-btn" style="padding: 6px 16px;">Try {w['tool']} →</a>
          </div>
        </div>
        """, unsafe_allow_html=True)
