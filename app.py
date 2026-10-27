"""
Personal Wellness Dashboard (Next-Level Edition)
Single-User Longitudinal Behavioral Analytics, Autonomic Habit Resilience,
Bio-Digital Twin Engine & Academic Submission Dossier.
"""

from __future__ import annotations

import io
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure Root and Path resolution
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import Dashboard Core Modules
import assistant
import badges
import bio_twin
import breathwork
import calendar_heatmap
import chronotype
import clock_visualizer
import data_loader
import insights
import metrics
import personas
import report_generator
import resilience
import security
import simulation
import soundscapes
import theme
import validation
import vitality
import viva_defense


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Personal Wellness Dashboard | Next-Level Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# State Management Initialization
# ---------------------------------------------------------
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Enterprise Light"

if "goals" not in st.session_state:
    st.session_state.goals = metrics.UserGoals(
        sleep_min=7.0,
        sleep_max=9.0,
        steps_target=8000,
        water_target=8,
        activity_target=30,
    )

if "active_data_source" not in st.session_state:
    st.session_state.active_data_source = "default"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("assistant", "Hello! I am your local, deterministic Cognitive Habit Assistant. Ask me anything about your wellness data, trends, sleep consistency, or anomalies!")
    ]

# Determine dark mode boolean
is_dark = st.session_state.theme_mode != "Enterprise Light"

# Inject Global Design System CSS
theme_css = theme.get_theme_css(st.session_state.theme_mode)

# Add custom universal styles for enhanced UI aesthetics
custom_enhancements = f"""
<style>
/* Universal Visual Refinements */
.hero-container {{
    padding: 0.5rem 0 1rem 0;
}}
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
}}
.stTabs [data-baseweb="tab"] {{
    height: 46px;
    white-space: pre-wrap;
    border-radius: 8px 8px 0px 0px;
    font-size: 0.92rem;
    font-weight: 600;
    padding: 6px 14px;
}}
.stat-pill {{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 4px;
}}
.kpi-row {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: 1.2rem;
}}
.chat-bubble-user {{
    background: {'#1e293b' if is_dark else '#e0f2fe'};
    color: {'#38bdf8' if is_dark else '#0369a1'};
    border-left: 4px solid #0284c7;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 0.9rem;
}}
.chat-bubble-assistant {{
    background: {'#182230' if is_dark else '#f8fafc'};
    border: 1px solid {'#334155' if is_dark else '#e2e8f0'};
    color: {'#e2e8f0' if is_dark else '#1e293b'};
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    font-size: 0.92rem;
}}
</style>
"""
st.markdown(theme_css + custom_enhancements, unsafe_allow_html=True)


