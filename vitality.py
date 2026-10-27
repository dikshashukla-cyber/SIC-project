"""Habit Vitality & Next-Day Readiness Forecast Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

try:
    from src.metrics import UserGoals
except (ImportError, ModuleNotFoundError):
    from metrics import UserGoals


@dataclass
class VitalityReport:
    """Represents habit vitality and next-day routine readiness."""
    vitality_score: int
    momentum_zone: str
    zone_color: str
    recent_sleep_avg: float
    recent_steps_avg: int
    recent_water_avg: float
    key_drivers: List[str] = field(default_factory=list)
    readiness_outlook: str = ""


def calculate_vitality_forecast(
    df: pd.DataFrame,
    goals: Optional[UserGoals] = None,
    lookback_days: int = 3,
) -> Optional[VitalityReport]:
    """
    Evaluates recent behavioral momentum across the last N recorded days
    to project next-day habit readiness (non-medical behavioral momentum).
    """
    if goals is None:
        goals = UserGoals()

    if df.empty or len(df) < lookback_days or "date" not in df.columns:
        return None

    recent_df = df.sort_values("date").iloc[-lookback_days:].copy()

    recent_sleep = float(recent_df["sleep_hours"].dropna().mean())
    recent_steps = int(round(float(recent_df["steps"].dropna().mean())))
    recent_water = float(recent_df["water_glasses"].dropna().mean())

    # Component scores (0-100)
    # 1. Sleep driver: optimal if within target window
    if goals.sleep_min <= recent_sleep <= goals.sleep_max:
        sleep_driver = 100
        sleep_driver_msg = f"Consistent sleep averaging {recent_sleep:.1f} hrs/night"
    elif recent_sleep > goals.sleep_max:
        sleep_driver = max(60, int(100 - (recent_sleep - goals.sleep_max) * 15))
        sleep_driver_msg = f"Elevated sleep duration ({recent_sleep:.1f} hrs)"
    else:
        sleep_driver = max(30, int(100 - (goals.sleep_min - recent_sleep) * 30))
        sleep_driver_msg = f"Slight sleep deficit ({recent_sleep:.1f} hrs vs target {goals.sleep_min} hrs)"

    # 2. Steps driver
    steps_ratio = min(1.3, recent_steps / max(1, goals.steps_target))
    if steps_ratio >= 1.0:
        step_driver = 100
        step_driver_msg = f"Daily steps meeting target ({recent_steps:,} avg)"
    else:
        step_driver = int(steps_ratio * 100)
        step_driver_msg = f"Daily steps below target ({recent_steps:,} avg)"

    # 3. Hydration driver
    water_ratio = min(1.2, recent_water / max(1, goals.water_target))
    water_driver = int(min(100, water_ratio * 100))
    water_driver_msg = f"Hydration averaging {recent_water:.1f} glasses/day"

    # Composite Vitality score
    vitality = int(round(0.40 * sleep_driver + 0.35 * step_driver + 0.25 * water_driver))
    vitality = max(10, min(100, vitality))

    drivers = [sleep_driver_msg, step_driver_msg, water_driver_msg]

    if vitality >= 85:
        zone = "Peak Momentum Zone"
        color = "#16a34a"
        outlook = (
            "High behavioral momentum across sleep and activity. "
            "You are well-positioned for strong habit execution tomorrow."
        )
    elif vitality >= 65:
        zone = "Steady Vitality Zone"
        color = "#0284c7"
        outlook = (
            "Consistent baseline momentum. Routine execution is balanced "
            "with steady day-to-day habit sustainability."
        )
    elif vitality >= 45:
        zone = "Rest & Recharge Zone"
        color = "#eab308"
        outlook = (
            "Mild habit deceleration observed. Prioritizing consistent bedtime "
            "and hydration will help restore routine momentum."
        )
    else:
        zone = "Recovery Reset Recommended"
        color = "#ef4444"
        outlook = (
            "Routine fluctuations detected. A gentle return to core targets "
            "(hydration and consistent sleep) is recommended for tomorrow."
        )

    return VitalityReport(
        vitality_score=vitality,
        momentum_zone=zone,
        zone_color=color,
        recent_sleep_avg=round(recent_sleep, 1),
        recent_steps_avg=recent_steps,
        recent_water_avg=round(recent_water, 1),
        key_drivers=drivers,
        readiness_outlook=outlook,
    )
