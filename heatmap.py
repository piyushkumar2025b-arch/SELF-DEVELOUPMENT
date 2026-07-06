"""
Activity Heatmap page — GitHub-style contribution calendar
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date, timedelta
from db.database import get_progress, log_progress
from utils.styles import inject_css
from collections import defaultdict

def show_heatmap():
    inject_css()
    uid = st.session_state.user["id"]

    st.markdown("""
    <h1>🔥 Activity Heatmap</h1>
    <p style="color:#94a3b8">Track your daily preparation activity across all sections.</p>
    """, unsafe_allow_html=True)

    # Manual log
    with st.expander("➕ Log Manual Activity"):
        col1, col2 = st.columns(2)
        with col1:
            act_date = st.date_input("Date", value=date.today())
            activity = st.selectbox("Activity Type", [
                "dsa_practice", "mock_interview", "system_design", "aptitude",
                "company_research", "coding_practice", "reading", "other"
            ])
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📌 Log Activity", use_container_width=True):
                log_progress(uid, act_date.isoformat(), activity)
                st.success("Activity logged!")
                st.rerun()

    # Fetch data
    logs = get_progress(uid)
    if not logs:
        st.info("No activity logged yet. Start practicing to see your heatmap!")
        _show_empty_heatmap()
        return

    # Build daily counts
    daily = defaultdict(int)
    for row in logs:
        daily[row["date"]] += row["count"]

    # Build 365-day grid
    today = date.today()
    start = today - timedelta(days=364)
    all_dates = [start + timedelta(days=i) for i in range(365)]

    # Build heatmap grid (weeks × days)
    # Pad to start on Sunday
    start_weekday = start.weekday()  # Monday=0
    pad = (start_weekday + 1) % 7    # adjust to Sunday=0
    padded = [None] * pad + all_dates
    while len(padded) % 7 != 0:
        padded.append(None)

    weeks = [padded[i:i+7] for i in range(0, len(padded), 7)]
    num_weeks = len(weeks)

    z = []
    text = []
    for day_idx in range(7):
        row_z = []
        row_t = []
        for week in weeks:
            d = week[day_idx] if day_idx < len(week) else None
            if d is None:
                row_z.append(None)
                row_t.append("")
            else:
                cnt = daily.get(d.isoformat(), 0)
                row_z.append(cnt)
                row_t.append(f"{d.strftime('%b %d, %Y')}<br>{cnt} activit{'y' if cnt==1 else 'ies'}")
        z.append(row_z)
        text.append(row_t)

    day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    # Month labels
    month_labels = []
    month_positions = []
    current_month = None
    for w_idx, week in enumerate(weeks):
        for d in week:
            if d and d.month != current_month:
                current_month = d.month
                month_labels.append(d.strftime("%b"))
                month_positions.append(w_idx)
                break

    fig = go.Figure(go.Heatmap(
        z=z,
        text=text,
        hovertemplate="%{text}<extra></extra>",
        colorscale=[
            [0.0, "#1c2444"],
            [0.01, "#1e3a5f"],
            [0.25, "#1d4ed8"],
            [0.5, "#3b82f6"],
            [0.75, "#6366f1"],
            [1.0, "#a855f7"],
        ],
        showscale=True,
        colorbar=dict(
            title="Activities",
            titlefont=dict(color="#94a3b8"),
            tickfont=dict(color="#94a3b8"),
            bgcolor="#0f1629",
            bordercolor="#1e2d52",
        ),
        xgap=2,
        ygap=2,
        zmin=0,
    ))

    fig.update_layout(
        height=200,
        plot_bgcolor="#0a0e1a",
        paper_bgcolor="#0a0e1a",
        font=dict(color="#94a3b8"),
        xaxis=dict(
            tickvals=month_positions,
            ticktext=month_labels,
            tickfont=dict(color="#94a3b8", size=11),
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            tickvals=list(range(7)),
            ticktext=day_labels,
            tickfont=dict(color="#94a3b8", size=11),
            showgrid=False,
            zeroline=False,
        ),
        margin=dict(l=40, r=20, t=20, b=30),
    )

    st.plotly_chart(fig, use_container_width=True)

    # Stats
    st.markdown("### 📊 Activity Breakdown")
    total_days = len([d for d in all_dates if daily.get(d.isoformat(), 0) > 0])
    total_acts = sum(daily.values())
    max_streak = _compute_streak(daily, all_dates)
    current_streak = _current_streak(daily)

    cols = st.columns(4)
    for col, (num, label, color) in zip(cols, [
        (total_acts, "Total Activities", "#6366f1"),
        (total_days, "Active Days", "#3b82f6"),
        (current_streak, "Current Streak 🔥", "#f59e0b"),
        (max_streak, "Best Streak", "#10b981"),
    ]):
        with col:
            st.markdown(f"""<div class="stat-chip">
              <div class="num" style="color:{color}">{num}</div>
              <div class="label">{label}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Activity type breakdown
    type_counts = defaultdict(int)
    for row in logs:
        type_counts[row["activity_type"]] += row["count"]

    if type_counts:
        df = pd.DataFrame(list(type_counts.items()), columns=["Activity", "Count"])
        df = df.sort_values("Count", ascending=True)
        fig2 = go.Figure(go.Bar(
            x=df["Count"], y=df["Activity"],
            orientation="h",
            marker=dict(
                color=df["Count"],
                colorscale=[[0, "#1c2444"], [1, "#6366f1"]],
            ),
            text=df["Count"],
            textposition="outside",
            textfont=dict(color="#94a3b8"),
        ))
        fig2.update_layout(
            plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a",
            font=dict(color="#94a3b8"),
            height=300,
            margin=dict(l=10, r=60, t=20, b=20),
            xaxis=dict(showgrid=False, zeroline=False, color="#94a3b8"),
            yaxis=dict(showgrid=False, color="#94a3b8"),
        )
        st.plotly_chart(fig2, use_container_width=True)

def _compute_streak(daily, all_dates):
    max_s = cur = 0
    for d in all_dates:
        if daily.get(d.isoformat(), 0) > 0:
            cur += 1
            max_s = max(max_s, cur)
        else:
            cur = 0
    return max_s

def _current_streak(daily):
    today = date.today()
    streak = 0
    d = today
    while daily.get(d.isoformat(), 0) > 0:
        streak += 1
        d -= timedelta(days=1)
    return streak

def _show_empty_heatmap():
    today = date.today()
    start = today - timedelta(days=364)
    all_dates = [start + timedelta(days=i) for i in range(365)]
    start_weekday = start.weekday()
    pad = (start_weekday + 1) % 7
    padded = [None] * pad + all_dates
    while len(padded) % 7 != 0:
        padded.append(None)
    weeks = [padded[i:i+7] for i in range(0, len(padded), 7)]
    z = [[0 if weeks[w][d] else None for w in range(len(weeks))] for d in range(7)]
    fig = go.Figure(go.Heatmap(z=z, colorscale=[[0,"#1c2444"],[1,"#6366f1"]],
        showscale=False, xgap=2, ygap=2))
    fig.update_layout(height=150, plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a",
        margin=dict(l=40,r=20,t=10,b=20),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, tickvals=list(range(7)),
            ticktext=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],
            tickfont=dict(color="#94a3b8", size=10)))
    st.plotly_chart(fig, use_container_width=True)
