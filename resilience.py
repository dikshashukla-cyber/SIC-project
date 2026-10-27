"""IBM Z-inspired Autonomic Habit Resiliency & Uptime Engine.

Applies systems reliability concepts (availability, uptime, MTTR) to human wellness habits:
- Habit Availability / Uptime %: Ratio of days where essential baseline routines were maintained.
- Mean Time to Recovery (MTTR): Average consecutive days taken to bounce back after a missed day.
- Autonomic Health State: Behavioral resilience categorization inspired by self-healing systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple
import pandas as pd

try:
    from src.metrics import UserGoals
except (ImportError, ModuleNotFoundError):
    from metrics import UserGoals


@dataclass
class ResiliencyReport:
    """Represents autonomic habit resilience metrics."""
    uptime_pct: float
    total_active_days: int
    successful_days: int
    outage_days: int
    mean_time_to_recovery_days: float
    autonomic_health_status: str
    status_color: str
    resilience_summary: str


def calculate_autonomic_resiliency(
    df: pd.DataFrame,
    goals: Optional[UserGoals] = None,
) -> ResiliencyReport:
    """
    Calculates habit availability (uptime) and recovery metrics (MTTR).
    A day is considered an 'available / uptime' day if it satisfies at least 2 of 3 primary pillars:
    - Steps >= 80% of target
    - Sleep within [min_sleep - 0.5, max_sleep + 0.5]
    - Water >= 80% of target
    """
    if goals is None:
        goals = UserGoals()

    if df.empty or "date" not in df.columns:
        return ResiliencyReport(
            uptime_pct=0.0,
            total_active_days=0,
            successful_days=0,
            outage_days=0,
            mean_time_to_recovery_days=0.0,
            autonomic_health_status="Offline",
            status_color="#64748b",
            resilience_summary="No data available to calculate habit resilience.",
        )

    clean_df = df.sort_values("date").reset_index(drop=True)
    n = len(clean_df)

    step_floor = goals.steps_target * 0.80
    sleep_floor = max(4.5, goals.sleep_min - 0.5)
    sleep_ceil = goals.sleep_max + 0.5
    water_floor = max(4, int(goals.water_target * 0.80))

    # Evaluate each day
    is_available_list: List[bool] = []
    for _, row in clean_df.iterrows():
        pillars_met = 0
        if pd.notna(row["steps"]) and row["steps"] >= step_floor:
            pillars_met += 1
        if pd.notna(row["sleep_hours"]) and (sleep_floor <= row["sleep_hours"] <= sleep_ceil):
            pillars_met += 1
        if pd.notna(row["water_glasses"]) and row["water_glasses"] >= water_floor:
            pillars_met += 1

        is_available_list.append(pillars_met >= 2)

    successful_days = sum(is_available_list)
    outage_days = n - successful_days
    uptime_pct = round((successful_days / n) * 100.0, 1) if n > 0 else 0.0

    # Calculate MTTR (Mean Time to Recovery)
    # Count consecutive stretches of outage days that recover back to an available day
    recovery_times: List[int] = []
    current_outage_streak = 0
    for met in is_available_list:
        if not met:
            current_outage_streak += 1
        else:
            if current_outage_streak > 0:
                recovery_times.append(current_outage_streak)
                current_outage_streak = 0

    if recovery_times:
        mttr = round(sum(recovery_times) / len(recovery_times), 1)
    else:
        mttr = 1.0 if outage_days > 0 else 0.0

    # Autonomic Health State determination
    if uptime_pct >= 90.0:
        status = "Optimal Autonomic Resilience"
        color = "#16a34a"
        summary = (
            f"Exceptional habit uptime of {uptime_pct}%. Routine operates with high availability "
            f"and near-instant recovery ({mttr} days MTTR)."
        )
    elif uptime_pct >= 75.0:
        status = "Self-Healing Routine"
        color = "#0284c7"
        summary = (
            f"Strong habit uptime of {uptime_pct}%. System demonstrates effective self-recovery, "
            f"bouncing back from routine drops in ~{mttr} days."
        )
    elif uptime_pct >= 60.0:
        status = "Moderate Routine Drift"
        color = "#eab308"
        summary = (
            f"Moderate habit uptime of {uptime_pct}%. Periodic drops in activity or sleep take "
            f"~{mttr} days to re-stabilize."
        )
    else:
        status = "Degraded Habit Availability"
        color = "#ef4444"
        summary = (
            f"Habit availability stands at {uptime_pct}%. Significant routine variance observed "
            f"with recovery taking ~{mttr} days."
        )

    return ResiliencyReport(
        uptime_pct=uptime_pct,
        total_active_days=n,
        successful_days=successful_days,
        outage_days=outage_days,
        mean_time_to_recovery_days=mttr,
        autonomic_health_status=status,
        status_color=color,
        resilience_summary=summary,
    )
