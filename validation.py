"""Data validation rules, schema verification, and anomaly detection for Wellness Dashboard."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


REQUIRED_COLUMNS = ["date", "sleep_hours", "steps", "water_glasses"]
OPTIONAL_COLUMNS = ["mood_score", "activity_minutes"]

# Data validation ranges (non-medical validation thresholds)
VALIDATION_RULES = {
    "sleep_hours": {"min": 0.0, "max": 24.0, "type": "float", "name": "Sleep Hours"},
    "steps": {"min": 0, "max": 100000, "type": "int", "name": "Daily Steps"},
    "water_glasses": {"min": 0, "max": 50, "type": "int", "name": "Water Glasses"},
    "mood_score": {"min": 1, "max": 5, "type": "int", "name": "Mood Score (1-5)"},
    "activity_minutes": {"min": 0, "max": 1440, "type": "int", "name": "Activity Minutes"},
}


@dataclass
class ValidationReport:
    """Represents the outcome of dataset validation."""
    is_valid: bool
    schema_errors: List[str] = field(default_factory=list)
    total_records: int = 0
    valid_count: int = 0
    invalid_count: int = 0
    valid_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    invalid_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    missing_counts: Dict[str, int] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    @property
    def has_records(self) -> bool:
        return self.valid_count > 0


def validate_wellness_data(df: pd.DataFrame) -> ValidationReport:
    """
    Validates a pandas DataFrame containing wellness records.

    Rules applied:
    - Verifies required columns exist.
    - Ensures optional columns are present or initialized as NaN.
    - Parses and validates dates (YYYY-MM-DD format).
    - Checks numeric ranges without coercing nulls to zero.
    - Separates valid rows from invalid rows with explicit error reasons.
    """
    if df is None or not isinstance(df, pd.DataFrame):
        return ValidationReport(
            is_valid=False,
            schema_errors=["Input data must be a valid pandas DataFrame."],
        )

    if df.empty:
        return ValidationReport(
            is_valid=False,
            schema_errors=["The uploaded dataset is empty."],
            total_records=0,
        )

    # Normalize column names: strip whitespace and lowercase
    working_df = df.copy()
    working_df.columns = [str(c).strip().lower() for c in working_df.columns]

    # Check for missing required columns
    missing_required = [col for col in REQUIRED_COLUMNS if col not in working_df.columns]
    if missing_required:
        return ValidationReport(
            is_valid=False,
            schema_errors=[
                f"Missing required column(s): {', '.join(missing_required)}. "
                f"Required schema: {', '.join(REQUIRED_COLUMNS)}."
            ],
            total_records=len(working_df),
        )

    # Ensure optional columns exist (populated with NaN if absent)
    for opt_col in OPTIONAL_COLUMNS:
        if opt_col not in working_df.columns:
            working_df[opt_col] = np.nan

    total_records = len(working_df)
    row_issues: List[List[str]] = [[] for _ in range(total_records)]

    # 1. Date Validation
    parsed_dates = pd.to_datetime(working_df["date"], errors="coerce")
    for idx, (original, parsed) in enumerate(zip(working_df["date"], parsed_dates)):
        if pd.isna(parsed):
            row_issues[idx].append(f"Invalid date value: '{original}'")
        else:
            if parsed.year < 2000 or parsed.year > 2100:
                row_issues[idx].append(f"Date year out of expected range (2000-2100): {parsed.date()}")

    working_df["parsed_date"] = parsed_dates.dt.date

    # 2. Check for duplicate dates
    valid_dates_series = working_df.loc[parsed_dates.notna(), "parsed_date"]
    duplicate_dates = set(valid_dates_series[valid_dates_series.duplicated()])
    warnings = []
    if duplicate_dates:
        warnings.append(
            f"Found {len(duplicate_dates)} duplicate date(s) in dataset: "
            f"{', '.join(str(d) for d in sorted(duplicate_dates)[:5])}."
        )

    # 3. Numeric range validation
    for col, rule in VALIDATION_RULES.items():
        is_optional = col in OPTIONAL_COLUMNS
        raw_series = working_df[col]
        numeric_series = pd.to_numeric(raw_series, errors="coerce")

        for idx, (raw_val, num_val) in enumerate(zip(raw_series, numeric_series)):
            if pd.isna(raw_val) or (isinstance(raw_val, str) and raw_val.strip() == ""):
                if not is_optional:
                    row_issues[idx].append(f"Missing required value for '{col}'")
                continue

            if pd.isna(num_val):
                row_issues[idx].append(f"Non-numeric value in '{col}': '{raw_val}'")
                continue

            min_val = rule["min"]
            max_val = rule["max"]
            if num_val < min_val or num_val > max_val:
                row_issues[idx].append(
                    f"{rule['name']} ({num_val}) out of expected range [{min_val}, {max_val}]"
                )

        working_df[col] = numeric_series

    # Missing counts
    all_cols = REQUIRED_COLUMNS + OPTIONAL_COLUMNS
    missing_counts = {col: int(working_df[col].isna().sum()) for col in all_cols}

    # Separate valid and invalid rows
    working_df["validation_issues"] = ["; ".join(issues) for issues in row_issues]
    is_row_valid = [len(issues) == 0 for issues in row_issues]

    valid_df = working_df[is_row_valid].copy()
    invalid_df = working_df[[not v for v in is_row_valid]].copy()

    if not valid_df.empty:
        valid_df["date"] = pd.to_datetime(valid_df["parsed_date"])
        valid_df = valid_df.sort_values("date").reset_index(drop=True)
        valid_df = valid_df.drop(columns=["parsed_date", "validation_issues"])

    if not invalid_df.empty:
        invalid_df = invalid_df.drop(columns=["parsed_date"]).reset_index(drop=True)

    return ValidationReport(
        is_valid=True,
        schema_errors=[],
        total_records=total_records,
        valid_count=len(valid_df),
        invalid_count=len(invalid_df),
        valid_df=valid_df,
        invalid_df=invalid_df,
        missing_counts=missing_counts,
        warnings=warnings,
    )


def detect_anomalies(df: pd.DataFrame, iqr_multiplier: float = 2.0) -> pd.DataFrame:
    """
    Identifies statistical outliers/anomalies in numeric wellness metrics using IQR.
    Returns an anomaly log dataframe with date, metric, value, expected range, and note.
    """
    if df.empty or len(df) < 7:
        return pd.DataFrame(columns=["date", "metric", "value", "typical_range", "note"])

    anomalies = []
    numeric_cols = ["sleep_hours", "steps", "water_glasses"]
    if "activity_minutes" in df.columns and df["activity_minutes"].notna().sum() >= 7:
        numeric_cols.append("activity_minutes")

    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 7:
            continue

        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        if iqr == 0:
            std = float(series.std())
            if std == 0:
                continue
            mean_val = float(series.mean())
            lower_bound = max(0.0, mean_val - 2.0 * std)
            upper_bound = mean_val + 2.0 * std
        else:
            lower_bound = max(0.0, q1 - iqr_multiplier * iqr)
            upper_bound = q3 + iqr_multiplier * iqr

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        for _, row in outliers.iterrows():
            val = row[col]
            direction = "High" if val > upper_bound else "Low"
            anomalies.append({
                "date": row["date"].strftime("%Y-%m-%d") if hasattr(row["date"], "strftime") else str(row["date"]),
                "metric": col.replace("_", " ").title(),
                "value": round(val, 1) if isinstance(val, float) else val,
                "typical_range": f"{round(lower_bound, 1)} – {round(upper_bound, 1)}",
                "note": f"Unusually {direction} value compared to typical pattern",
            })

    if not anomalies:
        return pd.DataFrame(columns=["date", "metric", "value", "typical_range", "note"])

    anomaly_df = pd.DataFrame(anomalies)
    return anomaly_df.sort_values("date").reset_index(drop=True)
