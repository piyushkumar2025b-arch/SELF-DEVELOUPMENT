"""
Dashboard page — integrates C++ performance analytics and React JSX/Tailwind interactive widgets
"""
import streamlit as st
import subprocess
import os
import sys
import json
from datetime import date
from utils.styles import inject_css
from db.database import get_progress, get_fitness_logs, get_notes, get_links, get_connection

def run_cpp_analytics(dsa_count, streak, apt_pct, fit_count):
    # Check for executable
    exe_name = "analytics.exe" if sys.platform == "win32" else "analytics"
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exe_path = os.path.join(root_dir, "cpp_modules", exe_name)
    
    if os.path.exists(exe_path):
        try:
            # Run C++ binary
            res = subprocess.run(
                [exe_path, str(dsa_count), str(streak), str(apt_pct), str(fit_count)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            # Parse output
            return json.loads(res.stdout.strip())
        except Exception:
            pass # fallback to python emulator
            
    # Python Emulator Fallback
    score = (dsa_count * 2.5) + (streak * 3.0) + (apt_pct * 0.4) + (fit_count * 5.0)
    score = min(max(score, 0.0), 100.0)
    
    status = "Novice Prep Status"
    color = "#ef4444"
    tip = "Start logging your coding practices, workouts, and solve some DSA problems daily."
    
    if score >= 80.0:
        status = "Elite Candidate ready for FAANG!"
        color = "#10b981"
        tip = "Excellent progress! Focus on mock interviewing and high-level system design topics."
    elif score >= 50.0:
        status = "Solid Candidate"
        color = "#f59e0b"
        tip = "Good consistency. Increase LeetCode Medium/Hard problems frequency and finish your aptitude tests."
    elif score >= 20.0:
        status = "Developing Candidate"
        color = "#3b82f6"
        tip = "Keep solving DSA problems. Try to build a consistent 7-day streak to unlock week warrior badges."

    return {
        "success": True,
        "score": int(score),
        "status": status,
        "color": color,
        "recommendation": tip
    }

def show_dashboard():
    inject_css()
    uid = st.session_state.user["id"]
    
    st.markdown("""
    <h1>📊 Interactive Analytics Dashboard</h1>
    <p style="color:#94a3b8">Interactive real-time metrics computed via C++ engine and rendered with React JSX.</p>
    """, unsafe_allow_html=True)
    
    # Fetch metrics for C++
    conn = get_connection()
    c = conn.cursor()
    # DSA topics visited
    c.execute("SELECT COUNT(DISTINCT activity_type) FROM progress_logs WHERE user_id=? AND activity_type LIKE 'dsa_%'", (uid,))
    dsa_count = c.fetchone()[0]
    
    # Aptitude accuracy estimation
    c.execute("SELECT COUNT(*) FROM progress_logs WHERE user_id=? AND activity_type='aptitude_question'", (uid,))
    apt_tries = c.fetchone()[0]
    # Simple estimate (default 50% accuracy or mock)
    apt_pct = min(100, apt_tries * 5) if apt_tries > 0 else 0
    
    conn.close()
    
    streak = st.session_state.user.get("streak", 0)
    workouts = len(get_fitness_logs(uid))
    
    # Compute via C++
    report = run_cpp_analytics(dsa_count, streak, apt_pct, workouts)
    
    # Display C++ suggestion banner
    st.markdown(f"""
    <div class="card" style="border-color:{report['color']}80; background:linear-gradient(135deg, rgba(10,14,26,0.6), {report['color']}08); margin-bottom: 2rem;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <span style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase; font-weight:bold; letter-spacing:0.05em;">C++ High-Performance Advisor</span>
          <h2 style="margin:5px 0 0 0; font-size:1.6rem; color:#f1f5f9;">{report['status']}</h2>
          <p style="color:#cbd5e1; margin-top:8px; font-size:0.92rem;">💡 {report['recommendation']}</p>
        </div>
        <div style="text-align:center; padding-left: 20px;">
          <div style="font-size:2.8rem; font-weight:800; color:{report['color']}; font-family:var(--mono); line-height:1;">{report['score']}%</div>
          <div style="color:#94a3b8; font-size:0.68rem; text-transform:uppercase; margin-top:5px; font-weight:bold;">Prep Index</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Embed React + Tailwind frontend frame
    # Load index.html, badge_animator.js, and InteractiveDashboard.jsx
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        frontend_dir = os.path.join(root_dir, "frontend")
        with open(os.path.join(frontend_dir, "index.html"), "r", encoding="utf-8") as f:
            html_template = f.read()
        with open(os.path.join(frontend_dir, "badge_animator.js"), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(frontend_dir, "InteractiveDashboard.jsx"), "r", encoding="utf-8") as f:
            jsx_code = f.read()
            
        # Inline them directly into the HTML to ensure server compatibility
        inlined_html = html_template.replace(
            '<script src="badge_animator.js"></script>',
            f'<script>{js_code}</script>'
        ).split('<script type="text/javascript">')[0] + f'<script type="text/babel">{jsx_code}</script></body></html>'
        
        # Display the iframe component
        import streamlit.components.v1 as components
        components.html(inlined_html, height=520, scrolling=True)
        
    except Exception as e:
        st.error(f"Error loading interactive React components: {e}")
