"""GitHub-Style Habit Contribution Heatmap Grid visualizer."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

try:
    from src.metrics import UserGoals
except (ImportError, ModuleNotFoundError):
    from metrics import UserGoals


def build_habit_calendar_heatmap(df: pd.DataFrame, goals: UserGoals) -> go.Figure:
    """
    Renders a GitHub-style activity contribution calendar grid.
    Each cell represents a day, colored by how many goals were satisfied (0-3).
    """
    if df.empty or "date" not in df.columns:
        fig = go.Figure()
        fig.update_layout(title="No data available for calendar heatmap")
        return fig

    clean_df = df.sort_values("date").copy()
    clean_df["date"] = pd.to_datetime(clean_df["date"])

    # Determine targets met per day
    targets_met = []
    hover_texts = []
    for _, row in clean_df.iterrows():
        met = 0
        if pd.notna(row["sleep_hours"]) and (goals.sleep_min <= row["sleep_hours"] <= goals.sleep_max):
            met += 1
        if pd.notna(row["steps"]) and row["steps"] >= goals.steps_target:
            met += 1
        if pd.notna(row["water_glasses"]) and row["water_glasses"] >= goals.water_target:
            met += 1

        targets_met.append(met)
        date_str = row["date"].strftime("%b %d, %Y (%a)")
        hover_texts.append(
            f"<b>{date_str}</b><br>"
            f"🎯 Targets Achieved: <b>{met} / 3</b><br>"
            f"💤 Sleep: {row['sleep_hours']:.1f} hrs<br>"
            f"🚶 Steps: {int(row['steps']):,}<br>"
            f"💧 Water: {int(row['water_glasses'])} glasses"
        )

    clean_df["targets_met"] = targets_met
    clean_df["hover_text"] = hover_texts

    # Day of week (0=Mon, 6=Sun) and Week index
    clean_df["day_name"] = clean_df["date"].dt.strftime("%a")
    clean_df["day_num"] = clean_df["date"].dt.dayofweek  # 0 to 6
    min_date = clean_df["date"].min()
    clean_df["week_num"] = ((clean_df["date"] - min_date).dt.days // 7)

    days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    y_labels = days_order[::-1]  # reverse so Mon is at the top

    # Create pivot for heatmap values and hover texts
    val_pivot = clean_df.pivot(index="day_num", columns="week_num", values="targets_met").reindex(range(6, -1, -1))
    text_pivot = clean_df.pivot(index="day_num", columns="week_num", values="hover_text").reindex(range(6, -1, -1))

    # GitHub-inspired green color scale
    # 0 = Light Gray, 1 = Pale Lime, 2 = Vibrant Green, 3 = Deep Emerald
    custom_colorscale = [
        [0.0, "#e2e8f0"],    # 0 targets
        [0.33, "#bbf7d0"],   # 1 target
        [0.66, "#4ade80"],   # 2 targets
        [1.0, "#15803d"],    # 3 targets (all met)
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=val_pivot.values,
            x=[f"Wk {c + 1}" for c in val_pivot.columns],
            y=y_labels,
            text=text_pivot.values,
            hoverinfo="text",
            colorscale=custom_colorscale,
            zmin=0,
            zmax=3,
            showscale=False,
            xgap=4,
            ygap=4,
        )
    )

    fig.update_layout(
        title={
            "text": "🟩 60-Day Habit Execution Grid (GitHub-Style Activity Matrix)",
            "font": {"size": 15, "color": "#0f172a"},
        },
        height=220,
        margin=dict(l=40, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, tickfont=dict(size=10, color="#64748b")),
        yaxis=dict(showgrid=False, tickfont=dict(size=11, color="#0f172a"), autorange="reversed"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
    )

    return fig
