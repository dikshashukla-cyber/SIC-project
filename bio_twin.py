"""
Bio-Digital Twin, 3D Phase Space Orbit & Neuro-Momentum Physics Engine.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np
import plotly.graph_objects as go
try:
    from src.metrics import UserGoals
except (ImportError, ModuleNotFoundError):
    from metrics import UserGoals


@dataclass
class BiologicalAgeReport:
    chronological_age: float
    biological_age: float
    age_delta: float  # negative means rejuvenated (younger)
    rejuvenation_index_pct: float
    status_label: str
    status_color: str
    breakdown: Dict[str, float]  # factor -> age impact in years


@dataclass
class NeuroMomentumReport:
    momentum_score: float  # 0 to 100
    velocity_rate: float
    inertia_mass: int  # based on streak
    friction_coefficient: float
    escape_velocity_achieved: bool
    status_title: str
    status_color: str
    explanation: str


def calculate_biological_age(df: pd.DataFrame, chronological_age: float = 21.0) -> BiologicalAgeReport:
    """
    Estimates biological vitality age delta based on longitudinal biometrics:
    - Sleep duration & stability
    - Cardiovascular volume (daily steps)
    - Cellular hydration (water intake)
    - Consistency / habit uptime
    """
    if df.empty:
        return BiologicalAgeReport(
            chronological_age=chronological_age,
            biological_age=chronological_age,
            age_delta=0.0,
            rejuvenation_index_pct=100.0,
            status_label="Insufficient Data",
            status_color="#64748b",
            breakdown={}
        )

    avg_sleep = df["sleep_hours"].mean()
    avg_steps = df["steps"].mean()
    avg_water = df["water_glasses"].mean()
    avg_mood = df["mood_score"].mean() if "mood_score" in df.columns and df["mood_score"].notna().any() else 3.5

    # 1. Sleep Impact (-1.5 to +1.8 years)
    if 7.0 <= avg_sleep <= 8.5:
        sleep_impact = -1.5
    elif 6.5 <= avg_sleep < 7.0 or 8.5 < avg_sleep <= 9.0:
        sleep_impact = -0.5
    elif 5.5 <= avg_sleep < 6.5:
        sleep_impact = +1.0
    else:
        sleep_impact = +1.8

    # 2. Steps Impact (-2.0 to +1.5 years)
    if avg_steps >= 10000:
        steps_impact = -2.0
    elif avg_steps >= 8000:
        steps_impact = -1.2
    elif avg_steps >= 6000:
        steps_impact = -0.4
    elif avg_steps >= 4000:
        steps_impact = +0.8
    else:
        steps_impact = +1.6

    # 3. Hydration Impact (-1.0 to +0.8 years)
    if avg_water >= 8:
        water_impact = -1.0
    elif avg_water >= 6:
        water_impact = -0.4
    else:
        water_impact = +0.8

    # 4. Mood / Neuro-Balance (-0.8 to +0.6 years)
    if avg_mood >= 4.0:
        mood_impact = -0.8
    elif avg_mood >= 3.0:
        mood_impact = -0.2
    else:
        mood_impact = +0.6

    total_delta = round(sleep_impact + steps_impact + water_impact + mood_impact, 1)
    bio_age = round(chronological_age + total_delta, 1)

    # Rejuvenation score index (100 = matched, >100 = younger/healthier)
    rejuv_index = round((chronological_age / max(bio_age, 10.0)) * 100.0, 1)

    if total_delta <= -2.5:
        status = "✨ Peak Cellular Rejuvenation (High Longevity Reserve)"
        color = "#10b981"  # Emerald
    elif total_delta < 0.0:
        status = "🌿 Positive Vitality Balance (Age Reversal Active)"
        color = "#06b6d4"  # Cyan
    elif total_delta == 0.0:
        status = "⚖️ Biological Equilibrium (Synchronized)"
        color = "#f59e0b"  # Amber
    else:
        status = "⚠️ Oxidative Burnout Warning (Biological Acceleration)"
        color = "#ef4444"  # Red

    breakdown = {
        "Sleep Quality Window": sleep_impact,
        "Cardiovascular Step Endurance": steps_impact,
        "Cellular Hydration Reserve": water_impact,
        "Neuro-Emotional Balance": mood_impact,
    }

    return BiologicalAgeReport(
        chronological_age=chronological_age,
        biological_age=bio_age,
        age_delta=total_delta,
        rejuvenation_index_pct=rejuv_index,
        status_label=status,
        status_color=color,
        breakdown=breakdown,
    )


def calculate_neuro_momentum(df: pd.DataFrame, goals: UserGoals) -> NeuroMomentumReport:
    """
    Computes habit momentum using Newtonian kinematic physics metaphor:
    - Momentum p = mass (streak length) * velocity (recent compliance rate)
    - Friction mu = rate of missed targets in last 14 days
    - Escape Velocity: When routine becomes autonomous without cognitive willpower drain
    """
    if len(df) < 3:
        return NeuroMomentumReport(
            momentum_score=50.0,
            velocity_rate=1.0,
            inertia_mass=1,
            friction_coefficient=0.2,
            escape_velocity_achieved=False,
            status_title="Calibrating Momentum...",
            status_color="#64748b",
            explanation="Record more consecutive days to compute neuro-momentum physics.",
        )

    recent_14 = df.tail(14)
    compliant_days = 0
    for _, row in recent_14.iterrows():
        hit_sleep = goals.sleep_min <= row["sleep_hours"] <= goals.sleep_max
        hit_steps = row["steps"] >= goals.steps_target
        hit_water = row["water_glasses"] >= goals.water_target
        if sum([hit_sleep, hit_steps, hit_water]) >= 2:
            compliant_days += 1

    velocity = round(compliant_days / len(recent_14), 2)  # 0.0 to 1.0

    # Calculate active consecutive streak
    streak = 0
    for _, row in df.iloc[::-1].iterrows():
        hit_sleep = goals.sleep_min <= row["sleep_hours"] <= goals.sleep_max
        hit_steps = row["steps"] >= goals.steps_target
        hit_water = row["water_glasses"] >= goals.water_target
        if sum([hit_sleep, hit_steps, hit_water]) >= 2:
            streak += 1
        else:
            break

    mass = max(1, streak)
    friction = round((len(recent_14) - compliant_days) / len(recent_14), 2)

    # Raw momentum: (mass^0.6) * (velocity^1.2) normalized to 0-100
    raw_momentum = (pow(mass, 0.55) * pow(velocity, 1.1) * 35.0) - (friction * 15.0)
    momentum_score = round(max(5.0, min(99.0, raw_momentum)), 1)

    escape_velocity = momentum_score >= 75.0 and streak >= 7

    if escape_velocity:
        title = "🚀 Autonomous Escape Velocity Achieved"
        color = "#10b981"
        expl = "Your habit loop has shifted from conscious willpower to subconscious automaticity. Cognitive friction is near zero."
    elif momentum_score >= 55.0:
        title = "⚡ High Kinetic Momentum"
        color = "#06b6d4"
        expl = "Habits are building solid behavioral inertia. Maintain compliance to cross the neuroplastic escape threshold."
    elif momentum_score >= 35.0:
        title = "🔄 Steady Acceleration Phase"
        color = "#f59e0b"
        expl = "Consistent effort detected, but routine remains susceptible to schedule disruption friction."
    else:
        title = "⚠️ High Neural Friction Zone"
        color = "#ef4444"
        expl = "Frequent target breaks increase willpower expenditure. Implement micro-habit stacking to reduce start-up friction."

    return NeuroMomentumReport(
        momentum_score=momentum_score,
        velocity_rate=velocity,
        inertia_mass=mass,
        friction_coefficient=friction,
        escape_velocity_achieved=escape_velocity,
        status_title=title,
        status_color=color,
        explanation=expl,
    )


def build_3d_habit_orbit_chart(df: pd.DataFrame, goals: UserGoals, dark_mode: bool = False) -> go.Figure:
    """
    Renders an interactive 3D Phase Space Orbit of habit trajectories:
    X: Sleep Hours
    Y: Daily Steps
    Z: Water Glasses
    Color: Mood Score or Behavioral Day Score
    Connecting lines visualize sequential day-by-day evolution through 3D state space.
    """
    df_sorted = df.sort_values("date").copy()
    
    # Calculate daily score for color scale
    color_vals = []
    hover_texts = []
    for _, row in df_sorted.iterrows():
        date_str = str(row["date"])[:10]
        s = row["sleep_hours"]
        st = row["steps"]
        w = row["water_glasses"]
        m = row.get("mood_score", 3.0)
        
        # normalized quality score
        score = (min(s / 8.0, 1.0) * 33) + (min(st / 10000.0, 1.0) * 33) + (min(w / 8.0, 1.0) * 34)
        color_vals.append(score)
        
        hover_texts.append(
            f"<b>📅 {date_str}</b><br>"
            f"• Sleep: {s:.1f} hrs<br>"
            f"• Steps: {int(st):,}<br>"
            f"• Hydration: {int(w)} glasses<br>"
            f"• Mood: {m}<br>"
            f"• State Score: {score:.1f}/100"
        )

    fig = go.Figure()

    # 1. Trajectory Spline Line through 3D Phase Space
    fig.add_trace(
        go.Scatter3d(
            x=df_sorted["sleep_hours"],
            y=df_sorted["steps"],
            z=df_sorted["water_glasses"],
            mode="lines",
            line=dict(
                color="#00f2fe" if dark_mode else "#0284c7",
                width=3.5,
            ),
            name="Habit Phase Orbit",
            hoverinfo="none",
        )
    )

    # 2. Daily Coordinate Markers
    fig.add_trace(
        go.Scatter3d(
            x=df_sorted["sleep_hours"],
            y=df_sorted["steps"],
            z=df_sorted["water_glasses"],
            mode="markers",
            marker=dict(
                size=6,
                color=color_vals,
                colorscale="Viridis" if not dark_mode else "Turbo",
                colorbar=dict(
                    title=dict(text="Vitality Index", font=dict(color="#f4f4f4" if dark_mode else "#0f172a", size=10)),
                    tickfont=dict(color="#f4f4f4" if dark_mode else "#0f172a", size=9),
                    len=0.75,
                    thickness=12,
                    x=1.02,
                ),
                opacity=0.9,
            ),
            text=hover_texts,
            hoverinfo="text",
            name="Daily State Points",
        )
    )

    # 3. Attractor Basin / Optimal Wellness Target Box
    # Box corners for optimal zone: Sleep [7, 9], Steps [8000, 12000], Water [8, 12]
    basin_x = [goals.sleep_min, goals.sleep_max, goals.sleep_max, goals.sleep_min, goals.sleep_min]
    basin_y = [goals.steps_target, goals.steps_target, 12000, 12000, goals.steps_target]
    basin_z = [goals.water_target, goals.water_target, goals.water_target, goals.water_target, goals.water_target]

    fig.add_trace(
        go.Scatter3d(
            x=basin_x,
            y=basin_y,
            z=basin_z,
            mode="lines",
            line=dict(color="#10b981", width=3, dash="dash"),
            name="🎯 Attractor Basin (Target Zone)",
            hoverinfo="name",
        )
    )

    # Latest Day Beacon Marker
    last_row = df_sorted.iloc[-1]
    fig.add_trace(
        go.Scatter3d(
            x=[last_row["sleep_hours"]],
            y=[last_row["steps"]],
            z=[last_row["water_glasses"]],
            mode="markers+text",
            marker=dict(size=11, color="#ef4444", symbol="diamond"),
            text=["📍 Current Day Position"],
            textposition="top center",
            textfont=dict(color="#ef4444", size=11),
            name="Current State",
            hoverinfo="none",
        )
    )

    bg_color = "#0a0e17" if dark_mode else "#f8fafc"
    grid_color = "#262626" if dark_mode else "#e2e8f0"
    text_color = "#f4f4f4" if dark_mode else "#334155"

    fig.update_layout(
        title=dict(
            text="🌌 3D Habit Phase Space Trajectory & Attractor Orbit",
            font=dict(size=15, color=text_color),
        ),
        scene=dict(
            xaxis=dict(
                title=dict(text="Sleep Duration (hrs)", font=dict(color=text_color, size=11)),
                backgroundcolor=bg_color,
                gridcolor=grid_color,
                tickfont=dict(color=text_color, size=9),
            ),
            yaxis=dict(
                title=dict(text="Daily Steps", font=dict(color=text_color, size=11)),
                backgroundcolor=bg_color,
                gridcolor=grid_color,
                tickfont=dict(color=text_color, size=9),
            ),
            zaxis=dict(
                title=dict(text="Hydration (glasses)", font=dict(color=text_color, size=11)),
                backgroundcolor=bg_color,
                gridcolor=grid_color,
                tickfont=dict(color=text_color, size=9),
            ),
            bgcolor=bg_color,
            camera=dict(
                eye=dict(x=1.7, y=1.7, z=1.2),
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=35, b=10),
        height=450,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.05,
            xanchor="center",
            x=0.5,
            font=dict(color=text_color, size=10),
        ),
    )

    return fig
