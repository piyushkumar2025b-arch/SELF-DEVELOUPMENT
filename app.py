"""
Main Streamlit application entrypoint
"""
import streamlit as st
import os
import base64
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="FAANG Prep Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

from db.database import init_db, get_user_settings, save_wallpaper, get_dev_uploads, save_dev_upload, get_user
from utils.styles import inject_css, quote_box
from utils.api_helpers import get_quote_of_day

# Ensure DB and directories are set up
init_db()
os.makedirs("dev_uploads_store", exist_ok=True)

# Initialize Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "is_dev" not in st.session_state:
    st.session_state.is_dev = False

# Inject base css style
inject_css()

# Inject Wallpaper if present
def inject_wallpaper():
    if st.session_state.logged_in and st.session_state.user:
        uid = st.session_state.user["id"]
        settings = get_user_settings(uid)
        wpath = settings.get("wallpaper_path")
        if wpath and os.path.exists(wpath):
            try:
                with open(wpath, "rb") as f:
                    data = base64.b64encode(f.read()).decode()
                ext = Path(wpath).suffix.replace(".","")
                if not ext:
                    ext = "png"
                st.markdown(f"""
                <style>
                .stApp {{
                    background-image: linear-gradient(rgba(10, 14, 26, 0.85), rgba(10, 14, 26, 0.85)), url("data:image/{ext};base64,{data}") !important;
                    background-size: cover !important;
                    background-attachment: fixed !important;
                    background-position: center !important;
                }}
                </style>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Could not load custom wallpaper: {e}")

inject_wallpaper()

# Show Login if not logged in
if not st.session_state.logged_in:
    from pages_module.auth import show_auth
    show_auth()
else:
    # Get fresh user state
    uid = st.session_state.user["id"]
    if uid not in (0, -1): # skip DB refresh for dev override and guest
        st.session_state.user = get_user(uid)

    # Sidebar Header
    u_name = st.session_state.user["username"]
    u_color = st.session_state.user.get("avatar_color", "#6366f1")
    streak = st.session_state.user.get("streak", 0)

    st.sidebar.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; padding:10px 0; border-bottom:1px solid #1e2d52; margin-bottom:15px;">
      <div style="width:40px; height:40px; border-radius:50%; background:{u_color}; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:1.2rem; color:white;">
        {u_name[0].upper()}
      </div>
      <div>
        <h4 style="margin:0; color:#f1f5f9;">{u_name}</h4>
        <span style="color:#94a3b8; font-size:0.75rem;">🔥 {streak} Day Streak</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation menu
    nav_options = [
        "📈 Performance Dashboard",
        "📊 DSA Prep",
        "🔍 Algorithm Visualizer",
        "💻 Code Sandbox",
        "🏢 FAANG Company Guide",
        "🧠 Aptitude Trainer",
        "💻 Learn Coding Languages",
        "📅 Study Planner",
        "🎯 Mock Interview",
        "🚀 Project Showcase",
        "👥 Community Forum",
        "🔌 Coding Profiles",
        "🔥 Activity Heatmap",
        "📝 Notes",
        "💪 Fitness Tracker",
        "🤖 AI Skills Corner",
        "⚙️ Settings & Customization"
    ]

    if st.session_state.is_dev:
        nav_options.append("🛠️ Developer Console")

    nav_options.append("🔑 Sign Out")

    choice = st.sidebar.radio("Navigation Menu", nav_options, label_visibility="collapsed")

    st.sidebar.markdown("---")
    
    # Quote of the day at the bottom of sidebar
    quote = get_quote_of_day()
    st.sidebar.markdown(f"""
    <div style="padding:10px; background:rgba(99,102,241,0.05); border:1px solid rgba(99,102,241,0.15); border-radius:8px;">
      <p style="font-size:0.78rem; font-style:italic; color:#cbd5e1; margin-bottom:5px;">"{quote['quote']}"</p>
      <p style="font-size:0.65rem; color:#818cf8; text-align:right; margin:0;">— {quote['author']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Route page selection
    if choice == "📈 Performance Dashboard":
        from pages_module.dashboard import show_dashboard
        show_dashboard()
    elif choice == "📊 DSA Prep":
        from pages_module.dsa import show_dsa
        show_dsa()
    elif choice == "🔍 Algorithm Visualizer":
        from pages_module.visualizer import show_visualizer
        show_visualizer()
    elif choice == "💻 Code Sandbox":
        from pages_module.sandbox import show_sandbox
        show_sandbox()
    elif choice == "🏢 FAANG Company Guide":
        from pages_module.company_prep import show_company_prep
        show_company_prep()
    elif choice == "🧠 Aptitude Trainer":
        from pages_module.aptitude import show_aptitude
        show_aptitude()
    elif choice == "💻 Learn Coding Languages":
        from pages_module.languages import show_languages
        show_languages()
    elif choice == "🔌 Coding Profiles":
        from pages_module.profiles import show_profiles
        show_profiles()
    elif choice == "🔥 Activity Heatmap":
        from pages_module.heatmap import show_heatmap
        show_heatmap()
    elif choice == "📝 Notes":
        from pages_module.notes import show_notes
        show_notes()
    elif choice == "💪 Fitness Tracker":
        from pages_module.fitness import show_fitness
        show_fitness()
    elif choice == "📅 Study Planner":
        from pages_module.study_planner import show_study_planner
        show_study_planner()
    elif choice == "🎯 Mock Interview":
        from pages_module.mock_interview import show_mock_interview
        show_mock_interview()
    elif choice == "🚀 Project Showcase":
        from pages_module.project_showcase import show_project_showcase
        show_project_showcase()
    elif choice == "👥 Community Forum":
        from pages_module.community import show_community
        show_community()
    elif choice == "🤖 AI Skills Corner":
        from pages_module.ai_skills import show_ai_skills
        show_ai_skills()
    elif choice == "⚙️ Settings & Customization":
        st.markdown("<h1>⚙️ Settings & Customization</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Customize your workspace profile details and look-and-feel.</p>", unsafe_allow_html=True)
        
        st.markdown("### 🖼️ Upload Custom Wallpaper")
        wp_file = st.file_uploader("Upload wallpaper image (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if wp_file is not None:
            os.makedirs("wallpapers", exist_ok=True)
            wp_path = os.path.join("wallpapers", f"wallpaper_{uid}_{wp_file.name}")
            with open(wp_path, "wb") as f:
                f.write(wp_file.getbuffer())
            save_wallpaper(uid, wp_path)
            st.success("Custom wallpaper set! Please reload to see the background change.")
            st.rerun()
            
        settings = get_user_settings(uid)
        if settings.get("wallpaper_path"):
            if st.button("❌ Remove Custom Wallpaper", use_container_width=True):
                save_wallpaper(uid, None)
                st.success("Custom wallpaper removed!")
                st.rerun()
                
    elif choice == "🛠️ Developer Console":
        st.markdown("<h1>🛠️ Developer Console</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Upload and manage tools, worksheets, code files, and references. Access restricted to Developer Mode.</p>", unsafe_allow_html=True)
        
        # Dev file upload
        with st.expander("📤 Upload Developer Reference Files", expanded=True):
            dev_file = st.file_uploader("Upload file", type=None)
            dev_desc = st.text_input("File Description", placeholder="e.g. C++ Compiler build instructions")
            if st.button("🚀 Save File to Vault", use_container_width=True):
                if dev_file is not None:
                    filepath = os.path.join("dev_uploads_store", dev_file.name)
                    with open(filepath, "wb") as f:
                        f.write(dev_file.getbuffer())
                    save_dev_upload(dev_file.name, filepath, dev_desc)
                    st.success(f"File '{dev_file.name}' saved securely! 🔒")
                    st.rerun()
                else:
                    st.error("Please upload a file.")
                    
        # Dev uploaded files list
        st.markdown("### 🔒 Secure Developer Vault Files")
        uploads = get_dev_uploads()
        if uploads:
            for item in uploads:
                filename = item["filename"]
                filepath = item["filepath"]
                description = item["description"]
                uploaded_at = item["uploaded_at"]
                
                file_exists = os.path.exists(filepath)
                
                with st.expander(f"📁 {filename}", expanded=False):
                    st.markdown(f"**Description:** {description if description else 'No description provided'}")
                    st.markdown(f"**Uploaded At:** `{uploaded_at}`")
                    st.markdown(f"**Secure File Path:** `{filepath}`")
                    
                    if file_exists:
                        with open(filepath, "rb") as f:
                            btn_data = f.read()
                        st.download_button(
                            "⬇️ Download File",
                            data=btn_data,
                            file_name=filename,
                            key=f"dev_dl_{item['id']}",
                            use_container_width=True
                        )
                    else:
                        st.error("File no longer exists on local filesystem.")
        else:
            st.info("No developer files uploaded to the vault yet.")
            
    elif choice == "🔑 Sign Out":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.is_dev = False
        st.success("Successfully logged out!")
        st.rerun()
