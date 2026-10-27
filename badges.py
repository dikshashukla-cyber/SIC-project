"""Gamified Habit Milestones & Achievement Badges Engine for Wellness Dashboard."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import pandas as pd

from src.metrics import UserGoals, calculate_composite_score, calculate_habit_streaks, calculate_weekday_vs_weekend_stats


@dataclass
class AchievementBadge:
    """Represents an unlockable behavioral habit badge."""
    badge_id: str
    title: str
    icon: str
    description: str
    unlocked: bool
    progress_pct: int
    progress_label: str


def evaluate_achievement_badges(
    df: pd.DataFrame,
    goals: Optional[UserGoals] = None,
) -> List[AchievementBadge]:
    """
    Evaluates unlockable milestone badges based on recorded data and goals.
    Encourages positive routine consistency without clinical implications.
    """
    if goals is None:
        goals = UserGoals()

    if df.empty or "date" not in df.columns:
        return []

    clean_df = df.copy()
    n = len(clean_df)

    streaks = calculate_habit_streaks(clean_df, goals)
    comp = calculate_composite_score(clean_df, goals)
    weekend = calculate_weekday_vs_weekend_stats(clean_df)

    badges: List[AchievementBadge] = []

    # 1. Five Nines Resilience: >= 10 recorded days with completion rate >= 90%
    dates = pd.to_datetime(clean_df["date"]).dt.date
    date_span = max(1, (dates.max() - dates.min()).days + 1)
    logging_rate = (dates.nunique() / date_span) * 100.0
    unlocked_resilience = n >= 10 and logging_rate >= 90.0
    prog_resilience = min(100, int((n / 10.0) * 100))
    badges.append(
        AchievementBadge(
            badge_id="five_nines",
            title="Five Nines Resiliency",
            icon="🛡️",
            description="Log 10+ consecutive days with ≥90% logging availability.",
            unlocked=unlocked_resilience,
            progress_pct=prog_resilience,
            progress_label=f"{n}/10 days logged ({logging_rate:.0f}% uptime)",
        )
    )

    # 2. Hydro Master: Streak of 7+ days meeting hydration target
    water_streak = streaks.get("water")
    cur_w = water_streak.longest_streak if water_streak else 0
    unlocked_water = cur_w >= 7
    prog_water = min(100, int((cur_w / 7.0) * 100))
    badges.append(
        AchievementBadge(
            badge_id="hydro_master",
            title="Hydro Master",
            icon="🌊",
            description=f"Achieve a 7-day streak meeting your water target (≥{goals.water_target} glasses).",
            unlocked=unlocked_water,
            progress_pct=prog_water,
            progress_label=f"{cur_w}/7 days streak",
        )
    )

    # 3. Century Walker: Total steps >= 100,000
    total_steps = int(clean_df["steps"].dropna().sum())
    unlocked_steps = total_steps >= 100000
    prog_steps = min(100, int((total_steps / 100000.0) * 100))
    badges.append(
        AchievementBadge(
            badge_id="century_walker",
            title="Century Walker",
            icon="⚡",
            description="Accumulate 100,000+ total recorded steps across the period.",
            unlocked=unlocked_steps,
            progress_pct=prog_steps,
            progress_label=f"{total_steps:,} / 100,000 steps",
        )
    )

    # 4. Circadian Harmony: Sleep standard deviation < 0.75 hrs with >= 7 days
    sleep_std = float(clean_df["sleep_hours"].dropna().std()) if n >= 7 else 9.9
    unlocked_sleep = n >= 7 and sleep_std <= 0.75
    prog_sleep = 100 if unlocked_sleep else (int(max(0, (1.5 - sleep_std) / 0.75 * 100)) if sleep_std < 1.5 else 20)
    badges.append(
        AchievementBadge(
            badge_id="circadian_harmony",
            title="Circadian Harmony",
            icon="🌙",
            description="Maintain high sleep regularity (standard deviation ≤ 45 minutes).",
            unlocked=unlocked_sleep,
            progress_pct=prog_sleep,
            progress_label=f"Std Dev: {sleep_std:.2f} hrs" if n >= 7 else "Requires 7+ days",
        )
    )

    # 5. Weekend Peak Performer: Weekend step average > weekday step average
    if weekend and weekend.steps_diff > 0:
        unlocked_weekend = True
        prog_weekend = 100
        label_weekend = f"+{weekend.steps_diff:,} weekend steps"
    else:
        unlocked_weekend = False
        prog_weekend = 40
        label_weekend = "Weekend activity below workdays"

    badges.append(
        AchievementBadge(
            badge_id="weekend_peak",
            title="Weekend Peak Performer",
            icon="🏔️",
            description="Average higher physical step activity on weekends than workdays.",
            unlocked=unlocked_weekend,
            progress_pct=prog_weekend,
            progress_label=label_weekend,
        )
    )

    # 6. Consistency Master: Composite score >= 85
    unlocked_master = comp.overall_score >= 85
    badges.append(
        AchievementBadge(
            badge_id="consistency_master",
            title="Consistency Master",
            icon="🌟",
            description="Achieve an overall Behavioral Consistency Score of 85+ / 100.",
            unlocked=unlocked_master,
            progress_pct=comp.overall_score,
            progress_label=f"Score: {comp.overall_score}/100",
        )
    )

    return badges
