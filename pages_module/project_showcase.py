"""
Project Showcase page
"""
import streamlit as st
from datetime import date
from db.database import add_project, get_projects, delete_project, log_progress, add_badge, get_user
from utils.styles import inject_css

def show_project_showcase():
    inject_css()
    uid = st.session_state.user["id"]
    
    st.markdown("""
    <h1>🚀 Project Showcase</h1>
    <p style="color:#94a3b8;">Showcase your projects, share your work, and get inspired by others!</p>
    """, unsafe_allow_html=True)
    
    # Add project form
    with st.expander("➕ Add New Project", expanded=False):
        with st.form("add_project_form"):
            title = st.text_input("Project Title")
            description = st.text_area("Description")
            tech_stack = st.text_input("Tech Stack (comma separated, e.g., Python, React, PostgreSQL)")
            github_url = st.text_input("GitHub URL")
            live_url = st.text_input("Live Demo URL (optional)")
            
            if st.form_submit_button("Add Project", use_container_width=True):
                if title:
                    add_project(uid, title, description, tech_stack, github_url, live_url)
                    log_progress(uid, str(date.today()), "project_showcase")
                    
                    # Check and award badge if needed
                    user = get_user(uid)
                    import json
                    current_badges = set(json.loads(user.get('badges', '[]')))
                    if 'project_shower' not in current_badges:
                        add_badge(uid, 'project_shower')
                        st.balloons()
                    
                    st.success("Project added to showcase!")
                    st.rerun()
                else:
                    st.error("Please enter a project title!")
    
    # View all projects
    st.markdown("<br>### 🌟 All Projects", unsafe_allow_html=True)
    projects = get_projects()
    
    if projects:
        for project in projects:
            st.markdown("---")
            col_a, col_b = st.columns([3,1])
            with col_a:
                st.markdown(f"### {project['title']}")
                if project.get('description'):
                    st.markdown(f"<p style='color:#cbd5e1;'>{project['description']}</p>", unsafe_allow_html=True)
                if project.get('tech_stack'):
                    stack_tags = [f"<span style='display:inline-block; padding:4px 8px; margin:2px; background:#374151; border-radius:4px; font-size:0.8rem;'>{tag.strip()}</span>" for tag in project['tech_stack'].split(',')]
                    st.markdown(f"<div>{''.join(stack_tags)}</div>", unsafe_allow_html=True)
                
                link_col1, link_col2 = st.columns([1,1])
                with link_col1:
                    if project.get('github_url'):
                        st.markdown(f"<a href='{project['github_url']}' target='_blank' class='link-btn'>🔗 GitHub Repo</a>", unsafe_allow_html=True)
                with link_col2:
                    if project.get('live_url'):
                        st.markdown(f"<a href='{project['live_url']}' target='_blank' class='link-btn'>🌐 Live Demo</a>", unsafe_allow_html=True)
                
                st.markdown(f"<p style='font-size:0.8rem; color:#818cf8; margin-top:8px;'>By {project.get('username', 'User')} • {project['created_at'].split('T')[0]}</p>", unsafe_allow_html=True)
                
            with col_b:
                if 'username' in project and project['username'] == st.session_state.user['username']:
                    if st.button("❌ Delete", key=f"del_proj_{project['id']}", use_container_width=True):
                        delete_project(project['id'])
                        st.success("Project deleted!")
                        st.rerun()
    else:
        st.info("No projects added yet! Be the first to showcase your work!")
