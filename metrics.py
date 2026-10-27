"""Metric calculation, statistical aggregation, habit science, and composite score engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


@dataclass
class UserGoals:
    """Configurable user goals for habit evaluation."""
    sleep_min: float = 7.0
    sleep_max: float = 9.0
    steps_target: int = 8000
    water_target: int = 8
    activity_target: int = 30


@dataclass
class MetricSummary:
    """Summary statistics for a single metric."""
    name: str
    count: int
    mean: Optional[float]
    median: Optional[float]
    min_val: Optional[float]
    max_val: Optional[float]
    total: Optional[float] = None
    missing_count: int = 0


@dataclass
class DashboardStats:
    """Consolidated statistics for the filtered dataset."""
    total_days_in_range: int
    recorded_days_count: int
    completion_rate_pct: float
    sleep_summary: MetricSummary
    steps_summary: MetricSummary
    water_summary: MetricSummary
    mood_summary: Optional[MetricSummary] = None
    activity_summary: Optional[MetricSummary] = None


@dataclass
class CompositeScore:
    """Composite Behavioral Consistency Index (0-100)."""
    overall_score: int
    tier: str
    tier_color: str
    sleep_score: int
    steps_score: int
    water_score: int
    logging_score: int
    summary_text: str


@dataclass
class StreakInfo:
    """Consecutive day streak achievement."""
    metric_name: str
    current_streak: int
    longest_streak: int
    target_description: str


@dataclass
class WeekdayWeekendStats:
    """Comparative behavioral breakdown between workdays and weekends."""
    weekday_days: int
    weekend_days: int
    weekday_sleep_avg: float
    weekend_sleep_avg: float
    sleep_diff: float
    weekday_steps_avg: int
    weekend_steps_avg: int
    steps_diff: int
    weekday_water_avg: float
    weekend_water_avg: float
    water_diff: float
    weekday_activity_avg: Optional[float] = None
    weekend_activity_avg: Optional[float] = None


def filter_by_date_range(
    df: pd.DataFrame,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> pd.DataFrame:
    """Filters DataFrame by inclusive date boundaries [start_date, end_date]."""
    if df.empty or "date" not in df.columns:
        return df.copy()

    filtered = df.copy()
    filtered["date"] = pd.to_datetime(filtered["date"])

    if start_date is not None:
        start_ts = pd.to_datetime(start_date)
        filtered = filtered[filtered["date"] >= start_ts]

    if end_date is not None:
        end_ts = pd.to_datetime(end_date)
        filtered = filtered[filtered["date"] <= end_ts]

    return filtered.sort_values("date").reset_index(drop=True)


def calculate_metric_summary(
    series: pd.Series,
    name: str,
    include_total: bool = False,
) -> MetricSummary:
    """Calculates summary statistics for a numeric series."""
    valid_series = series.dropna()
    count = int(len(valid_series))
    missing_count = int(series.isna().sum())

    if count == 0:
        return MetricSummary(
            name=name,
            count=0,
            mean=None,
            median=None,
            min_val=None,
            max_val=None,
            total=None if include_total else None,
            missing_count=missing_count,
        )

    return MetricSummary(
        name=name,
        count=count,
        mean=round(float(valid_series.mean()), 2),
        median=round(float(valid_series.median()), 2),
        min_val=round(float(valid_series.min()), 2),
        max_val=round(float(valid_series.max()), 2),
        total=round(float(valid_series.sum()), 2) if include_total else None,
        missing_count=missing_count,
    )


def calculate_dashboard_stats(
    df: pd.DataFrame,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> Optional[DashboardStats]:
    """Computes overall summary statistics for the filtered dataset."""
    if df.empty:
        return None

    df_filtered = filter_by_date_range(df, start_date, end_date)
    if df_filtered.empty:
        return None

    dates = pd.to_datetime(df_filtered["date"]).dt.date
    min_date = start_date if start_date else dates.min()
    max_date = end_date if end_date else dates.max()

    total_days = max(1, (max_date - min_date).days + 1)
    recorded_days = int(dates.nunique())
    completion_rate = round(min(100.0, (recorded_days / total_days) * 100.0), 1)

    sleep_summary = calculate_metric_summary(df_filtered["sleep_hours"], "Sleep Hours", include_total=False)
    steps_summary = calculate_metric_summary(df_filtered["steps"], "Daily Steps", include_total=True)
    water_summary = calculate_metric_summary(df_filtered["water_glasses"], "Water Glasses", include_total=True)

    mood_summary = None
    if "mood_score" in df_filtered.columns and df_filtered["mood_score"].notna().any():
        mood_summary = calculate_metric_summary(df_filtered["mood_score"], "Mood Score (1-5)", include_total=False)

    activity_summary = None
    if "activity_minutes" in df_filtered.columns and df_filtered["activity_minutes"].notna().any():
        activity_summary = calculate_metric_summary(df_filtered["activity_minutes"], "Activity Minutes", include_total=True)

    return DashboardStats(
        total_days_in_range=total_days,
        recorded_days_count=recorded_days,
        completion_rate_pct=completion_rate,
        sleep_summary=sleep_summary,
        steps_summary=steps_summary,
        water_summary=water_summary,
        mood_summary=mood_summary,
        activity_summary=activity_summary,
    )


def calculate_composite_score(df: pd.DataFrame, goals: Optional[UserGoals] = None) -> CompositeScore:
    """
    Calculates the Composite Behavioral Wellness Consistency Index (0–100).
    A transparent, rule-based formula measuring habit adherence against personal targets.
    Formula weights:
    - Sleep Target Regularity: 30%
    - Steps Target Fulfillment: 30%
    - Water Intake Regularity: 20%
    - Logging Completeness: 20%
    """
    if goals is None:
        goals = UserGoals()

    if df.empty:
        return CompositeScore(0, "No Data", "#64748b", 0, 0, 0, 0, "No recorded data.")

    clean_df = df.copy()
    n = len(clean_df)

    # 1. Sleep score: % of days where sleep is within target window
    valid_sleep = clean_df["sleep_hours"].dropna()
    if len(valid_sleep) > 0:
        sleep_met = (valid_sleep >= goals.sleep_min) & (valid_sleep <= goals.sleep_max)
        sleep_score = int(round((sleep_met.sum() / len(valid_sleep)) * 100))
    else:
        sleep_score = 0

    # 2. Steps score: % of days meeting step target
    valid_steps = clean_df["steps"].dropna()
    if len(valid_steps) > 0:
        steps_met = valid_steps >= goals.steps_target
        steps_score = int(round((steps_met.sum() / len(valid_steps)) * 100))
    else:
        steps_score = 0

    # 3. Water score: % of days meeting hydration target
    valid_water = clean_df["water_glasses"].dropna()
    if len(valid_water) > 0:
        water_met = valid_water >= goals.water_target
        water_score = int(round((water_met.sum() / len(valid_water)) * 100))
    else:
        water_score = 0

    # 4. Logging score: ratio of recorded days to date span
    dates = pd.to_datetime(clean_df["date"]).dt.date
    date_span = max(1, (dates.max() - dates.min()).days + 1)
    logging_score = int(round(min(100.0, (dates.nunique() / date_span) * 100)))

    # Weighted sum
    overall = int(round(0.30 * sleep_score + 0.30 * steps_score + 0.20 * water_score + 0.20 * logging_score))
    overall = max(0, min(100, overall))

    if overall >= 85:
        tier = "Highly Consistent Routine"
        tier_color = "#16a34a"
        summary = "Exceptional habit consistency across sleep, activity, and hydration targets."
    elif overall >= 70:
        tier = "Consistent Routine"
        tier_color = "#0284c7"
        summary = "Steady routine with strong habit execution on most recorded days."
    elif overall >= 50:
        tier = "Moderate Consistency"
        tier_color = "#eab308"
        summary = "Moderate habit adherence with notable variance between active and rest days."
    else:
        tier = "Variable Routine"
        tier_color = "#ef4444"
        summary = "High day-to-day fluctuations across sleep duration and daily steps."

    return CompositeScore(
        overall_score=overall,
        tier=tier,
        tier_color=tier_color,
        sleep_score=sleep_score,
        steps_score=steps_score,
        water_score=water_score,
        logging_score=logging_score,
        summary_text=summary,
    )


def calculate_weekday_vs_weekend_stats(df: pd.DataFrame) -> Optional[WeekdayWeekendStats]:
    """Computes behavioral comparison between weekdays (Mon–Fri) and weekends (Sat–Sun)."""
    if df.empty or len(df) < 5:
        return None

    clean_df = df.copy()
    clean_df["date"] = pd.to_datetime(clean_df["date"])
    clean_df["day_of_week"] = clean_df["date"].dt.dayofweek  # 0=Mon, 4=Fri, 5=Sat, 6=Sun
    clean_df["is_weekend"] = clean_df["day_of_week"] >= 5

    weekdays_df = clean_df[~clean_df["is_weekend"]]
    weekends_df = clean_df[clean_df["is_weekend"]]

    if weekdays_df.empty or weekends_df.empty:
        return None

    wd_sleep = round(float(weekdays_df["sleep_hours"].dropna().mean()), 2)
    we_sleep = round(float(weekends_df["sleep_hours"].dropna().mean()), 2)

    wd_steps = int(round(float(weekdays_df["steps"].dropna().mean())))
    we_steps = int(round(float(weekends_df["steps"].dropna().mean())))

    wd_water = round(float(weekdays_df["water_glasses"].dropna().mean()), 2)
    we_water = round(float(weekends_df["water_glasses"].dropna().mean()), 2)

    wd_act = None
    we_act = None
    if "activity_minutes" in clean_df.columns and clean_df["activity_minutes"].notna().any():
        wd_act = round(float(weekdays_df["activity_minutes"].dropna().mean()), 1)
        we_act = round(float(weekends_df["activity_minutes"].dropna().mean()), 1)

    return WeekdayWeekendStats(
        weekday_days=len(weekdays_df),
        weekend_days=len(weekends_df),
        weekday_sleep_avg=wd_sleep,
        weekend_sleep_avg=we_sleep,
        sleep_diff=round(we_sleep - wd_sleep, 2),
        weekday_steps_avg=wd_steps,
        weekend_steps_avg=we_steps,
        steps_diff=we_steps - wd_steps,
        weekday_water_avg=wd_water,
        weekend_water_avg=we_water,
        water_diff=round(we_water - wd_water, 2),
        weekday_activity_avg=wd_act,
        weekend_activity_avg=we_act,
    )


def calculate_habit_streaks(df: pd.DataFrame, goals: Optional[UserGoals] = None) -> Dict[str, StreakInfo]:
    """Calculates active and longest streaks for personal targets."""
    if goals is None:
        goals = UserGoals()

    if df.empty or "date" not in df.columns:
        return {}

    sorted_df = df.sort_values("date").reset_index(drop=True)

    def _calc_streak(met_series: pd.Series) -> Tuple[int, int]:
        current = 0
        longest = 0
        streak = 0
        for val in met_series:
            if val:
                streak += 1
                if streak > longest:
                    longest = streak
            else:
                streak = 0
        # If the last day met the target, streak is current
        current = streak if (len(met_series) > 0 and met_series.iloc[-1]) else 0
        return current, longest

    # Steps streak
    steps_met = sorted_df["steps"] >= goals.steps_target
    cur_steps, max_steps = _calc_streak(steps_met)

    # Sleep streak
    sleep_met = (sorted_df["sleep_hours"] >= goals.sleep_min) & (sorted_df["sleep_hours"] <= goals.sleep_max)
    cur_sleep, max_sleep = _calc_streak(sleep_met)

    # Water streak
    water_met = sorted_df["water_glasses"] >= goals.water_target
    cur_water, max_water = _calc_streak(water_met)

    return {
        "steps": StreakInfo("Daily Steps", cur_steps, max_steps, f"≥ {goals.steps_target:,} steps"),
        "sleep": StreakInfo("Sleep Window", cur_sleep, max_sleep, f"{goals.sleep_min:.1f}–{goals.sleep_max:.1f} hrs"),
        "water": StreakInfo("Hydration", cur_water, max_water, f"≥ {goals.water_target} glasses"),
    }


def calculate_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates Pearson correlation matrix for numeric wellness metrics."""
    numeric_cols = ["sleep_hours", "steps", "water_glasses"]
    for opt in ["mood_score", "activity_minutes"]:
        if opt in df.columns and df[opt].notna().sum() >= 5:
            numeric_cols.append(opt)

    valid_cols = [c for c in numeric_cols if c in df.columns]
    if len(valid_cols) < 2 or len(df) < 5:
        return pd.DataFrame()

    corr = df[valid_cols].corr().round(2)
    # Rename columns for cleaner display
    label_map = {
        "sleep_hours": "Sleep (hrs)",
        "steps": "Steps",
        "water_glasses": "Water (gls)",
        "mood_score": "Mood (1-5)",
        "activity_minutes": "Activity (min)",
    }
    corr = corr.rename(index=label_map, columns=label_map)
    return corr


def add_rolling_averages(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """Calculates rolling averages for time-series visualization."""
    if df.empty or "date" not in df.columns:
        return df.copy()

    df_sorted = df.sort_values("date").copy()
    numeric_cols = ["sleep_hours", "steps", "water_glasses"]
    for opt in ["mood_score", "activity_minutes"]:
        if opt in df_sorted.columns:
            numeric_cols.append(opt)

    for col in numeric_cols:
        df_sorted[f"{col}_rolling_{window}d"] = (
            df_sorted[col].rolling(window=window, min_periods=1).mean().round(2)
        )

    return df_sorted
