"""Rule-based, transparent trend observations module for Wellness Dashboard.

Important:
This module adheres strictly to non-medical guidelines:
- Never generates medical diagnoses, prognostications, or prescriptive health advice.
- Uses transparent rule-based comparisons of recorded values across periods.
- Clearly states differences without implying causal links between factors.
- Suppresses trend observations when sample size is insufficient (< 7 recorded days).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np
import pandas as pd


MIN_DAYS_FOR_TRENDS = 7
MIN_DAYS_FOR_PERIOD_COMPARISON = 14


@dataclass
class TrendObservation:
    """Represents a single rule-based observation."""
    category: str
    summary: str
    detail: str
    tag: str = "Neutral"  # "Increase", "Decrease", "Steady", "Info"


@dataclass
class TrendReport:
    """Complete trend observations report."""
    has_sufficient_data: bool
    status_message: str
    observations: List[TrendObservation] = field(default_factory=list)
    earlier_period_dates: Optional[str] = None
    recent_period_dates: Optional[str] = None


def generate_trend_observations(df: pd.DataFrame) -> TrendReport:
    """
    Generates rule-based mathematical comparisons across recorded periods.
    Suppresses conclusions if sample size is insufficient.
    """
    if df.empty or "date" not in df.columns:
        return TrendReport(
            has_sufficient_data=False,
            status_message="No records found in the selected date range. Please select a broader date range or load data.",
        )

    clean_df = df.sort_values("date").copy()
    clean_df["date"] = pd.to_datetime(clean_df["date"])
    recorded_days = clean_df["date"].dt.date.nunique()

    if recorded_days < MIN_DAYS_FOR_TRENDS:
        return TrendReport(
            has_sufficient_data=False,
            status_message=(
                f"Insufficient data for trend observations. At least {MIN_DAYS_FOR_TRENDS} recorded days "
                f"are required to evaluate patterns (currently: {recorded_days} day{'s' if recorded_days != 1 else ''})."
            ),
        )

    observations: List[TrendObservation] = []

    # 1. Period Comparison (when >= 14 recorded days)
    earlier_dates_str = None
    recent_dates_str = None

    if recorded_days >= MIN_DAYS_FOR_PERIOD_COMPARISON:
        midpoint = len(clean_df) // 2
        earlier_df = clean_df.iloc[:midpoint]
        recent_df = clean_df.iloc[midpoint:]

        earlier_start = earlier_df["date"].dt.date.min()
        earlier_end = earlier_df["date"].dt.date.max()
        recent_start = recent_df["date"].dt.date.min()
        recent_end = recent_df["date"].dt.date.max()

        earlier_dates_str = f"{earlier_start} to {earlier_end}"
        recent_dates_str = f"{recent_start} to {recent_end}"

        # Compare Sleep
        earlier_sleep = earlier_df["sleep_hours"].dropna().mean()
        recent_sleep = recent_df["sleep_hours"].dropna().mean()
        if pd.notna(earlier_sleep) and pd.notna(recent_sleep):
            diff = recent_sleep - earlier_sleep
            if abs(diff) < 0.2:
                tag = "Steady"
                detail = f"Average sleep remained steady at ~{recent_sleep:.1f} hrs/day across both periods."
            elif diff > 0:
                tag = "Increase"
                detail = (
                    f"Average sleep was {recent_sleep:.1f} hrs/day in the recent period compared to "
                    f"{earlier_sleep:.1f} hrs/day in the earlier period (+{diff:.1f} hrs/day)."
                )
            else:
                tag = "Decrease"
                detail = (
                    f"Average sleep was {recent_sleep:.1f} hrs/day in the recent period compared to "
                    f"{earlier_sleep:.1f} hrs/day in the earlier period ({diff:.1f} hrs/day)."
                )

            observations.append(
                TrendObservation(
                    category="Sleep Duration",
                    summary=f"Recent average: {recent_sleep:.1f} hrs/day ({'+' if diff > 0 else ''}{diff:.1f} hrs difference)",
                    detail=detail,
                    tag=tag,
                )
            )

        # Compare Steps
        earlier_steps = earlier_df["steps"].dropna().mean()
        recent_steps = recent_df["steps"].dropna().mean()
        if pd.notna(earlier_steps) and pd.notna(recent_steps):
            diff_steps = recent_steps - earlier_steps
            if abs(diff_steps) < 300:
                tag = "Steady"
                detail = f"Daily steps averaged ~{int(round(recent_steps)):,} steps/day consistently across periods."
            elif diff_steps > 0:
                tag = "Increase"
                detail = (
                    f"Daily steps averaged {int(round(recent_steps)):,} steps/day in the recent period compared to "
                    f"{int(round(earlier_steps)):,} steps/day earlier (+{int(round(diff_steps)):,} steps/day)."
                )
            else:
                tag = "Decrease"
                detail = (
                    f"Daily steps averaged {int(round(recent_steps)):,} steps/day in the recent period compared to "
                    f"{int(round(earlier_steps)):,} steps/day earlier ({int(round(diff_steps)):,} steps/day)."
                )

            observations.append(
                TrendObservation(
                    category="Daily Step Count",
                    summary=f"Recent average: {int(round(recent_steps)):,} steps/day ({'+' if diff_steps > 0 else ''}{int(round(diff_steps)):,} difference)",
                    detail=detail,
                    tag=tag,
                )
            )

        # Compare Hydration
        earlier_water = earlier_df["water_glasses"].dropna().mean()
        recent_water = recent_df["water_glasses"].dropna().mean()
        if pd.notna(earlier_water) and pd.notna(recent_water):
            diff_water = recent_water - earlier_water
            if abs(diff_water) < 0.5:
                tag = "Steady"
                detail = f"Water intake remained consistent at ~{recent_water:.1f} glasses/day."
            elif diff_water > 0:
                tag = "Increase"
                detail = (
                    f"Water intake averaged {recent_water:.1f} glasses/day recently compared to "
                    f"{earlier_water:.1f} glasses/day earlier (+{diff_water:.1f} glasses/day)."
                )
            else:
                tag = "Decrease"
                detail = (
                    f"Water intake averaged {recent_water:.1f} glasses/day recently compared to "
                    f"{earlier_water:.1f} glasses/day earlier ({diff_water:.1f} glasses/day)."
                )

            observations.append(
                TrendObservation(
                    category="Hydration",
                    summary=f"Recent average: {recent_water:.1f} glasses/day ({'+' if diff_water > 0 else ''}{diff_water:.1f} difference)",
                    detail=detail,
                    tag=tag,
                )
            )

    # 2. Weekday vs. Weekend Behavioral Reflection
    clean_df["day_of_week"] = clean_df["date"].dt.dayofweek
    weekdays_df = clean_df[clean_df["day_of_week"] < 5]
    weekends_df = clean_df[clean_df["day_of_week"] >= 5]

    if len(weekdays_df) >= 3 and len(weekends_df) >= 2:
        wd_sleep = weekdays_df["sleep_hours"].dropna().mean()
        we_sleep = weekends_df["sleep_hours"].dropna().mean()
        if pd.notna(wd_sleep) and pd.notna(we_sleep):
            diff = we_sleep - wd_sleep
            if diff >= 0.8:
                observations.append(
                    TrendObservation(
                        category="Weekend Sleep Shift",
                        summary=f"Weekend sleep averaged +{diff:.1f} hrs higher than workdays",
                        detail=f"Recorded sleep averaged {we_sleep:.1f} hrs on weekends versus {wd_sleep:.1f} hrs on weekdays.",
                        tag="Info",
                    )
                )
            elif diff <= -0.8:
                observations.append(
                    TrendObservation(
                        category="Weekend Sleep Shift",
                        summary=f"Weekend sleep averaged {diff:.1f} hrs lower than workdays",
                        detail=f"Recorded sleep averaged {we_sleep:.1f} hrs on weekends versus {wd_sleep:.1f} hrs on weekdays.",
                        tag="Info",
                    )
                )

        wd_steps = weekdays_df["steps"].dropna().mean()
        we_steps = weekends_df["steps"].dropna().mean()
        if pd.notna(wd_steps) and pd.notna(we_steps):
            step_diff = we_steps - wd_steps
            if abs(step_diff) >= 1500:
                direction = "higher" if step_diff > 0 else "lower"
                observations.append(
                    TrendObservation(
                        category="Weekend Step Shift",
                        summary=f"Weekend steps averaged {abs(int(step_diff)):,} steps {direction} than workdays",
                        detail=f"Step counts averaged {int(we_steps):,} steps on weekends compared to {int(wd_steps):,} on weekdays.",
                        tag="Increase" if step_diff > 0 else "Decrease",
                    )
                )

    # 3. Regularity & Consistency Check
    sleep_std = clean_df["sleep_hours"].dropna().std()
    if pd.notna(sleep_std):
        if sleep_std <= 0.7:
            consistency_desc = "high consistency (recorded variation within ~45 minutes)"
        elif sleep_std <= 1.2:
            consistency_desc = "moderate day-to-day variation (~1 hour difference)"
        else:
            consistency_desc = "high day-to-day variation (>1.2 hours difference)"

        observations.append(
            TrendObservation(
                category="Sleep Regularity",
                summary=f"Standard deviation: {sleep_std:.2f} hrs",
                detail=f"Recorded sleep hours showed {consistency_desc} across the {recorded_days} recorded days.",
                tag="Steady" if sleep_std <= 1.0 else "Info",
            )
        )

    # 4. Step Benchmark Consistency
    steps_series = clean_df["steps"].dropna()
    if not steps_series.empty:
        target = 8000
        days_above = int((steps_series >= target).sum())
        pct_above = round((days_above / len(steps_series)) * 100, 1)
        observations.append(
            TrendObservation(
                category="Daily Step Consistency",
                summary=f"{days_above} of {len(steps_series)} days ({pct_above}%) met or exceeded 8,000 steps",
                detail=(
                    f"Across {len(steps_series)} recorded days, the daily step count was 8,000 or greater "
                    f"on {days_above} days ({pct_above}%)."
                ),
                tag="Increase" if pct_above >= 60 else "Info",
            )
        )

    return TrendReport(
        has_sufficient_data=True,
        status_message=f"Analyzed {recorded_days} recorded days across the selected range.",
        observations=observations,
        earlier_period_dates=earlier_dates_str,
        recent_period_dates=recent_dates_str,
    )
