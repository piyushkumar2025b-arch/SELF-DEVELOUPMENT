"""
Authentication page: Login / Register / Developer mode
"""
import streamlit as st
from db.database import create_user, verify_user, add_badge
from utils.styles import inject_css

DEV_PASSWORD = "LOVE"

def show_auth():
    inject_css()
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1rem;">
      <div style="font-size:3.5rem; margin-bottom:0.5rem;">🚀</div>
      <h1 style="font-size:2.5rem; background:linear-gradient(135deg,#6366f1,#3b82f6,#10b981);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;">
        FAANG Prep Hub
      </h1>
      <p style="color:#94a3b8; margin-top:0.5rem; font-size:1.05rem;">
        Your all-in-one FAANG interview preparation platform
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Guest login — prominent CTA
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(251,191,36,0.12), rgba(245,158,11,0.06));
            border: 1px solid rgba(251,191,36,0.35);
            border-radius: 14px;
            padding: 1.1rem 1.4rem;
            margin-bottom: 1.2rem;
            text-align: center;
        ">
          <div style="font-size:1.8rem; margin-bottom:0.3rem;">👤</div>
          <p style="color:#fbbf24; font-weight:700; font-size:1.05rem; margin:0 0 0.3rem 0;">Just browsing?</p>
          <p style="color:#94a3b8; font-size:0.85rem; margin:0 0 0.8rem 0;">Jump in instantly — no account needed.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("👤  Continue as Guest", use_container_width=True, key="guest_btn"):
            st.session_state.logged_in = True
            st.session_state.is_dev = False
            st.session_state.user = {
                "id": -1,
                "username": "Guest",
                "email": "",
                "badges": "[]",
                "streak": 0,
                "avatar_color": "#f59e0b",
            }
            st.success("Welcome, Guest! Explore the app freely. 🎉")
            st.rerun()

        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin: 0.8rem 0;">
          <hr style="flex:1; border-color:#1e2d52; margin:0;">
          <span style="color:#475569; font-size:0.8rem;">or sign in</span>
          <hr style="flex:1; border-color:#1e2d52; margin:0;">
        </div>
        """, unsafe_allow_html=True)

    # Mode selector
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        mode = st.radio(
            "Select option",
            ["🔑 Existing User", "✨ New User", "👨‍💻 Developer Mode"],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if mode == "✨ New User":
            st.markdown("### Create Account")
            username = st.text_input("Username", placeholder="e.g. code_ninja_42", key="reg_user")
            email    = st.text_input("Email (optional)", placeholder="you@email.com", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")
            confirm  = st.text_input("Confirm Password", type="password", key="reg_conf")

            if st.button("🚀 Create Account", use_container_width=True):
                if not username or not password:
                    st.error("Username and password are required.")
                elif len(password) < 4:
                    st.error("Password must be at least 4 characters.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                else:
                    result = create_user(username, password, email)
                    if result["success"]:
                        st.success("Account created! Please log in.")
                    else:
                        st.error(result["message"])

        elif mode == "🔑 Existing User":
            st.markdown("### Welcome Back")
            username = st.text_input("User ID / Username", placeholder="Enter your username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("🔓 Sign In", use_container_width=True):
                if not username or not password:
                    st.error("Please enter username and password.")
                else:
                    result = verify_user(username, password)
                    if result["success"]:
                        st.session_state.user = result["user"]
                        st.session_state.logged_in = True
                        st.session_state.is_dev = False
                        add_badge(result["user"]["id"], "first_login")
                        st.success(f"Welcome back, {username}! 👋")
                        st.rerun()
                    else:
                        st.error(result["message"])

        elif mode == "👨‍💻 Developer Mode":
            st.markdown("### Developer Access")
            st.markdown('<div class="card card-red"><small style="color:#f87171">🔒 Restricted Access — Developer Only</small></div>', unsafe_allow_html=True)
            dev_pass = st.text_input("Developer Password", type="password", key="dev_pass")

            if st.button("🔐 Enter Dev Mode", use_container_width=True):
                if dev_pass == DEV_PASSWORD:
                    st.session_state.is_dev = True
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        "id": 0, "username": "Developer", "badges": "[]",
                        "streak": 0, "avatar_color": "#ec4899"
                    }
                    st.success("Developer mode activated! 🛠️")
                    st.rerun()
                else:
                    st.error("Incorrect developer password.")

    # Feature pins
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;">
      <span class="pin pin-green">📊 DSA Prep</span>
      <span class="pin">🏢 FAANG Company Guide</span>
      <span class="pin pin-gold">🧠 Aptitude Trainer</span>
      <span class="pin pin-red">🔥 Heatmap Tracker</span>
      <span class="pin">💻 Coding Languages</span>
      <span class="pin pin-green">🤖 AI Skills Corner</span>
      <span class="pin">💪 Fitness Tracker</span>
      <span class="pin pin-gold">📝 Notes</span>
    </div>
    """, unsafe_allow_html=True)
