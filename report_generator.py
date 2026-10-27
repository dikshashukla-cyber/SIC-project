"""Executive Wellness Report generator (HTML/Printable format) for IBM Z Datathon 2026."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional
import pandas as pd

try:
    from src.metrics import DashboardStats, CompositeScore, WeekdayWeekendStats, StreakInfo
    from src.insights import TrendReport
    from src.resilience import ResiliencyReport
    from src.badges import AchievementBadge
except (ImportError, ModuleNotFoundError):
    from metrics import DashboardStats, CompositeScore, WeekdayWeekendStats, StreakInfo
    from insights import TrendReport
    from resilience import ResiliencyReport
    from badges import AchievementBadge


def generate_executive_html_report(
    stats: DashboardStats,
    composite: CompositeScore,
    trend_report: TrendReport,
    streaks: dict[str, StreakInfo],
    weekend_stats: Optional[WeekdayWeekendStats] = None,
    resilience_report: Optional[ResiliencyReport] = None,
    badges: Optional[List[AchievementBadge]] = None,
    persona_name: Optional[str] = None,
) -> str:
    """
    Builds a self-contained, beautifully styled HTML executive summary report.
    Can be opened in any browser and saved/printed to PDF (Ctrl+P).
    """
    now_str = datetime.now().strftime("%B %d, %Y - %H:%M")

    # Render Streaks HTML
    streak_cards_html = ""
    for _, s in streaks.items():
        streak_cards_html += f"""
        <div class="card" style="flex: 1; min-width: 140px; text-align: center;">
            <div class="card-label">{s.metric_name}</div>
            <div class="card-value" style="font-size: 1.6rem; color: #0284c7;">{s.current_streak} days</div>
            <div class="card-sub">Longest: {s.longest_streak} days ({s.target_description})</div>
        </div>
        """

    # Render Badges HTML if available
    badges_html = ""
    if badges:
        badge_items = ""
        for b in badges:
            status_style = "border: 1px solid #bbf7d0; background: #f0fdf4;" if b.unlocked else "border: 1px solid #e2e8f0; background: #f8fafc; opacity: 0.65;"
            badge_items += f"""
            <div style="flex: 1; min-width: 220px; {status_style} border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                <div style="font-size: 1.1rem; font-weight: 700; color: #0f172a;">{b.icon} {b.title}</div>
                <div style="font-size: 0.8rem; color: #475569; margin: 3px 0;">{b.description}</div>
                <div style="font-size: 0.78rem; font-weight: 600; color: {'#16a34a' if b.unlocked else '#64748b'};">
                    {'✅ Unlocked' if b.unlocked else '🔒 In Progress'}: {b.progress_label}
                </div>
            </div>
            """
        badges_html = f"""
        <h3 style="margin-top: 24px; color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">🏆 Habit Milestones & Badges</h3>
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;">
            {badge_items}
        </div>
        """

    # Render Observations HTML
    obs_html = ""
    for obs in trend_report.observations:
        tag_color = {
            "Increase": "#16a34a",
            "Decrease": "#dc2626",
            "Steady": "#0284c7",
            "Info": "#475569",
        }.get(obs.tag, "#475569")

        obs_html += f"""
        <div style="border-left: 3px solid {tag_color}; background: #f8fafc; padding: 10px 14px; margin-bottom: 8px; border-radius: 4px;">
            <strong style="color: #0f172a;">{obs.category}</strong>: {obs.summary}
            <div style="font-size: 0.85rem; color: #475569; margin-top: 3px;">{obs.detail}</div>
        </div>
        """

    # Render Resiliency Box if available
    resilience_box_html = ""
    if resilience_report:
        resilience_box_html = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 14px 20px; margin-bottom: 20px;">
            <div>
                <div style="font-size: 0.78rem; font-weight: 700; color: #166534; text-transform: uppercase;">🛡️ IBM Z Autonomic Habit Resiliency</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-top: 2px;">{resilience_report.autonomic_health_status}</div>
                <div style="font-size: 0.85rem; color: #475569; margin-top: 2px;">{resilience_report.resilience_summary}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.6rem; font-weight: 800; color: {resilience_report.status_color};">{resilience_report.uptime_pct}%</div>
                <div style="font-size: 0.75rem; color: #64748b;">Habit Uptime ({resilience_report.mean_time_to_recovery_days}d MTTR)</div>
            </div>
        </div>
        """

    # Render Weekend Comparison HTML if available
    weekend_html = ""
    if weekend_stats:
        weekend_html = f"""
        <h3 style="margin-top: 24px; color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">📅 Weekday vs. Weekend Behavioral Comparison</h3>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #f1f5f9; text-align: left;">
                    <th style="padding: 8px; border: 1px solid #e2e8f0;">Metric</th>
                    <th style="padding: 8px; border: 1px solid #e2e8f0;">Weekdays (Mon–Fri)</th>
                    <th style="padding: 8px; border: 1px solid #e2e8f0;">Weekends (Sat–Sun)</th>
                    <th style="padding: 8px; border: 1px solid #e2e8f0;">Difference</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;"><strong>Average Sleep</strong></td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{weekend_stats.weekday_sleep_avg:.1f} hrs</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{weekend_stats.weekend_sleep_avg:.1f} hrs</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{'+' if weekend_stats.sleep_diff > 0 else ''}{weekend_stats.sleep_diff:.1f} hrs</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;"><strong>Daily Steps</strong></td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{weekend_stats.weekday_steps_avg:,} steps</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{weekend_stats.weekend_steps_avg:,} steps</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{'+' if weekend_stats.steps_diff > 0 else ''}{weekend_stats.steps_diff:,} steps</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;"><strong>Hydration</strong></td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{weekend_stats.weekday_water_avg:.1f} glasses</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{weekend_stats.weekend_water_avg:.1f} glasses</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{'+' if weekend_stats.water_diff > 0 else ''}{weekend_stats.water_diff:.1f} glasses</td>
                </tr>
            </tbody>
        </table>
        """

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Executive Wellness Report — IBM Z Datathon 2026</title>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1e293b;
        background-color: #f8fafc;
        margin: 0;
        padding: 24px;
    }}
    .report-container {{
        max-width: 900px;
        margin: 0 auto;
        background: #ffffff;
        padding: 36px 40px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    .header {{
        border-bottom: 2px solid #0284c7;
        padding-bottom: 16px;
        margin-bottom: 20px;
    }}
    .disclaimer {{
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #16a34a;
        padding: 10px 14px;
        font-size: 0.85rem;
        color: #166534;
        border-radius: 4px;
        margin-bottom: 24px;
    }}
    .cards-row {{
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 24px;
    }}
    .card {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px;
        flex: 1;
        min-width: 150px;
    }}
    .card-label {{
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 4px;
    }}
    .card-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
    }}
    .card-sub {{
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 2px;
    }}
    .score-badge {{
        display: inline-block;
        padding: 6px 14px;
        border-radius: 9999px;
        color: white;
        font-weight: 700;
        font-size: 1rem;
        background: {composite.tier_color};
    }}
    @media print {{
        body {{ background: #ffffff; padding: 0; }}
        .report-container {{ border: none; box-shadow: none; padding: 0; }}
    }}
</style>
</head>
<body>
<div class="report-container">
    <div class="header">
        <h1 style="margin: 0; font-size: 1.8rem; color: #0f172a;">Executive Wellness Report</h1>
        <div style="font-size: 0.9rem; color: #64748b; margin-top: 4px;">
            IBM Z Datathon 2026 Prototype &bull; Generated: {now_str}
            {f'&bull; Profile: <strong>{persona_name}</strong>' if persona_name else ''}
        </div>
    </div>

    <div class="disclaimer">
        <strong>⚠️ Non-Medical Health Notice:</strong>
        This report summarizes self-recorded wellness habits for personal review. It is not medical advice, clinical diagnosis, or a predictive health evaluation.
    </div>

    {resilience_box_html}

    <div style="display: flex; align-items: center; justify-content: space-between; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px 24px; margin-bottom: 24px;">
        <div>
            <div style="font-size: 0.85rem; text-transform: uppercase; font-weight: 600; color: #64748b;">Composite Behavioral Consistency Index</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #0f172a; margin-top: 4px;">{composite.tier}</div>
            <div style="font-size: 0.85rem; color: #475569; margin-top: 2px;">{composite.summary_text}</div>
        </div>
        <div style="text-align: right;">
            <div class="score-badge">{composite.overall_score} / 100</div>
        </div>
    </div>

    <h3 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">📊 Key Period Metrics</h3>
    <div class="cards-row">
        <div class="card">
            <div class="card-label">Average Sleep</div>
            <div class="card-value">{stats.sleep_summary.mean or 'N/A'} hrs</div>
            <div class="card-sub">Range: {stats.sleep_summary.min_val or 0} – {stats.sleep_summary.max_val or 0} hrs</div>
        </div>
        <div class="card">
            <div class="card-label">Daily Steps</div>
            <div class="card-value">{int(stats.steps_summary.mean or 0):,}</div>
            <div class="card-sub">Total: {int(stats.steps_summary.total or 0):,} steps</div>
        </div>
        <div class="card">
            <div class="card-label">Hydration</div>
            <div class="card-value">{stats.water_summary.mean or 'N/A'} gls</div>
            <div class="card-sub">Total: {int(stats.water_summary.total or 0)} glasses</div>
        </div>
        <div class="card">
            <div class="card-label">Logging Rate</div>
            <div class="card-value">{stats.completion_rate_pct:.0f}%</div>
            <div class="card-sub">{stats.recorded_days_count} of {stats.total_days_in_range} days</div>
        </div>
    </div>

    <h3 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">🔥 Habit Streaks</h3>
    <div class="cards-row">
        {streak_cards_html}
    </div>

    {badges_html}

    {weekend_html}

    <h3 style="margin-top: 24px; color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">🔍 Transparent Trend Observations</h3>
    <div style="margin-top: 10px;">
        {obs_html}
    </div>

    <div style="margin-top: 36px; padding-top: 12px; border-top: 1px solid #e2e8f0; font-size: 0.8rem; color: #94a3b8; text-align: center;">
        Prepared with Wellness Dashboard (Unique Edition) &bull; IBM Z Datathon 2026 Prototype &bull; Single-User Personal Tracking
    </div>
</div>
</body>
</html>
"""
    return html_template
