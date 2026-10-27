"""Evaluator persona datasets generator for Personal Wellness Platform.

Provides 3 distinct pre-configured synthetic personas for live demonstration:
1. The Active Professional: Highly consistent weekday routine, high hydration, weekend outdoor activities.
2. The Variable Night Owl: Weekday sleep deficits, weekend sleep catch-up, variable steps.
3. The Balanced Habit Tracker: Steady 7.5-8.0 hrs sleep, 8 glasses water, moderate daily activity.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_persona_dataset(persona_key: str, days: int = 60, end_date_str: str = "2026-10-15") -> pd.DataFrame:
    """
    Generates a realistic 60-day synthetic wellness dataset for a selected persona.
    """
    dates = pd.date_range(end=end_date_str, periods=days, freq="D")
    rng = np.random.default_rng(seed=42 if persona_key == "active" else (101 if persona_key == "night_owl" else 202))

    data = []
    for d in dates:
        is_weekend = d.weekday() >= 5

        if persona_key == "active":
            # Active Professional: high steps, long weekend hikes, consistent sleep
            sleep = round(rng.normal(7.3, 0.4) if not is_weekend else rng.normal(8.0, 0.5), 1)
            sleep = max(5.5, min(10.0, sleep))
            steps = int(rng.normal(9200, 800) if not is_weekend else rng.normal(12500, 1500))
            steps = max(4000, min(25000, steps))
            water = int(rng.normal(9, 1) if not is_weekend else rng.normal(10, 1.2))
            water = max(6, min(16, water))
            mood = int(rng.choice([4, 5], p=[0.4, 0.6]))
            activity = int(rng.normal(45, 10) if not is_weekend else rng.normal(80, 20))
            activity = max(20, min(180, activity))

        elif persona_key == "night_owl":
            # Variable Night Owl: short sleep weekdays, catch-up weekends, erratic steps
            sleep = round(rng.normal(6.1, 0.6) if not is_weekend else rng.normal(8.8, 0.7), 1)
            sleep = max(4.5, min(11.5, sleep))
            steps = int(rng.normal(6500, 1200) if not is_weekend else rng.normal(5400, 1600))
            steps = max(2500, min(15000, steps))
            water = int(rng.normal(6, 1.2))
            water = max(3, min(12, water))
            mood = int(rng.choice([3, 4, 5], p=[0.4, 0.4, 0.2]))
            activity = int(rng.normal(25, 10) if not is_weekend else rng.normal(20, 15))
            activity = max(5, min(90, activity))

        else:
            # Balanced Habit Tracker: steady routines throughout
            sleep = round(rng.normal(7.6, 0.3), 1)
            sleep = max(6.5, min(9.0, sleep))
            steps = int(rng.normal(8500, 600))
            steps = max(6000, min(12000, steps))
            water = int(rng.normal(8, 0.8))
            water = max(6, min(12, water))
            mood = int(rng.choice([4, 5], p=[0.5, 0.5]))
            activity = int(rng.normal(40, 8))
            activity = max(15, min(75, activity))

        data.append({
            "date": d.strftime("%Y-%m-%d"),
            "sleep_hours": sleep,
            "steps": steps,
            "water_glasses": water,
            "mood_score": mood,
            "activity_minutes": activity,
        })

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df


PERSONA_PROFILES = {
    "active": {
        "name": "🏃 The Active Professional",
        "description": "Consistent workday routine, high hydration, and active weekend hikes.",
        "sample_key": "active",
    },
    "night_owl": {
        "name": "🦉 The Variable Night Owl",
        "description": "Weekday sleep deficit with weekend catch-up sleep and variable step habits.",
        "sample_key": "night_owl",
    },
    "balanced": {
        "name": "🧘 The Balanced Habit Tracker",
        "description": "Highly consistent sleep, steady hydration, and predictable daily activity.",
        "sample_key": "balanced",
    },
}
