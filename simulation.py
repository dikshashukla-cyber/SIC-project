"""What-If? Routine Scenario Simulator for predictive behavioral modeling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import pandas as pd

from src.metrics import UserGoals, calculate_composite_score, CompositeScore
from src.resilience import calculate_autonomic_resiliency, ResiliencyReport


@dataclass
class SimulationResult:
    """Represents comparative outcome of a simulated routine adjustment."""
    baseline_composite: int
    projected_composite: int
    composite_gain: int
    baseline_uptime: float
    projected_uptime: float
    uptime_gain: float
    projected_tier: str
    impact_summary: str


def simulate_routine_tweak(
    df: pd.DataFrame,
    delta_sleep: float = 0.0,
    delta_steps: int = 0,
    delta_water: int = 0,
    goals: Optional[UserGoals] = None,
) -> Optional[SimulationResult]:
    """
    Simulates hypothetical adjustments to daily sleep, steps, and water intake.
    Models the prospective impact on the Composite Consistency Index and Habit Uptime.
    """
    if df.empty or "date" not in df.columns:
        return None

    if goals is None:
        goals = UserGoals()

    # Calculate baseline
    base_comp = calculate_composite_score(df, goals)
    base_res = calculate_autonomic_resiliency(df, goals)

    # Create adjusted simulation dataset
    sim_df = df.copy()
    if delta_sleep != 0.0 and "sleep_hours" in sim_df.columns:
        sim_df["sleep_hours"] = (sim_df["sleep_hours"] + delta_sleep).clip(lower=0.0, upper=24.0)

    if delta_steps != 0 and "steps" in sim_df.columns:
        sim_df["steps"] = (sim_df["steps"] + delta_steps).clip(lower=0, upper=100000)

    if delta_water != 0 and "water_glasses" in sim_df.columns:
        sim_df["water_glasses"] = (sim_df["water_glasses"] + delta_water).clip(lower=0, upper=50)

    # Calculate projected outcomes
    proj_comp = calculate_composite_score(sim_df, goals)
    proj_res = calculate_autonomic_resiliency(sim_df, goals)

    comp_diff = proj_comp.overall_score - base_comp.overall_score
    uptime_diff = round(proj_res.uptime_pct - base_res.uptime_pct, 1)

    if comp_diff > 0:
        summary = (
            f"📈 Projected Improvement: Adjusting your daily routine by {f'{delta_sleep:+.1f} hrs sleep, ' if delta_sleep != 0 else ''}"
            f"{f'{delta_steps:+,} steps, ' if delta_steps != 0 else ''}"
            f"{f'{delta_water:+} glasses water' if delta_water != 0 else ''} "
            f"yields a prospective +{comp_diff} point boost in consistency and +{uptime_diff}% higher habit availability."
        )
    elif comp_diff < 0:
        summary = (
            f"📉 Projected Decline: These adjustments would reduce your consistency index by {abs(comp_diff)} points "
            f"and lower habit availability by {abs(uptime_diff)}%."
        )
    else:
        summary = "Steady projection: Your current baseline already supports this routine target."

    return SimulationResult(
        baseline_composite=base_comp.overall_score,
        projected_composite=proj_comp.overall_score,
        composite_gain=comp_diff,
        baseline_uptime=base_res.uptime_pct,
        projected_uptime=proj_res.uptime_pct,
        uptime_gain=uptime_diff,
        projected_tier=proj_comp.tier,
        impact_summary=summary,
    )
