"""
Community/Forum page
"""
import streamlit as st
from datetime import date
from db.database import add_community_post, get_community_posts, delete_community_post, log_progress, add_badge, get_user
from utils.styles import inject_css

def show_community():
    inject_css()
    uid = st.session_state.user["id"]
    
    st.markdown("""
    <h1>👥 Community Forum</h1>
    <p style="color:#94a3b8;">Connect with other learners, share resources, and ask questions!</p>
    """, unsafe_allow_html=True)
    
    # Create new post
    with st.expander("✍️ Create New Post", expanded=False):
        with st.form("new_post_form"):
            title = st.text_input("Post Title")
            category = st.selectbox("Category", ["General", "Questions", "Resources", "Study Groups", "Career Advice"])
            content = st.text_area("Content")
            
            if st.form_submit_button("Create Post", use_container_width=True):
                if title and content:
                    add_community_post(uid, title, content, category)
                    log_progress(uid, str(date.today()), "community_post")
                    
                    # Check and award badge if needed
                    user = get_user(uid)
                    import json
                    current_badges = set(json.loads(user.get('badges', '[]')))
                    if 'community_builder' not in current_badges:
                        add_badge(uid, 'community_builder')
                        st.balloons()
                    
                    st.success("Post created!")
                    st.rerun()
                else:
                    st.error("Please provide a title and content!")
    
    # View all posts
    st.markdown("<br>### 📋 Recent Posts", unsafe_allow_html=True)
    posts = get_community_posts()
    
    if posts:
        for post in posts:
            category_color = {
                "General": "#6366f1",
                "Questions": "#f59e0b",
                "Resources": "#10b981",
                "Study Groups": "#3b82f6",
                "Career Advice": "#ec4899"
            }.get(post['category'], "#94a3b8")
            
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <h3 style="margin:0;">{post['title']}</h3>
                        <span style="padding:3px 8px; border-radius:4px; background:{category_color}; color:white; font-size:0.75rem;">{post['category']}</span>
                    </div>
                    <p style="color:#cbd5e1; margin:0 0 8px 0;">{post['content']}</p>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:0.8rem; color:#818cf8;">Posted by {post['username']} on {post['created_at'].split('T')[0]}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if post['username'] == st.session_state.user['username']:
                    if st.button("❌ Delete Post", key=f"del_post_{post['id']}"):
                        delete_community_post(post['id'])
                        st.success("Post deleted!")
                        st.rerun()
    else:
        st.info("No community posts yet! Be the first to post!")
