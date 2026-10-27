"""Z-Cognitive Habit Assistant — Local, deterministic natural language query engine.

Processes user queries offline using rule-based parsing and DataFrame statistics.
Zero external API calls, zero telemetry, 100% private and transparent.
"""

from __future__ import annotations

from typing import Dict, Any, Optional
import pandas as pd

try:
    from src.metrics import UserGoals, calculate_dashboard_stats, calculate_habit_streaks, calculate_weekday_vs_weekend_stats, calculate_composite_score
    from src.resilience import calculate_autonomic_resiliency
    from src.chronotype import calculate_circadian_chronotype
    from src.validation import detect_anomalies
except (ImportError, ModuleNotFoundError):
    from metrics import UserGoals, calculate_dashboard_stats, calculate_habit_streaks, calculate_weekday_vs_weekend_stats, calculate_composite_score
    from resilience import calculate_autonomic_resiliency
    from chronotype import calculate_circadian_chronotype
    from validation import detect_anomalies


def answer_wellness_query(
    query: str,
    df: pd.DataFrame,
    goals: Optional[UserGoals] = None,
) -> str:
    """
    Evaluates natural language questions about the user's active records
    and computes deterministic, transparent answers directly from pandas data.
    """
    if df.empty or "date" not in df.columns:
        return "No records are currently loaded in the selected date range to answer your question."

    if goals is None:
        goals = UserGoals()

    q = query.lower().strip()
    clean_df = df.copy()
    n = len(clean_df)

    # 1. Best / Most Active Day / Steps Record
    if any(k in q for k in ["best day", "most active", "highest step", "max step", "record step"]):
        max_row = clean_df.loc[clean_df["steps"].idxmax()]
        date_str = max_row["date"].strftime("%B %d, %Y") if hasattr(max_row["date"], "strftime") else str(max_row["date"])
        steps_val = int(max_row["steps"])
        sleep_val = max_row["sleep_hours"]
        water_val = max_row["water_glasses"]
        return (
            f"🏆 **Your Most Active Day**:  \n"
            f"On **{date_str}**, you recorded **{steps_val:,} steps**, accompanied by "
            f"**{sleep_val:.1f} hours of sleep** and **{water_val} glasses of water**."
        )

    # 2. Streaks query
    if any(k in q for k in ["streak", "consecutive", "longest streak"]):
        streaks = calculate_habit_streaks(clean_df, goals)
        st_steps = streaks.get("steps")
        st_sleep = streaks.get("sleep")
        st_water = streaks.get("water")
        return (
            f"🔥 **Your Habit Streaks Breakdown**:  \n"
            f"- **Daily Steps (≥{goals.steps_target:,} steps)**: Current active streak is **{st_steps.current_streak} days** (Longest: **{st_steps.longest_streak} days**).  \n"
            f"- **Sleep Window ({goals.sleep_min}–{goals.sleep_max} hrs)**: Current active streak is **{st_sleep.current_streak} days** (Longest: **{st_sleep.longest_streak} days**).  \n"
            f"- **Hydration (≥{goals.water_target} gls)**: Current active streak is **{st_water.current_streak} days** (Longest: **{st_water.longest_streak} days**)."
        )

    # 3. Weekend vs Weekday comparison
    if any(k in q for k in ["weekend", "weekday", "workday", "saturday", "sunday"]):
        we = calculate_weekday_vs_weekend_stats(clean_df)
        if not we:
            return "There are not enough records spanning both weekdays and weekends in the current range to compare."
        sleep_sign = "+" if we.sleep_diff > 0 else ""
        step_sign = "+" if we.steps_diff > 0 else ""
        return (
            f"📅 **Weekday vs. Weekend Comparison**:  \n"
            f"- **Sleep Duration**: Weekdays averaged **{we.weekday_sleep_avg:.1f} hrs** vs. Weekends **{we.weekend_sleep_avg:.1f} hrs** ({sleep_sign}{we.sleep_diff:.1f} hrs).  \n"
            f"- **Step Count**: Weekdays averaged **{we.weekday_steps_avg:,} steps** vs. Weekends **{we.weekend_steps_avg:,} steps** ({step_sign}{we.steps_diff:,} steps).  \n"
            f"- **Hydration**: Weekdays averaged **{we.weekday_water_avg:.1f} glasses** vs. Weekends **{we.weekend_water_avg:.1f} glasses**."
        )

    # 4. Hydration query
    if any(k in q for k in ["water", "hydration", "drink", "glasses"]):
        water_avg = clean_df["water_glasses"].dropna().mean()
        days_met = (clean_df["water_glasses"] >= goals.water_target).sum()
        pct_met = (days_met / n) * 100.0
        return (
            f"💧 **Hydration Performance**:  \n"
            f"You averaged **{water_avg:.1f} glasses of water per day**. "
            f"You met or exceeded your daily target ({goals.water_target} glasses) on "
            f"**{days_met} out of {n} days ({pct_met:.0f}%)**."
        )

    # 5. Sleep regularity / deficit query
    if any(k in q for k in ["sleep", "rest", "bed", "hours", "night"]):
        sleep_avg = clean_df["sleep_hours"].dropna().mean()
        sleep_std = clean_df["sleep_hours"].dropna().std()
        days_in_target = ((clean_df["sleep_hours"] >= goals.sleep_min) & (clean_df["sleep_hours"] <= goals.sleep_max)).sum()
        pct_in_target = (days_in_target / n) * 100.0
        return (
            f"💤 **Sleep Regularity Review**:  \n"
            f"Average recorded sleep was **{sleep_avg:.1f} hrs/night** with a standard deviation of **{sleep_std:.2f} hrs**. "
            f"Your sleep fell within your target window ({goals.sleep_min}–{goals.sleep_max} hrs) on "
            f"**{days_in_target} of {n} days ({pct_in_target:.0f}%)**."
        )

    # 6. Chronotype / Social Jetlag query
    if any(k in q for k in ["chronotype", "jetlag", "circadian", "social jetlag", "owl", "lark"]):
        chrono = calculate_circadian_chronotype(clean_df)
        if not chrono:
            return "Requires at least 7 recorded days spanning workdays and weekends to evaluate chronotype."
        return (
            f"{chrono.chronotype_icon} **Circadian Chronotype & Social Jetlag**:  \n"
            f"Your behavioral profile is classified as **{chrono.chronotype}**.  \n"
            f"Your **Social Jetlag Index is {chrono.social_jetlag_minutes} minutes** "
            f"(the difference between your weekend and weekday sleep schedules), with a "
            f"Circadian Alignment Score of **{chrono.circadian_alignment_score}/100** ({chrono.alignment_tier})."
        )

    # 7. Resiliency / Uptime query
    if any(k in q for k in ["resilience", "uptime", "availability", "ibm z", "recovery", "mttr"]):
        res = calculate_autonomic_resiliency(clean_df, goals)
        return (
            f"🛡️ **IBM Z Autonomic Habit Resiliency**:  \n"
            f"Your **Habit Availability stands at {res.uptime_pct}% Uptime** across {res.total_active_days} days.  \n"
            f"- Status: **{res.autonomic_health_status}**  \n"
            f"- Mean Time to Recovery (MTTR): **{res.mean_time_to_recovery_days} days** (average time to bounce back to routine after a drop).  \n"
            f"- Successful Days: **{res.successful_days} of {res.total_active_days}**."
        )

    # 8. Anomaly / Outlier query
    if any(k in q for k in ["anomaly", "anomalies", "outlier", "outliers", "unusual", "extreme"]):
        anomalies = detect_anomalies(clean_df)
        if anomalies.empty:
            return "✅ **No statistical anomalies detected**: All recorded days fall within typical expected ranges."
        return (
            f"⚠️ **Detected {len(anomalies)} statistical outlier(s)** in your records:  \n"
            + "\n".join([f"- **{row['date']}**: {row['metric']} was {row['value']} (expected range: {row['typical_range']})" for _, row in anomalies.head(5).iterrows()])
        )

    # Default general summary
    stats = calculate_dashboard_stats(clean_df)
    comp = calculate_composite_score(clean_df, goals)
    return (
        f"📊 **Executive Routine Summary**:  \n"
        f"Across **{n} recorded days**, your **Composite Behavioral Consistency Score is {comp.overall_score}/100** ({comp.tier}).  \n"
        f"- Daily Steps Average: **{int(stats.steps_summary.mean):,}**  \n"
        f"- Sleep Average: **{stats.sleep_summary.mean:.1f} hrs**  \n"
        f"- Water Average: **{stats.water_summary.mean:.1f} glasses**  \n"
        f"- Logging Completion: **{stats.completion_rate_pct:.0f}%**"
    )
