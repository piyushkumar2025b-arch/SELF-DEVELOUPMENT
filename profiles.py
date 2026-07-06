"""
Coding Profiles page — GitHub, LeetCode, Codeforces live data
"""
import streamlit as st
from utils.styles import inject_css
from utils.api_helpers import (
    fetch_github_profile, fetch_github_repos, fetch_github_contributions,
    fetch_leetcode_profile,
    fetch_codeforces_profile, fetch_codeforces_submissions
)
from db.database import save_api_tokens, get_api_tokens, add_badge
import plotly.graph_objects as go

def show_profiles():
    inject_css()
    uid = st.session_state.user["id"]

    st.markdown("""
    <h1>🔌 Coding Profiles</h1>
    <p style="color:#94a3b8">Connect your accounts to see live stats from GitHub, LeetCode, and Codeforces.</p>
    """, unsafe_allow_html=True)

    # Load saved tokens
    saved = get_api_tokens(uid)

    with st.expander("⚙️ Configure Profile Handles & Tokens", expanded=not bool(saved)):
        st.markdown('<p style="color:#94a3b8; font-size:0.85rem;">Your tokens are stored securely in the local database. GitHub token is optional but needed for contribution graph.</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            github_user  = st.text_input("GitHub Username", value=saved.get("github_token","").split("|")[0] if saved else "", key="gh_user")
            github_token = st.text_input("GitHub Token (optional)", type="password",
                                          value="", placeholder="ghp_xxxxx", key="gh_tok")
            lc_user = st.text_input("LeetCode Username", value=saved.get("leetcode_username",""), key="lc_user")
        with col2:
            cf_handle = st.text_input("Codeforces Handle", value=saved.get("codeforces_handle",""), key="cf_handle")
            cc_handle = st.text_input("CodeChef Handle", value=saved.get("codechef_handle",""), key="cc_handle")

        if st.button("💾 Save & Fetch Data", use_container_width=True):
            gh_combined = f"{github_user}|{github_token}" if github_token else github_user
            save_api_tokens(uid, gh_combined, lc_user, cf_handle, cc_handle)
            add_badge(uid, "api_connected")
            st.success("Saved!")
            st.rerun()

    saved = get_api_tokens(uid)
    if not saved:
        st.info("Configure your handles above to see your stats.")
        return

    tabs = []
    tab_names = []

    gh_raw = saved.get("github_token", "")
    gh_parts = gh_raw.split("|") if "|" in gh_raw else [gh_raw, ""]
    gh_user, gh_tok = gh_parts[0], gh_parts[1] if len(gh_parts) > 1 else ""

    if gh_user:  tab_names.append("🐙 GitHub")
    if saved.get("leetcode_username"): tab_names.append("💛 LeetCode")
    if saved.get("codeforces_handle"): tab_names.append("🔵 Codeforces")

    if not tab_names:
        st.info("No handles configured yet.")
        return

    tabs = st.tabs(tab_names)
    tab_idx = 0

    # ── GitHub ──────────────────────────────────────────
    if gh_user and tab_idx < len(tabs):
        with tabs[tab_idx]:
            st.markdown("### 🐙 GitHub Profile")
            with st.spinner("Fetching GitHub data..."):
                profile = fetch_github_profile(gh_user, gh_tok)
            if profile["success"]:
                col1, col2 = st.columns([1, 3])
                with col1:
                    if profile.get("avatar"):
                        st.image(profile["avatar"], width=120)
                with col2:
                    st.markdown(f"""
                    <div class="card">
                      <h3 style="margin:0; color:#f1f5f9;">{profile['name']}</h3>
                      <p style="color:#94a3b8; margin:4px 0;">@{gh_user}</p>
                      <p style="color:#94a3b8; font-size:0.85rem;">{profile.get('bio','')}</p>
                      <div style="display:flex; gap:1rem; margin-top:8px;">
                        <span>📦 <strong>{profile['repos']}</strong> repos</span>
                        <span>👥 <strong>{profile['followers']}</strong> followers</span>
                        <span>📍 {profile.get('location','')}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

                # Repos
                with st.spinner("Fetching repos..."):
                    repos = fetch_github_repos(gh_user, gh_tok)
                if repos:
                    st.markdown("#### 📦 Recent Repositories")
                    for r in repos[:6]:
                        lang_colors = {"Python":"#3776AB","JavaScript":"#F7DF1E","TypeScript":"#3178C6",
                                       "C++":"#00599C","Java":"#ED8B00","Go":"#00ADD8","Rust":"#DEA584"}
                        lc = lang_colors.get(r.get("language",""), "#6366f1")
                        st.markdown(f"""
                        <div class="q-item">
                          <div>
                            <a href="{r['url']}" target="_blank" style="color:#60a5fa; font-weight:600; text-decoration:none;">{r['name']}</a>
                            <span style="color:#94a3b8; font-size:0.82rem; margin-left:8px;">{r.get('description','')[:60]}</span>
                            <div style="margin-top:4px;">
                              <span style="color:{lc}; font-size:0.78rem;">● {r.get('language','')}</span>
                              <span style="color:#94a3b8; font-size:0.78rem; margin-left:10px;">⭐ {r['stars']}</span>
                              <span style="color:#94a3b8; font-size:0.78rem; margin-left:10px;">📅 {r['updated']}</span>
                            </div>
                          </div>
                        </div>""", unsafe_allow_html=True)

                # Contributions
                if gh_tok:
                    with st.spinner("Fetching contributions..."):
                        contrib = fetch_github_contributions(gh_user, gh_tok)
                    if contrib.get("success"):
                        st.markdown("#### 📊 Contribution Stats")
                        c1, c2, c3, c4 = st.columns(4)
                        for col, (num, label, color) in zip([c1,c2,c3,c4], [
                            (contrib["total"], "Total Contributions", "#6366f1"),
                            (contrib["commits"], "Commits", "#3b82f6"),
                            (contrib["prs"], "Pull Requests", "#10b981"),
                            (contrib["issues"], "Issues", "#f59e0b"),
                        ]):
                            with col:
                                st.markdown(f"""<div class="stat-chip">
                                  <div class="num" style="color:{color}">{num}</div>
                                  <div class="label">{label}</div></div>""", unsafe_allow_html=True)
            else:
                st.error(f"Could not fetch GitHub data: {profile.get('message')}")
        tab_idx += 1

    # ── LeetCode ─────────────────────────────────────────
    if saved.get("leetcode_username") and tab_idx < len(tabs):
        with tabs[tab_idx]:
            lc_name = saved["leetcode_username"]
            st.markdown(f"### 💛 LeetCode: @{lc_name}")
            with st.spinner("Fetching LeetCode stats..."):
                lc = fetch_leetcode_profile(lc_name)
            if lc.get("success"):
                col1, col2 = st.columns([1, 3])
                with col1:
                    if lc.get("avatar"):
                        st.image(lc["avatar"], width=100)
                with col2:
                    st.markdown(f"""
                    <div class="card">
                      <h3 style="margin:0;">{lc.get('name', lc_name)}</h3>
                      <p style="color:#94a3b8; margin:4px 0;">🏆 Rank: #{lc['ranking']:,}</p>
                      <p style="color:#94a3b8; font-size:0.85rem;">📍 {lc.get('country','')} | 🏢 {lc.get('company','')}</p>
                      <p style="color:#94a3b8; font-size:0.85rem;">🏅 {lc['badges']} badges earned</p>
                    </div>""", unsafe_allow_html=True)

                # Problem stats
                st.markdown("#### 📊 Problems Solved")
                c1, c2, c3, c4 = st.columns(4)
                for col, (num, label, color) in zip([c1,c2,c3,c4], [
                    (lc["total"], "Total Solved", "#6366f1"),
                    (lc["easy"], "Easy", "#10b981"),
                    (lc["medium"], "Medium", "#f59e0b"),
                    (lc["hard"], "Hard", "#ef4444"),
                ]):
                    with col:
                        st.markdown(f"""<div class="stat-chip">
                          <div class="num" style="color:{color}">{num}</div>
                          <div class="label">{label}</div></div>""", unsafe_allow_html=True)

                # Donut chart
                st.markdown("<br>", unsafe_allow_html=True)
                fig = go.Figure(go.Pie(
                    labels=["Easy", "Medium", "Hard"],
                    values=[lc["easy"], lc["medium"], lc["hard"]],
                    hole=0.6,
                    marker=dict(colors=["#10b981", "#f59e0b", "#ef4444"]),
                    textfont=dict(color="white"),
                ))
                fig.update_layout(
                    showlegend=True,
                    plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a",
                    font=dict(color="#94a3b8"),
                    height=280,
                    margin=dict(l=20, r=20, t=20, b=20),
                    legend=dict(font=dict(color="#94a3b8")),
                )
                st.plotly_chart(fig, use_container_width=True)

                # Skills
                if lc.get("skills"):
                    st.markdown("#### 🔧 Skills")
                    skills_html = "".join(f'<span class="company-tag">{s}</span>' for s in lc["skills"][:15])
                    st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.error(f"Could not fetch LeetCode data: {lc.get('message')}")
        tab_idx += 1

    # ── Codeforces ────────────────────────────────────────
    if saved.get("codeforces_handle") and tab_idx < len(tabs):
        with tabs[tab_idx]:
            cf_handle = saved["codeforces_handle"]
            st.markdown(f"### 🔵 Codeforces: @{cf_handle}")
            with st.spinner("Fetching Codeforces data..."):
                cf = fetch_codeforces_profile(cf_handle)
            if cf.get("success"):
                rank_colors = {
                    "newbie": "#808080", "pupil": "#008000", "specialist": "#03a89e",
                    "expert": "#0000ff", "candidate master": "#aa00aa",
                    "master": "#ff8c00", "international master": "#ff8c00",
                    "grandmaster": "#ff0000", "international grandmaster": "#ff0000",
                    "legendary grandmaster": "#ff0000",
                }
                rc = rank_colors.get(cf.get("rank","").lower(), "#6366f1")

                c1, c2 = st.columns([1, 3])
                with c1:
                    if cf.get("avatar"):
                        st.image(cf["avatar"], width=100)
                with c2:
                    st.markdown(f"""
                    <div class="card">
                      <h3 style="margin:0;">{cf_handle}</h3>
                      <span class="badge" style="background:{rc}22; color:{rc}; border:1px solid {rc}44;">{cf.get('rank','unrated').title()}</span>
                      <p style="color:#94a3b8; margin:6px 0;">📍 {cf.get('country','')} | 🏢 {cf.get('organization','')}</p>
                      <p style="color:#94a3b8; font-size:0.85rem;">👥 {cf['friends']} friends</p>
                    </div>""", unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                for col, (num, label, color) in zip([col1, col2, col3], [
                    (cf["rating"], "Current Rating", rc),
                    (cf["max_rating"], "Max Rating", "#f59e0b"),
                    (cf["contribution"], "Contribution", "#10b981"),
                ]):
                    with col:
                        st.markdown(f"""<div class="stat-chip">
                          <div class="num" style="color:{color}">{num}</div>
                          <div class="label">{label}</div></div>""", unsafe_allow_html=True)

                # Submissions
                with st.spinner("Fetching submissions..."):
                    subs = fetch_codeforces_submissions(cf_handle)
                if subs.get("success"):
                    st.markdown("<br>#### 📊 Submission Analysis")
                    c1, c2, c3 = st.columns(3)
                    for col, (num, label, color) in zip([c1, c2, c3], [
                        (subs["total_submissions"], "Total Submissions", "#6366f1"),
                        (subs["accepted"], "Accepted", "#10b981"),
                        (subs["unique_solved"], "Unique Solved", "#f59e0b"),
                    ]):
                        with col:
                            st.markdown(f"""<div class="stat-chip">
                              <div class="num" style="color:{color}">{num}</div>
                              <div class="label">{label}</div></div>""", unsafe_allow_html=True)

                    if subs.get("tags"):
                        st.markdown("<br>#### 🏷️ Top Solved Tags")
                        tags = subs["tags"]
                        fig = go.Figure(go.Bar(
                            y=list(tags.keys()),
                            x=list(tags.values()),
                            orientation="h",
                            marker=dict(color=list(tags.values()),
                                       colorscale=[[0,"#1c2444"],[1,"#6366f1"]]),
                            text=list(tags.values()),
                            textposition="outside",
                            textfont=dict(color="#94a3b8"),
                        ))
                        fig.update_layout(
                            plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a",
                            font=dict(color="#94a3b8"), height=320,
                            margin=dict(l=10,r=40,t=10,b=10),
                            xaxis=dict(showgrid=False, zeroline=False, color="#94a3b8"),
                            yaxis=dict(showgrid=False, color="#94a3b8"),
                        )
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"Could not fetch Codeforces data: {cf.get('message')}")
        tab_idx += 1
