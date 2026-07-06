import streamlit as st
from datetime import datetime
from db.database import add_user_comment, get_user_comments, get_connection
from utils.styles import inject_css

# Prepopulate database with realistic comments if empty
def seed_mock_comments_if_empty():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM user_comments")
    count = c.fetchone()[0]
    if count == 0:
        mock_comments = [
            (1, "Alice_Coder", "🎯 Determined", "Just solved 5 Dynamic Programming questions! Feeling ready for the Meta screening round.", "2026-07-06 08:30:00"),
            (2, "Bob_Dev", "😅 Stressed", "Trees and graphs are kicking my butt today. Visualizer helped a lot, but I need to do more practice.", "2026-07-06 09:12:00"),
            (3, "Charlie_Algorithms", "🚀 Excited", "Sandbox runtime is blazingly fast! Compiled Rust in 150ms. Awesome feature.", "2026-07-06 09:35:00"),
            (4, "TechQueen", "🏆 Confident", "Got a score of 95% in the Mock Interview simulator! Let's crack Google next week.", "2026-07-06 09:50:00"),
            (5, "PrepWizard", "🥱 Tired", "Did a 4-hour study blocks marathon. Time to track my fitness and call it a day.", "2026-07-06 10:02:00")
        ]
        c.executemany(
            "INSERT INTO user_comments (user_id, username, feeling, comment, created_at) VALUES (?,?,?,?,?)",
            mock_comments
        )
        conn.commit()
    conn.close()

def show_comments():
    inject_css()
    seed_mock_comments_if_empty()
    
    st.markdown("<h1>💬 Workspace Feed & Testimonials</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:1.0rem;'>Share how you are feeling, write notes for your future self, or log testimonials about your preparation experience.</p>", unsafe_allow_html=True)
    
    # Check login session
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("Please sign in to read and post comments.")
        return
        
    current_user = st.session_state.user
    uid = current_user["id"]
    u_name = current_user["username"]
    
    # ── Post a Comment Form ────────────────────────────────────
    st.markdown("### ✍️ Share Your Status")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        feeling = st.selectbox(
            "How are you feeling?",
            ["🎯 Determined", "🚀 Excited", "😅 Stressed", "🏆 Confident", "🥱 Tired", "🧠 Focused", "🔥 Unstoppable"]
        )
    with col2:
        comment_text = st.text_input("What is on your mind?", placeholder="e.g. Crushing binary search today! 🚀")
        
    if st.button("📢 Post Status Update", use_container_width=True):
        if comment_text.strip() == "":
            st.error("Status update content cannot be empty.")
        else:
            add_user_comment(uid, u_name, feeling, comment_text)
            st.success("Status posted successfully! ✨")
            st.rerun()
            
    st.markdown("---")
    
    # ── Display Comments ───────────────────────────────────────
    st.markdown("### 📣 Live Feed")
    comments = get_user_comments()
    
    if not comments:
        st.info("No status updates in the feed yet. Be the first to post!")
        return
        
    for item in comments:
        # Format date nicely
        raw_date = item["created_at"]
        try:
            parsed = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
            formatted_date = parsed.strftime("%b %d, %Y at %I:%M %p")
        except Exception:
            try:
                # Isoformat parsing fallback
                parsed = datetime.fromisoformat(raw_date)
                formatted_date = parsed.strftime("%b %d, %Y at %I:%M %p")
            except Exception:
                formatted_date = raw_date
            
        username = item["username"]
        user_id = item["user_id"]
        feel = item["feeling"]
        content = item["comment"]
        
        # User ID badge
        uid_badge = f"ID: #{user_id}" if user_id > 0 else "ID: #Dev"
        if user_id == -1:
            uid_badge = "ID: #Guest"
            
        # Draw comment card with premium styling
        st.markdown(f"""
        <div style="background:rgba(30, 41, 59, 0.45); border:1px solid rgba(99, 102, 241, 0.2); border-radius:12px; padding:16px; margin-bottom:12px; backdrop-filter: blur(10px);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <div style="width:28px; height:28px; border-radius:50%; background:#4f46e5; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:0.8rem;">
                        {username[0].upper()}
                    </div>
                    <span style="font-weight:600; color:#f1f5f9;">@{username}</span>
                    <span style="background:rgba(99, 102, 241, 0.15); color:#818cf8; font-size:0.7rem; padding:2px 6px; border-radius:4px; font-weight:bold;">{uid_badge}</span>
                </div>
                <span style="font-size:0.75rem; color:#64748b;">📅 {formatted_date}</span>
            </div>
            <div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">
                <span style="font-size:0.85rem; background:rgba(245, 158, 11, 0.1); color:#fbbf24; padding:2px 6px; border-radius:4px; font-weight:500;">
                    {feel}
                </span>
            </div>
            <p style="color:#cbd5e1; margin:0; font-size:0.95rem; line-height:1.4;">{content}</p>
        </div>
        """, unsafe_allow_html=True)
