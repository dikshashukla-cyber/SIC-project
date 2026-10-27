"""24-Hour Circadian Polar Clock Dial visualizer."""

from __future__ import annotations

import plotly.graph_objects as go
import pandas as pd


def build_circadian_polar_clock(avg_sleep_hours: float = 7.5, is_weekend_shifted: bool = False) -> go.Figure:
    """
    Renders an interactive 24-hour polar clock dial illustrating sleep-wake cycles,
    circadian rest phases, and optimal activity windows.
    Angles: 0 degrees = Midnight (00:00), 90 deg = 06:00, 180 deg = 12:00 (Noon), 270 deg = 18:00.
    """
    fig = go.Figure()

    # Bedtime: ~23:00 (345 deg) on weekdays, ~00:30 (7.5 deg) if weekend shifted
    bedtime_hour = 0.5 if is_weekend_shifted else 23.0
    sleep_duration = avg_sleep_hours
    wake_hour = (bedtime_hour + sleep_duration) % 24

    # 1. 24-Hour Clock Dial Sectors
    # Day phase: 07:00 to 22:00
    fig.add_trace(
        go.Barpolar(
            r=[100],
            theta=[180],  # Centered around noon
            width=[225],  # 15 hours width
            name="Daytime Active Phase",
            marker_color="rgba(56, 189, 248, 0.18)",
            marker_line_color="rgba(56, 189, 248, 0.4)",
            marker_line_width=1,
            hoverinfo="name",
        )
    )

    # Peak Physical Activity Window (16:30 to 19:30)
    fig.add_trace(
        go.Barpolar(
            r=[90],
            theta=[270],  # 18:00
            width=[45],   # 3 hours width
            name="Peak Physical Activity Window",
            marker_color="rgba(16, 185, 129, 0.45)",
            marker_line_color="#059669",
            marker_line_width=1.5,
            hoverinfo="name",
        )
    )

    # Sleep Window Wedge
    sleep_center_hour = (bedtime_hour + sleep_duration / 2) % 24
    sleep_center_deg = (sleep_center_hour / 24.0) * 360.0
    sleep_width_deg = (sleep_duration / 24.0) * 360.0

    fig.add_trace(
        go.Barpolar(
            r=[100],
            theta=[sleep_center_deg],
            width=[sleep_width_deg],
            name=f"Sleep Rest Window (~{sleep_duration:.1f} hrs)",
            marker_color="rgba(37, 99, 235, 0.55)",
            marker_line_color="#1d4ed8",
            marker_line_width=2,
            hoverinfo="name",
        )
    )

    # 24 Hour Tick Labels
    hour_ticks = list(range(0, 24, 3))
    hour_labels = [f"{h:02d}:00" for h in hour_ticks]

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 105]),
            angularaxis=dict(
                direction="clockwise",
                period=360,
                tickmode="array",
                tickvals=[(h / 24.0) * 360 for h in hour_ticks],
                ticktext=hour_labels,
                tickfont=dict(size=10, color="#475569", family="Segoe UI"),
                rotation=90,  # 00:00 at the top
            ),
        ),
        title={
            "text": f"⏰ 24-Hour Circadian Polar Clock ({'Weekend Shifted' if is_weekend_shifted else 'Workweek Anchor'})",
            "font": {"size": 14, "color": "#0f172a"},
        },
        height=320,
        margin=dict(l=30, r=30, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        paper_bgcolor="#ffffff",
    )

    return fig
