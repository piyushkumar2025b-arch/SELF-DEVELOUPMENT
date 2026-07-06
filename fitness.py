"""
Fitness Tracker page
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date, timedelta
from db.database import log_fitness, get_fitness_logs, add_badge
from utils.styles import inject_css
from collections import defaultdict

WORKOUT_TYPES = [
    "🏃 Running", "💪 Weightlifting", "🧘 Yoga", "🚴 Cycling",
    "🏊 Swimming", "🥊 Boxing/MMA", "🏋️ HIIT", "🚶 Walking",
    "🧗 Rock Climbing", "⚽ Sports", "💆 Stretching", "🎯 Other",
]

def show_fitness():
    inject_css()
    uid = st.session_state.user["id"]

    st.markdown("""
    <h1>💪 Fitness Tracker</h1>
    <p style="color:#94a3b8">A healthy body fuels a sharp mind. Track your workouts alongside your coding prep.</p>
    """, unsafe_allow_html=True)

    # Log workout form
    with st.expander("➕ Log Today's Workout", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            w_date = st.date_input("Date", value=date.today(), key="fit_date")
            w_type = st.selectbox("Workout Type", WORKOUT_TYPES, key="fit_type")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=300, value=30, key="fit_dur")
            calories = st.number_input("Calories Burned (est.)", min_value=0, max_value=3000, value=200, key="fit_cal")
        with col3:
            notes = st.text_area("Notes", placeholder="How did it go?", height=100, key="fit_notes")

        if st.button("🏋️ Log Workout", use_container_width=True):
            log_fitness(uid, w_date.isoformat(), w_type, duration, calories, notes)
            st.success("Workout logged! 💪")
            logs_check = get_fitness_logs(uid)
            if len(logs_check) >= 7:
                add_badge(uid, "fitness_fan")
            st.rerun()

    # Load logs
    logs = get_fitness_logs(uid)
    if not logs:
        st.info("No workouts logged yet. Start your fitness journey!")
        return

    df = pd.DataFrame(logs)
    df["date"] = pd.to_datetime(df["date"])

    # Stats
    total_workouts = len(df)
    total_duration = df["duration_minutes"].sum()
    total_calories = df["calories"].sum()
    this_week = df[df["date"] >= pd.Timestamp(date.today() - timedelta(days=7))]

    st.markdown("### 📊 Your Stats")
    col1, col2, col3, col4 = st.columns(4)
    for col, (num, label, color) in zip([col1, col2, col3, col4], [
        (total_workouts, "Total Workouts", "#6366f1"),
        (f"{total_duration//60}h {total_duration%60}m", "Total Time", "#3b82f6"),
        (f"{total_calories:,}", "Total Calories", "#ef4444"),
        (len(this_week), "This Week", "#10b981"),
    ]):
        with col:
            st.markdown(f"""<div class="stat-chip">
              <div class="num" style="color:{color}">{num}</div>
              <div class="label">{label}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    tab1, tab2, tab3 = st.tabs(["📅 Weekly Activity", "🥧 Workout Types", "📈 Progress"])

    with tab1:
        # Last 30 days
        last30 = df[df["date"] >= pd.Timestamp(date.today() - timedelta(days=30))]
        if not last30.empty:
            daily = last30.groupby("date")["duration_minutes"].sum().reset_index()
            fig = go.Figure(go.Bar(
                x=daily["date"],
                y=daily["duration_minutes"],
                marker=dict(
                    color=daily["duration_minutes"],
                    colorscale=[[0,"#1c2444"],[0.5,"#3b82f6"],[1,"#6366f1"]],
                ),
                text=daily["duration_minutes"].apply(lambda x: f"{x}m"),
                textposition="outside",
                textfont=dict(color="#94a3b8", size=10),
            ))
            fig.update_layout(
                plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a",
                font=dict(color="#94a3b8"), height=280,
                margin=dict(l=10,r=10,t=20,b=20),
                xaxis=dict(showgrid=False, color="#94a3b8"),
                yaxis=dict(showgrid=False, zeroline=False, color="#94a3b8", title="Minutes"),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        type_counts = df.groupby("workout_type")["duration_minutes"].sum()
        if not type_counts.empty:
            fig2 = go.Figure(go.Pie(
                labels=[t.split()[-1] for t in type_counts.index],
                values=type_counts.values,
                hole=0.5,
                marker=dict(colors=["#6366f1","#3b82f6","#10b981","#f59e0b","#ef4444","#ec4899","#8b5cf6","#14b8a6","#f97316","#84cc16","#06b6d4","#a855f7"]),
                textfont=dict(color="white", size=11),
            ))
            fig2.update_layout(
                plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a",
                font=dict(color="#94a3b8"), height=280,
                margin=dict(l=20,r=20,t=20,b=20),
                legend=dict(font=dict(color="#94a3b8")),
                showlegend=True,
            )
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        monthly = df.copy()
        monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
        monthly_stats = monthly.groupby("month").agg(
            workouts=("id","count"),
            total_min=("duration_minutes","sum"),
            total_cal=("calories","sum")
        ).reset_index()

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=monthly_stats["month"], y=monthly_stats["workouts"],
            mode="lines+markers", name="Workouts",
            line=dict(color="#6366f1", width=2),
            marker=dict(size=8, color="#6366f1"),
        ))
        fig3.add_trace(go.Scatter(
            x=monthly_stats["month"], y=monthly_stats["total_min"],
            mode="lines+markers", name="Minutes",
            line=dict(color="#10b981", width=2),
            marker=dict(size=8, color="#10b981"),
            yaxis="y2",
        ))
        fig3.update_layout(
            plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a",
            font=dict(color="#94a3b8"), height=280,
            margin=dict(l=10,r=60,t=20,b=20),
            xaxis=dict(showgrid=False, color="#94a3b8"),
            yaxis=dict(showgrid=False, zeroline=False, color="#6366f1", title="Workouts"),
            yaxis2=dict(overlaying="y", side="right", showgrid=False, zeroline=False, color="#10b981", title="Minutes"),
            legend=dict(font=dict(color="#94a3b8"), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Recent workouts table
    st.markdown("### 📋 Recent Workouts")
    recent = logs[:10]
    for log in recent:
        st.markdown(f"""
        <div class="workout-card">
          <div>
            <span style="font-size:1.2rem;">{log['workout_type'].split()[0]}</span>
            <strong style="margin-left:8px;">{log['workout_type'].split(' ',1)[-1] if len(log['workout_type'].split())>1 else log['workout_type']}</strong>
            <span style="color:#64748b; font-size:0.8rem; margin-left:8px;">📅 {log['date']}</span>
          </div>
          <div style="display:flex; gap:1rem; color:#94a3b8; font-size:0.85rem;">
            <span>⏱️ {log['duration_minutes']}min</span>
            <span>🔥 {log['calories']} cal</span>
            {f'<span>💬 {log["notes"][:30]}…</span>' if log.get("notes") and len(log["notes"])>0 else ''}
          </div>
        </div>""", unsafe_allow_html=True)
