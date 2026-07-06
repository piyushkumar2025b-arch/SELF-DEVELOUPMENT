"""
Coding Languages page — default language resources and custom resource saving
"""
import streamlit as st
from data.questions import CODING_LANGUAGES
from utils.styles import inject_css
from db.database import save_link, get_links, delete_link, add_badge

def show_languages():
    inject_css()
    uid = st.session_state.user["id"]

    st.markdown("""
    <h1>💻 Learn Coding Languages</h1>
    <p style="color:#94a3b8">Master core programming languages and build your personalized resource library.</p>
    """, unsafe_allow_html=True)

    # Add custom link section
    with st.expander("➕ Save Your Custom Resources/Links", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            link_name = st.text_input("Resource Name", placeholder="e.g. NeetCode Roadmap")
            link_url = st.text_input("Resource URL", placeholder="https://example.com")
        with col2:
            link_cat = st.selectbox("Language / Category", list(CODING_LANGUAGES.keys()) + ["General"])
            link_desc = st.text_input("Short Description (optional)", placeholder="Why is this useful?")
        
        if st.button("🔥 Save Resource", use_container_width=True):
            if not link_name.strip() or not link_url.strip():
                st.error("Name and URL are required.")
            elif not link_url.startswith("http"):
                st.error("Invalid URL. Make sure it starts with http:// or https://")
            else:
                save_link(uid, link_name.strip(), link_url.strip(), link_cat, link_desc.strip())
                st.success("Resource saved! 🚀")
                
                # Check for badge
                user_links = get_links(uid)
                if len(user_links) >= 5:
                    add_badge(uid, "link_sharer")
                st.rerun()

    # Tabs for default languages
    lang_names = list(CODING_LANGUAGES.keys())
    tabs = st.tabs([f"{CODING_LANGUAGES[l]['icon']} {l}" for l in lang_names])

    # Load custom links
    custom_links = get_links(uid)

    for i, lang in enumerate(lang_names):
        with tabs[i]:
            lang_data = CODING_LANGUAGES[lang]
            st.markdown(f"### {lang_data['icon']} {lang} Resources")
            st.markdown(f'<span class="badge badge-easy" style="font-size:0.8rem; margin-bottom:1rem;">Difficulty: {lang_data["level"]}</span>', unsafe_allow_html=True)
            
            # Default resources
            st.markdown("#### 📘 Curated Core Guides")
            for res in lang_data["resources"]:
                st.markdown(f"""
                <div class="q-item" style="margin: 6px 0;">
                  <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
                    <div>
                      <strong style="color:#f1f5f9;">{res['name']}</strong>
                    </div>
                    <a href="{res['url']}" target="_blank" class="link-btn">Open Resource 🔗</a>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Filter and show custom links for this language
            lang_custom = [cl for cl in custom_links if cl["category"] == lang]
            if lang_custom:
                st.markdown("<br>#### 📂 Your Saved Resources", unsafe_allow_html=True)
                for cl in lang_custom:
                    col_l, col_r = st.columns([4, 1])
                    with col_l:
                        desc_str = f'<div style="color:#94a3b8; font-size:0.8rem; margin-top:4px;">{cl["description"]}</div>' if cl["description"] else ""
                        st.markdown(f"""
                        <div class="q-item" style="margin: 4px 0; border-color:#818cf840;">
                          <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
                            <div>
                              <strong style="color:#818cf8;">{cl['name']}</strong>
                              {desc_str}
                            </div>
                            <a href="{cl['url']}" target="_blank" class="link-btn">Visit Link 🔗</a>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_r:
                        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️ Remove", key=f"del_link_{cl['id']}", use_container_width=True):
                            delete_link(cl["id"])
                            st.rerun()

    # General / Other category
    st.markdown("<br>---", unsafe_allow_html=True)
    st.markdown("### 🌐 General Prep & Custom Resources")
    general_custom = [cl for cl in custom_links if cl["category"] == "General"]
    if general_custom:
        for cl in general_custom:
            col_l, col_r = st.columns([4, 1])
            with col_l:
                desc_str = f'<div style="color:#94a3b8; font-size:0.8rem; margin-top:4px;">{cl["description"]}</div>' if cl["description"] else ""
                st.markdown(f"""
                <div class="q-item" style="margin: 4px 0; border-color:#10b98140;">
                  <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
                    <div>
                      <strong style="color:#10b981;">{cl['name']}</strong>
                      {desc_str}
                    </div>
                    <a href="{cl['url']}" target="_blank" class="link-btn">Visit Link 🔗</a>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            with col_r:
                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("🗑️ Remove", key=f"del_link_{cl['id']}", use_container_width=True):
                    delete_link(cl["id"])
                    st.rerun()
    else:
        st.info("No custom resources saved yet. Add your own coding prep links in the section at the top of the page.")
