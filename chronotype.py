"""Circadian Chronotype and Behavioral Social Jetlag Analyzer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import numpy as np
import pandas as pd


@dataclass
class ChronotypeReport:
    """Circadian and behavioral sleep regularity metrics."""
    chronotype: str
    chronotype_icon: str
    social_jetlag_minutes: int
    social_jetlag_hours: float
    weekday_sleep_avg: float
    weekend_sleep_avg: float
    circadian_alignment_score: int
    alignment_tier: str
    description: str


def calculate_circadian_chronotype(df: pd.DataFrame) -> Optional[ChronotypeReport]:
    """
    Computes behavioral sleep shifts between workdays and free days (Social Jetlag).
    Social Jetlag measures the difference in sleep duration and schedule between
    workdays (Mon-Fri) and weekends (Sat-Sun).
    """
    if df.empty or len(df) < 7 or "date" not in df.columns or "sleep_hours" not in df.columns:
        return None

    clean_df = df.copy()
    clean_df["date"] = pd.to_datetime(clean_df["date"])
    clean_df["day_of_week"] = clean_df["date"].dt.dayofweek

    weekdays_df = clean_df[clean_df["day_of_week"] < 5]
    weekends_df = clean_df[clean_df["day_of_week"] >= 5]

    if len(weekdays_df) < 3 or len(weekends_df) < 2:
        return None

    wd_sleep = float(weekdays_df["sleep_hours"].dropna().mean())
    we_sleep = float(weekends_df["sleep_hours"].dropna().mean())

    # Social Jetlag is modeled by the weekend sleep schedule shift:
    # A difference of 1 hour in sleep duration reflects ~45-60 mins shift in midpoint
    sleep_diff_hours = abs(we_sleep - wd_sleep)
    jetlag_minutes = int(round(sleep_diff_hours * 60))

    # Circadian alignment score (100 is perfect consistency, dropping by jetlag)
    alignment_score = max(20, min(100, int(round(100 - (jetlag_minutes * 0.5)))))

    if alignment_score >= 85:
        tier = "High Circadian Harmony"
    elif alignment_score >= 70:
        tier = "Moderate Circadian Shift"
    else:
        tier = "Elevated Social Jetlag"

    # Chronotype classification based on weekend sleep duration and overall pattern
    if we_sleep >= 8.5 and (we_sleep - wd_sleep) >= 1.2:
        chronotype = "Night Owl (Catch-Up Pattern)"
        icon = "🦉"
        desc = (
            f"Shows an elevated weekend sleep catch-up shift ({jetlag_minutes} mins). "
            f"Workday sleep is shorter ({wd_sleep:.1f} hrs) compared to weekends ({we_sleep:.1f} hrs)."
        )
    elif wd_sleep >= 7.2 and abs(we_sleep - wd_sleep) <= 0.6:
        chronotype = "Early Lark (Steady Anchor)"
        icon = "🌅"
        desc = (
            f"Shows low social jetlag ({jetlag_minutes} mins) with consistent sleep duration "
            f"anchored across both workdays ({wd_sleep:.1f} hrs) and weekends ({we_sleep:.1f} hrs)."
        )
    else:
        chronotype = "Balanced Intermediate"
        icon = "⚖️"
        desc = (
            f"Demonstrates a balanced intermediate pattern with moderate schedule variation "
            f"of ~{jetlag_minutes} minutes between workdays and weekends."
        )

    return ChronotypeReport(
        chronotype=chronotype,
        chronotype_icon=icon,
        social_jetlag_minutes=jetlag_minutes,
        social_jetlag_hours=round(jetlag_minutes / 60.0, 1),
        weekday_sleep_avg=round(wd_sleep, 1),
        weekend_sleep_avg=round(we_sleep, 1),
        circadian_alignment_score=alignment_score,
        alignment_tier=tier,
        description=desc,
    )