# ---------------------------------------------------------
# Sidebar: Control Center
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Control Center")
    st.caption("Personal Wellness Platform • Next-Level Edition")
    st.markdown("---")

    # 1. Theme Switcher
    st.markdown("#### 🎨 Design Theme")
    selected_theme = st.selectbox(
        "Interface Palette:",
        options=[
            "Enterprise Light",
            "Executive Dark",
            "Cyberpunk Bio-Hacker (Neon Glass)",
        ],
        index=["Enterprise Light", "Executive Dark", "Cyberpunk Bio-Hacker (Neon Glass)"].index(st.session_state.theme_mode),
        key="theme_selector",
    )
    if selected_theme != st.session_state.theme_mode:
        st.session_state.theme_mode = selected_theme
        st.rerun()

    st.markdown("---")

    # 2. Data Ingestion & Persona Switcher
    st.markdown("#### 📁 Dataset & Persona")
    dataset_option = st.selectbox(
        "Active Data Stream:",
        options=[
            "Default Sample Dataset (sample_wellness_data.csv)",
            "Persona: 🏃 Active Professional",
            "Persona: 🦉 Variable Night Owl",
            "Persona: ⚖️ Balanced Habit Tracker",
            "Upload Custom CSV File",
        ],
        index=0,
        key="data_source_selector",
    )

    uploaded_file = None
    custom_df = None

    if dataset_option == "Upload Custom CSV File":
        uploaded_file = st.file_uploader(
            "Upload CSV File:",
            type=["csv"],
            help="Schema: date, sleep_hours, steps, water_glasses, mood_score, activity_minutes",
        )
        if uploaded_file is not None:
            val_report = data_loader.load_and_validate(uploaded_file)
            if not val_report.is_valid:
                st.error("Validation Failed:")
                for err in val_report.schema_errors:
                    st.write(f"• {err}")
            else:
                custom_df = val_report.valid_df
                st.success(f"Loaded {val_report.valid_count} valid records!")
                if val_report.invalid_count > 0:
                    st.warning(f"Skipped {val_report.invalid_count} invalid rows.")
                if val_report.warnings:
                    with st.expander("Validation Warnings"):
                        for w in val_report.warnings:
                            st.caption(f"⚠️ {w}")
        
        # Download blank template
        st.download_button(
            label="📥 Download CSV Template",
            data=data_loader.get_csv_template(),
            file_name="wellness_template.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # Resolve active dataframe
    if dataset_option == "Persona: 🏃 Active Professional":
        raw_df = personas.generate_persona_dataset("active")
        active_persona_title = "Active Professional"
    elif dataset_option == "Persona: 🦉 Variable Night Owl":
        raw_df = personas.generate_persona_dataset("night_owl")
        active_persona_title = "Variable Night Owl"
    elif dataset_option == "Persona: ⚖️ Balanced Habit Tracker":
        raw_df = personas.generate_persona_dataset("balanced")
        active_persona_title = "Balanced Habit Tracker"
    elif dataset_option == "Upload Custom CSV File" and custom_df is not None:
        raw_df = custom_df
        active_persona_title = "Custom User Data"
    else:
        raw_df = data_loader.load_csv_data()
        active_persona_title = "Standard Benchmark Dataset"

    # Ensure date column is datetime
    if "date" in raw_df.columns:
        raw_df["date"] = pd.to_datetime(raw_df["date"])

    st.markdown("---")

    # 3. Global Date Range Filter
    st.markdown("#### 📅 Temporal Range Filter")
    if not raw_df.empty and "date" in raw_df.columns:
        min_avail_date = raw_df["date"].min().date()
        max_avail_date = raw_df["date"].max().date()

        date_col1, date_col2 = st.columns(2)
        with date_col1:
            start_date_input = st.date_input("Start Date", value=min_avail_date, min_value=min_avail_date, max_value=max_avail_date)
        with date_col2:
            end_date_input = st.date_input("End Date", value=max_avail_date, min_value=min_avail_date, max_value=max_avail_date)

        # Quick range shortcuts
        p1, p2, p3 = st.columns(3)
        if p1.button("All", use_container_width=True):
            start_date_input = min_avail_date
            end_date_input = max_avail_date
        if p2.button("30D", use_container_width=True):
            start_date_input = max(min_avail_date, max_avail_date - timedelta(days=30))
        if p3.button("14D", use_container_width=True):
            start_date_input = max(min_avail_date, max_avail_date - timedelta(days=14))

        df_filtered = metrics.filter_by_date_range(raw_df, start_date_input, end_date_input)
    else:
        df_filtered = raw_df.copy()
        start_date_input = None
        end_date_input = None

    st.markdown("---")

    # 4. Personal Targets & Habit Goals
    with st.expander("🎯 Target Calibration", expanded=False):
        sleep_min_val = st.slider("Min Sleep (hrs)", 4.0, 9.0, float(st.session_state.goals.sleep_min), 0.5)
        sleep_max_val = st.slider("Max Sleep (hrs)", 7.0, 12.0, float(st.session_state.goals.sleep_max), 0.5)
        steps_target_val = st.slider("Steps Target", 4000, 20000, int(st.session_state.goals.steps_target), 500)
        water_target_val = st.slider("Water Target (gls)", 4, 16, int(st.session_state.goals.water_target), 1)
        activity_target_val = st.slider("Activity Target (mins)", 10, 120, int(st.session_state.goals.activity_target), 5)

        st.session_state.goals = metrics.UserGoals(
            sleep_min=sleep_min_val,
            sleep_max=sleep_max_val,
            steps_target=steps_target_val,
            water_target=water_target_val,
            activity_target=activity_target_val,
        )

    st.markdown("---")

    # 5. Focus Soundscapes Generator Widget
    soundscapes.render_focus_soundscapes_widget()

    st.markdown("---")

    # 6. Session Security & Privacy Vault Badge
    sec_audit = security.audit_session_security(df_filtered)
    st.markdown(
        f"""
        <div style="font-size: 0.76rem; color: {'#94a3b8' if is_dark else '#64748b'}; line-height: 1.4;">
            <strong>🔒 Pervasive Privacy Vault</strong><br>
            • SHA-256: <code>{sec_audit.dataset_sha256[:12]}...</code><br>
            • State: <span style="color: #10b981;">{sec_audit.data_sovereignty_status}</span><br>
            • External Telemetry Beacons: <b>0</b>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Core Analytics Calculations
# ---------------------------------------------------------
goals = st.session_state.goals
stats = metrics.calculate_dashboard_stats(df_filtered, start_date_input, end_date_input)
comp = metrics.calculate_composite_score(df_filtered, goals)
streaks = metrics.calculate_habit_streaks(df_filtered, goals)
weekend_stats = metrics.calculate_weekday_vs_weekend_stats(df_filtered)
resilience_rep = resilience.calculate_autonomic_resiliency(df_filtered, goals)
vitality_rep = vitality.calculate_vitality_forecast(df_filtered, goals)
trend_report = insights.generate_trend_observations(df_filtered)
badges_list = badges.evaluate_achievement_badges(df_filtered, goals)
anomalies_df = validation.detect_anomalies(df_filtered)
chronotype_rep = chronotype.calculate_circadian_chronotype(df_filtered)


# ---------------------------------------------------------
# Main Application Header
# ---------------------------------------------------------
st.markdown('<div class="hero-container">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap;">
        <div>
            <div class="main-header">Personal Wellness Dashboard</div>
            <div class="sub-header">Longitudinal Behavioral Analytics, Autonomic Resilience & Bio-Digital Twin Engine</div>
        </div>
        <div style="text-align: right; margin-bottom: 1rem;">
            <span style="background: {'#1e293b' if is_dark else '#f1f5f9'}; border: 1px solid {'#334155' if is_dark else '#cbd5e1'}; padding: 5px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600;">
                📊 Stream: <b>{active_persona_title}</b> ({len(df_filtered)} records)
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Mandatory Non-Medical Educational Disclaimer
st.markdown(
    """
    <div class="disclaimer-banner">
        <strong>⚠️ Non-Medical Academic & Educational Demonstration:</strong>
        This analytics platform is engineered exclusively for single-user behavioral tracking and academic data science evaluation.
        It does not diagnose, treat, prevent, or monitor clinical health conditions. All algorithms utilize transparent, rule-based mathematical models.
    </div>
    """,
    unsafe_allow_html=True,
)

# Autonomic Resilience Banner
st.markdown(
    f"""
    <div class="resilience-banner">
        <strong>🛡️ Autonomic Habit Resilience: {resilience_rep.autonomic_health_status}</strong> &nbsp;|&nbsp;
        Habit Availability / Uptime: <b>{resilience_rep.uptime_pct:.1f}%</b> ({resilience_rep.successful_days}/{resilience_rep.total_active_days} days) &nbsp;|&nbsp;
        Mean Time to Recovery (MTTR): <b>{resilience_rep.mean_time_to_recovery_days:.1f} days</b>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# Primary Navigation Tabs
# ---------------------------------------------------------
tab_cockpit, tab_trends, tab_twin, tab_sim, tab_badges, tab_breath, tab_assistant, tab_report, tab_viva = st.tabs([
    "📊 Cockpit",
    "📈 Trends & Analytics",
    "🧬 Bio-Digital Twin",
    "🔮 What-If Simulator",
    "🏆 Milestones & Badges",
    "🧘 Breathwork Sync",
    "💬 Z-Assistant",
    "📄 Dossier & Export",
    "🎓 Viva Voce & Defense",
])


# =========================================================
# TAB 1: EXECUTIVE COCKPIT
# =========================================================
with tab_cockpit:
    if stats is None or df_filtered.empty:
        st.warning("No records found in the selected date range. Please broaden the date filter or load dataset.")
    else:
        # Hero KPI Cards
        avg_sleep = stats.sleep_summary.mean or 0.0
        avg_steps = int(stats.steps_summary.mean or 0)
        avg_water = stats.water_summary.mean or 0.0
        avg_mood = stats.mood_summary.mean if stats.mood_summary else None
        tot_activity = int(stats.activity_summary.total or 0) if stats.activity_summary else None

        sleep_delta_str = f"Target: {goals.sleep_min}–{goals.sleep_max}h"
        steps_delta_str = f"Target: ≥{goals.steps_target:,}"
        water_delta_str = f"Target: ≥{goals.water_target} gls"

        st.markdown(
            f"""
            <div class="kpi-row">
                <div class="metric-card">
                    <div class="metric-title">🛌 Sleep Duration</div>
                    <div class="metric-value">{avg_sleep:.1f} <span style="font-size: 1rem; font-weight: 500;">hrs/day</span></div>
                    <div class="metric-sub">{sleep_delta_str}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">🚶 Physical Activity</div>
                    <div class="metric-value">{avg_steps:,} <span style="font-size: 1rem; font-weight: 500;">steps</span></div>
                    <div class="metric-sub">{steps_delta_str}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">💧 Cellular Hydration</div>
                    <div class="metric-value">{avg_water:.1f} <span style="font-size: 1rem; font-weight: 500;">glasses</span></div>
                    <div class="metric-sub">{water_delta_str}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">🧠 Subjective Mood</div>
                    <div class="metric-value">{(f"{avg_mood:.1f} / 5.0" if avg_mood else "N/A")}</div>
                    <div class="metric-sub">Self-Reported Balance</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">📋 Logging Discipline</div>
                    <div class="metric-value">{stats.completion_rate_pct:.0f}%</div>
                    <div class="metric-sub">{stats.recorded_days_count} of {stats.total_days_in_range} days</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Composite Score & Habit Streaks Row
        c_left, c_right = st.columns([1.1, 1.2])

        with c_left:
            st.markdown("#### 🎯 Composite Behavioral Consistency Index (BCI)")
            st.caption("Weighted adherence across 4 orthogonal habit pillars (Sleep 30%, Steps 30%, Water 20%, Logging 20%).")

            # Circular / Progress Gauge Representation
            comp_color = comp.tier_color
            st.markdown(
                f"""
                <div style="background: {'#182230' if is_dark else '#ffffff'}; border: 1px solid {'#334155' if is_dark else '#e2e8f0'}; border-radius: 12px; padding: 18px 20px; text-align: center;">
                    <div style="font-size: 3.2rem; font-weight: 800; color: {comp_color}; font-family: 'JetBrains Mono', 'Fira Code', monospace;">
                        {comp.overall_score} <span style="font-size: 1.5rem; color: {'#94a3b8' if is_dark else '#64748b'};">/ 100</span>
                    </div>
                    <div style="display: inline-block; background: {comp_color}22; color: {comp_color}; border: 1px solid {comp_color}66; border-radius: 16px; padding: 4px 14px; font-weight: 700; font-size: 0.88rem; margin-bottom: 12px;">
                        {comp.tier}
                    </div>
                    <div style="font-size: 0.85rem; color: {'#cbd5e1' if is_dark else '#475569'}; margin-bottom: 16px;">
                        {comp.summary_text}
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; text-align: left; font-size: 0.8rem;">
                        <div style="background: {'#0f172a' if is_dark else '#f8fafc'}; padding: 8px 10px; border-radius: 6px;">
                            💤 Sleep Adherence: <b>{comp.sleep_score}%</b>
                        </div>
                        <div style="background: {'#0f172a' if is_dark else '#f8fafc'}; padding: 8px 10px; border-radius: 6px;">
                            🚶 Steps Fulfillment: <b>{comp.steps_score}%</b>
                        </div>
                        <div style="background: {'#0f172a' if is_dark else '#f8fafc'}; padding: 8px 10px; border-radius: 6px;">
                            💧 Hydration Target: <b>{comp.water_score}%</b>
                        </div>
                        <div style="background: {'#0f172a' if is_dark else '#f8fafc'}; padding: 8px 10px; border-radius: 6px;">
                            📅 Habit Uptime: <b>{comp.logging_score}%</b>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c_right:
            st.markdown("#### 🔥 Active Consecutive Habit Streaks")
            st.caption("Longitudinal momentum benchmarks based on uninterrupted daily target fulfillment.")

            for m_key, s_info in streaks.items():
                icon = "🚶" if "Steps" in s_info.metric_name else ("🛌" if "Sleep" in s_info.metric_name else "💧")
                ratio_pct = min(100, int((s_info.current_streak / max(1, s_info.longest_streak)) * 100))
                st.markdown(
                    f"""
                    <div style="background: {'#182230' if is_dark else '#ffffff'}; border: 1px solid {'#334155' if is_dark else '#e2e8f0'}; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <div style="font-weight: 700; font-size: 0.95rem; color: {'#f8fafc' if is_dark else '#0f172a'};">
                                {icon} {s_info.metric_name}
                            </div>
                            <div style="font-weight: 800; font-size: 1.15rem; color: #0284c7; font-family: 'JetBrains Mono', 'Fira Code', monospace;">
                                {s_info.current_streak} <span style="font-size: 0.8rem; font-weight: 500; color: {'#94a3b8' if is_dark else '#64748b'};">days active</span>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.78rem; color: {'#94a3b8' if is_dark else '#64748b'}; margin-bottom: 6px;">
                            <span>Criteria: {s_info.target_description}</span>
                            <span>Personal Record: <b>{s_info.longest_streak} days</b></span>
                        </div>
                        <div style="background: {'#0f172a' if is_dark else '#f1f5f9'}; height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #0284c7, #10b981); width: {ratio_pct}%; height: 100%;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Habit Vitality & Next-Day Readiness Forecast
        if vitality_rep:
            st.markdown("---")
            st.markdown("#### ⚡ Habit Vitality & Next-Day Readiness Outlook")
            v_col1, v_col2 = st.columns([1, 2])
            with v_col1:
                st.markdown(
                    f"""
                    <div style="background: {'#182230' if is_dark else '#ffffff'}; border: 1px solid {'#334155' if is_dark else '#e2e8f0'}; border-radius: 10px; padding: 14px 16px; text-align: center;">
                        <div style="font-size: 0.78rem; text-transform: uppercase; color: {'#94a3b8' if is_dark else '#64748b'};">Readiness Index</div>
                        <div style="font-size: 2.5rem; font-weight: 800; color: {vitality_rep.zone_color}; font-family: 'JetBrains Mono', 'Fira Code', monospace;">
                            {vitality_rep.vitality_score}
                        </div>
                        <div style="font-weight: 700; color: {vitality_rep.zone_color}; font-size: 0.9rem;">
                            {vitality_rep.momentum_zone}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with v_col2:
                st.markdown(
                    f"""
                    <div style="background: {'#182230' if is_dark else '#ffffff'}; border: 1px solid {'#334155' if is_dark else '#e2e8f0'}; border-radius: 10px; padding: 14px 18px;">
                        <div style="font-weight: 600; font-size: 0.9rem; color: {'#f8fafc' if is_dark else '#0f172a'}; margin-bottom: 6px;">
                            🧭 Prospective Behavioral Guidance:
                        </div>
                        <div style="font-size: 0.86rem; color: {'#cbd5e1' if is_dark else '#334155'}; line-height: 1.5; margin-bottom: 8px;">
                            {vitality_rep.readiness_outlook}
                        </div>
                        <div style="font-size: 0.8rem; color: {'#94a3b8' if is_dark else '#64748b'};">
                            <b>Recent Drivers:</b> {' • '.join(vitality_rep.key_drivers)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# =========================================================
# TAB 2: TRENDS & LONGITUDINAL ANALYTICS
# =========================================================
with tab_trends:
    st.markdown("### 📈 Longitudinal Biometric Evolution & Time-Series")
    st.caption("Smoothing raw day-to-day variance using 7-day backward moving averages.")

    if not df_filtered.empty and "date" in df_filtered.columns:
        df_rolling = metrics.add_rolling_averages(df_filtered, window=7)

        # Plotly Time-Series with SMA
        metric_choice = st.selectbox(
            "Select Metric to Inspect:",
            options=["Daily Steps", "Sleep Hours", "Water Glasses", "Mood Score"],
            index=0,
            key="ts_metric_choice",
        )

        col_map = {
            "Daily Steps": ("steps", "steps_rolling_7d", "Steps", "#38bdf8", goals.steps_target),
            "Sleep Hours": ("sleep_hours", "sleep_hours_rolling_7d", "Hours", "#818cf8", goals.sleep_min),
            "Water Glasses": ("water_glasses", "water_glasses_rolling_7d", "Glasses", "#34d399", goals.water_target),
            "Mood Score": ("mood_score", "mood_score_rolling_7d", "Score (1-5)", "#fbbf24", 3.0),
        }

        raw_col, roll_col, y_label, stroke_color, target_ref = col_map[metric_choice]

        if raw_col in df_rolling.columns:
            fig_ts = go.Figure()

            # Raw points
            fig_ts.add_trace(
                go.Scatter(
                    x=df_rolling["date"],
                    y=df_rolling[raw_col],
                    mode="markers",
                    name="Daily Raw Record",
                    marker=dict(color=stroke_color, size=6, opacity=0.45),
                    hovertemplate="%{x|%b %d, %Y}<br>Value: %{y}<extra></extra>",
                )
            )

            # Rolling SMA Line
            fig_ts.add_trace(
                go.Scatter(
                    x=df_rolling["date"],
                    y=df_rolling[roll_col],
                    mode="lines",
                    name="7-Day Rolling Trendline (SMA)",
                    line=dict(color=stroke_color, width=3),
                    hovertemplate="%{x|%b %d, %Y}<br>7d Trend: %{y:.1f}<extra></extra>",
                )
            )

            # Target Baseline Reference Line
            fig_ts.add_hline(
                y=target_ref,
                line_dash="dash",
                line_color="#10b981" if is_dark else "#059669",
                annotation_text=f"Target Baseline ({target_ref})",
                annotation_position="bottom right",
                annotation_font=dict(color="#10b981", size=10),
            )

            fig_ts.update_layout(
                title=dict(text=f"Longitudinal Trajectory: {metric_choice}", font=dict(color="#f8fafc" if is_dark else "#0f172a", size=14)),
                xaxis=dict(gridcolor="#334155" if is_dark else "#e2e8f0", tickfont=dict(color="#94a3b8" if is_dark else "#64748b")),
                yaxis=dict(title=y_label, gridcolor="#334155" if is_dark else "#e2e8f0", tickfont=dict(color="#94a3b8" if is_dark else "#64748b")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#94a3b8" if is_dark else "#64748b")),
                height=340,
                margin=dict(l=20, r=20, t=50, b=30),
            )
            st.plotly_chart(fig_ts, use_container_width=True)

        st.markdown("---")

        # GitHub-Style Activity Contribution Heatmap Grid
        st.markdown("#### 🟩 GitHub-Style Habit Contribution Heatmap")
        st.caption("Visualizing holistic daily target fulfillment across weeks and days.")
        fig_heat = calendar_heatmap.build_habit_calendar_heatmap(df_filtered, goals)
        st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown("---")

        # Circadian Clock Dial & Chronotype Analysis
        st.markdown("#### ⏰ Circadian Rhythm & 24-Hour Polar Clock")
        c_clock1, c_clock2 = st.columns([1, 1.2])

        with c_clock1:
            avg_sleep_val = stats.sleep_summary.mean or 7.5
            is_we_shifted = weekend_stats is not None and abs(weekend_stats.sleep_diff) >= 1.0
            fig_polar = clock_visualizer.build_circadian_polar_clock(avg_sleep_val, is_we_shifted)
            st.plotly_chart(fig_polar, use_container_width=True)

        with c_clock2:
            if chronotype_rep:
                st.markdown(
                    f"""
                    <div style="background: {'#182230' if is_dark else '#ffffff'}; border: 1px solid {'#334155' if is_dark else '#e2e8f0'}; border-radius: 10px; padding: 18px 20px;">
                        <div style="font-size: 1.3rem; font-weight: 700; color: {'#38bdf8' if is_dark else '#0284c7'}; margin-bottom: 6px;">
                            {chronotype_rep.chronotype_icon} Chronotype: {chronotype_rep.chronotype}
                        </div>
                        <div style="font-size: 0.88rem; color: {'#cbd5e1' if is_dark else '#475569'}; margin-bottom: 12px;">
                            {chronotype_rep.description}
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.82rem;">
                            <div style="background: {'#0f172a' if is_dark else '#f8fafc'}; padding: 10px; border-radius: 6px;">
                                🛌 Weekday Sleep: <b>{chronotype_rep.weekday_sleep_avg:.1f}h</b><br>
                                🏖️ Weekend Sleep: <b>{chronotype_rep.weekend_sleep_avg:.1f}h</b>
                            </div>
                            <div style="background: {'#0f172a' if is_dark else '#f8fafc'}; padding: 10px; border-radius: 6px;">
                                ✈️ Social Jetlag: <b>{chronotype_rep.social_jetlag_minutes} mins</b><br>
                                🎯 Circadian Alignment: <b>{chronotype_rep.circadian_alignment_score}/100</b>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("Log at least 7 days with both weekdays and weekends to compute Circadian Chronotype.")

        st.markdown("---")

        # Weekday vs Weekend Behavioral Split & Correlation Heatmap
        c_split1, c_split2 = st.columns([1.1, 1.1])

        with c_split1:
            st.markdown("#### 📅 Weekday vs. Weekend Behavioral Split")
            if weekend_stats:
                st.markdown(
                    f"""
                    <div style="background: {'#182230' if is_dark else '#ffffff'}; border: 1px solid {'#334155' if is_dark else '#e2e8f0'}; border-radius: 10px; padding: 14px 18px;">
                        <table style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="border-bottom: 1px solid {'#334155' if is_dark else '#e2e8f0'}; color: {'#94a3b8' if is_dark else '#64748b'};">
                                    <th style="text-align: left; padding: 6px 0;">Habit Metric</th>
                                    <th style="text-align: center;">Mon–Fri</th>
                                    <th style="text-align: center;">Sat–Sun</th>
                                    <th style="text-align: right;">Difference</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="border-bottom: 1px solid {'#33415522' if is_dark else '#f1f5f9'};">
                                    <td style="padding: 8px 0;">🛌 Sleep Duration</td>
                                    <td style="text-align: center;">{weekend_stats.weekday_sleep_avg:.1f}h</td>
                                    <td style="text-align: center;">{weekend_stats.weekend_sleep_avg:.1f}h</td>
                                    <td style="text-align: right; color: {'#38bdf8' if weekend_stats.sleep_diff >= 0 else '#fb7185'};">
                                        {'+' if weekend_stats.sleep_diff > 0 else ''}{weekend_stats.sleep_diff:.1f}h
                                    </td>
                                </tr>
                                <tr style="border-bottom: 1px solid {'#33415522' if is_dark else '#f1f5f9'};">
                                    <td style="padding: 8px 0;">🚶 Daily Steps</td>
                                    <td style="text-align: center;">{weekend_stats.weekday_steps_avg:,}</td>
                                    <td style="text-align: center;">{weekend_stats.weekend_steps_avg:,}</td>
                                    <td style="text-align: right; color: {'#38bdf8' if weekend_stats.steps_diff >= 0 else '#fb7185'};">
                                        {'+' if weekend_stats.steps_diff > 0 else ''}{weekend_stats.steps_diff:,}
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0;">💧 Hydration</td>
                                    <td style="text-align: center;">{weekend_stats.weekday_water_avg:.1f} gls</td>
                                    <td style="text-align: center;">{weekend_stats.weekend_water_avg:.1f} gls</td>
                                    <td style="text-align: right; color: {'#38bdf8' if weekend_stats.water_diff >= 0 else '#fb7185'};">
                                        {'+' if weekend_stats.water_diff > 0 else ''}{weekend_stats.water_diff:.1f} gls
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.caption("Record records spanning both weekdays and weekend days to view comparative split.")

        with c_split2:
            st.markdown("#### 🔗 Bivariate Pearson Correlation Matrix")
            corr_matrix = metrics.calculate_correlation_matrix(df_filtered)
            if not corr_matrix.empty:
                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale="Blues" if not is_dark else "Cividis",
                )
                fig_corr.update_layout(
                    height=240,
                    margin=dict(l=10, r=10, t=20, b=20),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#94a3b8" if is_dark else "#64748b", size=10),
                )
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.caption("Need at least 5 records to calculate correlation matrix.")

        st.markdown("---")

        # Rule-Based Trend Observations
        st.markdown("#### 🔍 Rule-Based Longitudinal Observations")
        st.caption("Deterministic mathematical period comparisons (Non-clinical).")

        if trend_report.has_sufficient_data:
            if trend_report.earlier_period_dates and trend_report.recent_period_dates:
                st.caption(f"Comparing earlier period ({trend_report.earlier_period_dates}) against recent period ({trend_report.recent_period_dates})")

            for obs in trend_report.observations:
                tag_color = "#10b981" if obs.tag == "Increase" else ("#f59e0b" if obs.tag == "Decrease" else "#38bdf8")
                st.markdown(
                    f"""
                    <div style="background: {'#182230' if is_dark else '#ffffff'}; border-left: 4px solid {tag_color}; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="font-weight: 700; font-size: 0.88rem; color: {'#f8fafc' if is_dark else '#0f172a'};">{obs.category}</span>
                            <span style="font-size: 0.75rem; font-weight: 700; color: {tag_color}; text-transform: uppercase;">{obs.tag}</span>
                        </div>
                        <div style="font-size: 0.82rem; color: {'#cbd5e1' if is_dark else '#475569'}; margin-top: 4px;">{obs.detail}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info(trend_report.status_message)

        # Statistical Anomaly Log
        st.markdown("---")
        st.markdown("#### 🚨 Statistical Anomaly & Outlier Log (IQR × 2.0)")
        if not anomalies_df.empty:
            st.dataframe(anomalies_df, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No statistical outliers detected within the active date range.")


# =========================================================
# TAB 3: BIO-DIGITAL TWIN & 3D PHASE SPACE
# =========================================================
with tab_twin:
    st.markdown("### 🧬 Bio-Digital Twin & Phase Space Dynamics")
    st.caption("Mathematical projections of biological vitality, attractor state spaces, and habit momentum physics.")

    if not df_filtered.empty and len(df_filtered) >= 3:
        # 3D Habit Phase Orbit Chart
        fig_3d = bio_twin.build_3d_habit_orbit_chart(df_filtered, goals, dark_mode=is_dark)
        st.plotly_chart(fig_3d, use_container_width=True)

        st.markdown("---")

        # Biological Age Delta & Neuro-Momentum Row
        bio_age_rep = bio_twin.calculate_biological_age(df_filtered, chronological_age=21.0)
        neuro_rep = bio_twin.calculate_neuro_momentum(df_filtered, goals)

        twin_c1, twin_c2 = st.columns([1, 1])

        with twin_c1:
            st.markdown("#### ⏳ Biological Vitality Age Projection")
            st.caption("Longitudinal biometric delta relative to chronological baseline (21.0 yrs).")

            delta_sign = "+" if bio_age_rep.age_delta > 0 else ""
            st.markdown(
                f"""
                <div style="background: {'#182230' if is_dark else '#ffffff'}; border: 1px solid {'#334155' if is_dark else '#e2e8f0'}; border-radius: 12px; padding: 18px 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div>
                            <div style="font-size: 0.78rem; color: {'#94a3b8' if is_dark else '#64748b'}; text-transform: uppercase;">Estimated Vitality Age</div>
                            <div style="font-size: 2.6rem; font-weight: 800; color: {bio_age_rep.status_color}; font-family: 'JetBrains Mono', 'Fira Code', monospace;">
                                {bio_age_rep.biological_age:.1f} <span style="font-size: 1rem; color: {'#94a3b8' if is_dark else '#64748b'};">yrs</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.1rem; font-weight: 800; color: {bio_age_rep.status_color};">
                                {delta_sign}{bio_age_rep.age_delta:.1f} yrs
                            </div>
                            <div style="font-size: 0.78rem; color: {'#94a3b8' if is_dark else '#64748b'};">{bio_age_rep.status_label}</div>
                        </div>
                    </div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: {'#f8fafc' if is_dark else '#0f172a'}; margin-bottom: 8px;">
                        Biometric Impact Contributions:
                    </div>
                    {''.join([f'<div style="display: flex; justify-content: space-between; font-size: 0.78rem; padding: 4px 0; border-bottom: 1px solid {"#33415533" if is_dark else "#f1f5f9"}; color: {"#cbd5e1" if is_dark else "#475569"};"><span>{k}</span><b style="color: {"#10b981" if v < 0 else "#fb7185"};">{"+" if v > 0 else ""}{v:.1f} yrs</b></div>' for k, v in bio_age_rep.breakdown.items()])}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with twin_c2:
            st.markdown("#### ⚡ Neuro-Momentum Newtonian Kinematics")
            st.caption("Quantifying habit momentum using mass (streak length) × velocity (target adherence).")

            esc_status = "🚀 Escape Velocity Achieved!" if neuro_rep.escape_velocity_achieved else "⏳ Sub-Orbital Routine Momentum"
            esc_color = "#10b981" if neuro_rep.escape_velocity_achieved else "#f59e0b"

            st.markdown(
                f"""
                <div style="background: {'#182230' if is_dark else '#ffffff'}; border: 1px solid {'#334155' if is_dark else '#e2e8f0'}; border-radius: 12px; padding: 18px 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div>
                            <div style="font-size: 0.78rem; color: {'#94a3b8' if is_dark else '#64748b'}; text-transform: uppercase;">Momentum Index</div>
                            <div style="font-size: 2.6rem; font-weight: 800; color: {neuro_rep.status_color}; font-family: 'JetBrains Mono', 'Fira Code', monospace;">
                                {neuro_rep.momentum_score:.0f} <span style="font-size: 1rem; color: {'#94a3b8' if is_dark else '#64748b'};">/ 100</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.88rem; font-weight: 700; color: {esc_color};">
                                {esc_status}
                            </div>
                            <div style="font-size: 0.76rem; color: {'#94a3b8' if is_dark else '#64748b'};">{neuro_rep.status_title}</div>
                        </div>
                    </div>
                    <div style="font-size: 0.83rem; color: {'#cbd5e1' if is_dark else '#475569'}; margin-bottom: 12px; line-height: 1.4;">
                        {neuro_rep.explanation}
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.78rem;">
                        <div style="background: {'#0f172a' if is_dark else '#f8fafc'}; padding: 6px 10px; border-radius: 6px;">
                            Inertia Mass: <b>{neuro_rep.inertia_mass} streak days</b>
                        </div>
                        <div style="background: {'#0f172a' if is_dark else '#f8fafc'}; padding: 6px 10px; border-radius: 6px;">
                            Compliance Velocity: <b>{neuro_rep.velocity_rate * 100:.0f}%</b>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Record at least 3 days of data to construct the 3D Bio-Digital Twin and state space orbit.")


# =========================================================
# TAB 4: WHAT-IF ROUTINE SIMULATOR
# =========================================================
with tab_sim:
    st.markdown("### 🔮 What-If Routine Scenario Simulator")
    st.caption("Hypothetical behavioral modeling: Simulate how adjustments to sleep, steps, or hydration impact your Composite Index and Habit Uptime.")

    sim_c1, sim_c2 = st.columns([1, 1.2])

    with sim_c1:
        st.markdown("#### 🎛️ Configure Routine Adjustments:")
        delta_sleep_val = st.slider("Sleep Adjustment (hrs/night)", -2.0, 2.0, 0.5, 0.25)
        delta_steps_val = st.slider("Physical Steps Adjustment (steps/day)", -5000, 5000, 1500, 500)
        delta_water_val = st.slider("Hydration Adjustment (glasses/day)", -4, 4, 1, 1)

    with sim_c2:
        st.markdown("#### 📊 Projected Outcome Analysis:")
        sim_res = simulation.simulate_routine_tweak(
            df_filtered,
            delta_sleep=delta_sleep_val,
            delta_steps=delta_steps_val,
            delta_water=delta_water_val,
            goals=goals,
        )

        if sim_res:
            score_diff = sim_res.composite_gain
            diff_color = "#10b981" if score_diff > 0 else ("#fb7185" if score_diff < 0 else "#94a3b8")
            diff_sign = "+" if score_diff > 0 else ""

            st.markdown(
                f"""
                <div style="background: {'#182230' if is_dark else '#ffffff'}; border: 1px solid {'#334155' if is_dark else '#e2e8f0'}; border-radius: 12px; padding: 18px 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                        <div>
                            <div style="font-size: 0.78rem; text-transform: uppercase; color: {'#94a3b8' if is_dark else '#64748b'};">Projected Composite Index</div>
                            <div style="font-size: 2.5rem; font-weight: 800; color: {'#38bdf8' if is_dark else '#0284c7'}; font-family: 'JetBrains Mono', 'Fira Code', monospace;">
                                {sim_res.projected_composite} <span style="font-size: 1.1rem; color: {diff_color};">({diff_sign}{score_diff} pts)</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.78rem; text-transform: uppercase; color: {'#94a3b8' if is_dark else '#64748b'};">Baseline Index</div>
                            <div style="font-size: 1.8rem; font-weight: 700; color: {'#cbd5e1' if is_dark else '#475569'}; font-family: 'JetBrains Mono', 'Fira Code', monospace;">
                                {sim_res.baseline_composite}
                            </div>
                        </div>
                    </div>
                    <div style="background: {'#0f172a' if is_dark else '#f8fafc'}; border-radius: 8px; padding: 12px 14px; margin-bottom: 12px;">
                        <div style="font-size: 0.85rem; color: {'#e2e8f0' if is_dark else '#1e293b'}; font-weight: 600;">
                            Tier Projection: <span style="color: #10b981;">{sim_res.projected_tier}</span>
                        </div>
                        <div style="font-size: 0.82rem; color: {'#94a3b8' if is_dark else '#64748b'}; margin-top: 4px;">
                            Projected Uptime: <b>{sim_res.projected_uptime:.1f}%</b> ({'+' if sim_res.uptime_gain >= 0 else ''}{sim_res.uptime_gain:.1f}%)
                        </div>
                    </div>
                    <div style="font-size: 0.85rem; color: {'#cbd5e1' if is_dark else '#334155'}; line-height: 1.5;">
                        💡 <b>Analytical Projection:</b> {sim_res.impact_summary}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("Load wellness records to run behavioral scenario simulations.")


# =========================================================
# TAB 5: GAMIFIED MILESTONES & BADGES
# =========================================================
with tab_badges:
    st.markdown("### 🏆 Gamified Habit Milestones & Badges")
    st.caption("Celebrating positive behavioral consistency and discipline without clinical prescriptions.")

    if badges_list:
        unlocked_count = sum(1 for b in badges_list if b.unlocked)
        st.markdown(
            f"""
            <div style="margin-bottom: 1rem;">
                <span style="font-size: 0.95rem; font-weight: 700; color: {'#38bdf8' if is_dark else '#0284c7'};">
                    Unlocked: {unlocked_count} of {len(badges_list)} Milestone Badges
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        b_cols = st.columns(3)
        for idx, badge in enumerate(badges_list):
            with b_cols[idx % 3]:
                card_style = "badge-unlocked" if badge.unlocked else "badge-locked"
                status_txt = "✅ Unlocked" if badge.unlocked else "🔒 In Progress"
                status_color = "#10b981" if badge.unlocked else "#94a3b8"

                st.markdown(
                    f"""
                    <div class="badge-card {card_style}" style="margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-size: 1.5rem;">{badge.icon}</span>
                            <span style="font-size: 0.75rem; font-weight: 700; color: {status_color};">{status_txt}</span>
                        </div>
                        <div style="font-weight: 700; font-size: 0.95rem; color: {'#f8fafc' if is_dark else '#0f172a'}; margin-bottom: 4px;">
                            {badge.title}
                        </div>
                        <div style="font-size: 0.8rem; color: {'#cbd5e1' if is_dark else '#475569'}; margin-bottom: 10px; min-height: 38px;">
                            {badge.description}
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: {'#94a3b8' if is_dark else '#64748b'}; margin-bottom: 4px;">
                            <span>Progress</span>
                            <span>{badge.progress_label}</span>
                        </div>
                        <div style="background: {'#0f172a' if is_dark else '#e2e8f0'}; height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="background: {'#10b981' if badge.unlocked else '#0284c7'}; width: {badge.progress_pct}%; height: 100%;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("Record wellness data to evaluate habit milestone achievements.")


# =========================================================
# TAB 6: BREATHWORK & VAGAL TONE RESET
# =========================================================
with tab_breath:
    breathwork.render_breathwork_widget(dark_mode=is_dark)


# =========================================================
# TAB 7: Z-COGNITIVE HABIT ASSISTANT
# =========================================================
with tab_assistant:
    st.markdown("### 💬 Z-Cognitive Habit Assistant")
    st.caption("Deterministic, 100% offline natural language query processor. Zero external cloud API calls, zero telemetry.")

    # Suggested Prompts
    st.markdown("##### 💡 Suggested Questions:")
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    suggested_q = None
    if s_col1.button("🏆 Most Active Day", use_container_width=True):
        suggested_q = "What was my most active day?"
    if s_col2.button("🔥 Habit Streaks", use_container_width=True):
        suggested_q = "Show my active habit streaks"
    if s_col3.button("✈️ Weekend vs Weekday", use_container_width=True):
        suggested_q = "What is the difference between my weekday and weekend sleep?"
    if s_col4.button("⏰ Chronotype", use_container_width=True):
        suggested_q = "What is my circadian chronotype?"

    # Chat history display
    for sender, msg in st.session_state.chat_history:
        if sender == "user":
            st.markdown(f'<div class="chat-bubble-user">👤 <b>You:</b> {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-assistant">🤖 <b>Z-Assistant:</b><br>{msg}</div>', unsafe_allow_html=True)

    # Input form
    user_query = st.chat_input("Ask about your wellness data, streaks, sleep rhythm, or anomalies...")
    query_to_run = suggested_q or user_query

    if query_to_run:
        # Append user message
        st.session_state.chat_history.append(("user", query_to_run))
        # Answer deterministically
        resp = assistant.answer_wellness_query(query_to_run, df_filtered, goals)
        st.session_state.chat_history.append(("assistant", resp))
        st.rerun()


# =========================================================
# TAB 8: EXECUTIVE DOSSIER & DATA EXPORT
# =========================================================
with tab_report:
    st.markdown("### 📄 Executive Summary Dossier & Data Vault")
    st.caption("Generate self-contained printable HTML executive summaries and export filtered datasets.")

    r_col1, r_col2 = st.columns([1, 1])

    with r_col1:
        st.markdown("#### 📑 Executive HTML Report Generator")
        st.write("Compiles all metrics, composite scores, streaks, resilience metrics, and trend observations into a standalone, printable report.")

        if stats:
            html_content = report_generator.generate_executive_html_report(
                stats=stats,
                composite=comp,
                trend_report=trend_report,
                streaks=streaks,
                weekend_stats=weekend_stats,
                resilience_report=resilience_rep,
                badges=badges_list,
                persona_name=active_persona_title,
            )

            st.download_button(
                label="📥 Download Executive HTML Report",
                data=html_content,
                file_name=f"wellness_executive_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html",
                use_container_width=True,
            )
            st.caption("Tip: Open downloaded HTML in your browser and press **Ctrl+P** to save as PDF!")

    with r_col2:
        st.markdown("#### 💾 Export Filtered Dataset")
        st.write(f"Export currently filtered records ({len(df_filtered)} records) as clean CSV.")

        csv_buffer = io.StringIO()
        df_filtered.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_buffer.getvalue(),
            file_name=f"wellness_data_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown("#### 📋 Active Dataset Table")
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)


# =========================================================
# TAB 9: VIVA VOCE & ACADEMIC DEFENSE ROOM
# =========================================================
with tab_viva:
    viva_defense.render_academic_defense_tab()


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; color: {'#94a3b8' if is_dark else '#64748b'}; flex-wrap: wrap;">
        <div>Personal Wellness Dashboard • Academic Submission Project 2 • Session 2026–2027</div>
        <div>Offline Privacy Guarantee • 100% Deterministic Local Analytics • Zero Telemetry</div>
    </div>
    """,
    unsafe_allow_html=True,
)
