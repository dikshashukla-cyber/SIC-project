"""Carbon Design System & Multi-Theme Injector."""

from __future__ import annotations


def get_theme_css(theme_mode: str) -> str:
    """Returns CSS styles matching Enterprise Light, Executive Dark, or Cyberpunk Bio-Hacker Neon."""
    if theme_mode == "Executive Dark":
        return """
        <style>
        /* Executive Dark Mode */
        .stApp {
            background-color: #0f172a !important;
            color: #f8fafc !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        .main-header {
            color: #38bdf8 !important;
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
            letter-spacing: -0.02em;
            font-size: 2.2rem;
            font-weight: 700;
        }
        .sub-header {
            color: #94a3b8 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1.05rem;
            margin-bottom: 1rem;
        }
        .disclaimer-banner {
            background-color: #1e293b !important;
            border-left: 4px solid #0284c7 !important;
            border: 1px solid #334155 !important;
            color: #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.2rem;
        }
        .disclaimer-banner strong {
            color: #38bdf8 !important;
        }
        .resilience-banner {
            background-color: #064e3b !important;
            border: 1px solid #059669 !important;
            border-left: 4px solid #10b981 !important;
            color: #6ee7b7 !important;
            border-radius: 8px !important;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.2rem;
        }
        .metric-card {
            background: #1e293b !important;
            border: 1px solid #334155 !important;
            color: #f8fafc !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
            border-radius: 10px !important;
            padding: 1rem 0.8rem;
            text-align: center;
        }
        .metric-title {
            color: #94a3b8 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.78rem;
            text-transform: uppercase;
            font-weight: 600;
        }
        .metric-value {
            color: #ffffff !important;
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
            font-size: 1.7rem;
            font-weight: 700;
        }
        .metric-sub {
            color: #cbd5e1 !important;
            font-size: 0.8rem;
        }
        .badge-card {
            background: #1e293b !important;
            border: 1px solid #334155 !important;
            color: #f8fafc !important;
            padding: 12px 14px;
            border-radius: 8px;
        }
        .badge-unlocked {
            border: 1px solid #10b981 !important;
            background: #064e3b !important;
        }
        .badge-locked {
            border: 1px solid #334155 !important;
            background: #1e293b !important;
            opacity: 0.65;
        }
        section[data-testid="stSidebar"] {
            background-color: #1e293b !important;
            border-right: 1px solid #334155 !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {
            color: #e2e8f0 !important;
            font-weight: 500 !important;
        }
        </style>
        """
    elif theme_mode == "Cyberpunk Bio-Hacker (Neon Glass)":
        return """
        <style>
        /* Cyberpunk Bio-Hacker Neon Glass Mode */
        .stApp {
            background: radial-gradient(circle at top left, #0d1322 0%, #060911 100%) !important;
            color: #f1f5f9 !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        .main-header {
            background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #9d4edd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.3rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        }
        .sub-header {
            color: #94a3b8 !important;
            font-size: 1.05rem;
            margin-bottom: 1rem;
        }
        .disclaimer-banner {
            background: rgba(15, 23, 42, 0.85) !important;
            backdrop-filter: blur(12px) !important;
            border-left: 4px solid #00f2fe !important;
            border: 1px solid rgba(0, 242, 254, 0.3);
            color: #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.1);
        }
        .disclaimer-banner strong {
            color: #00f2fe !important;
        }
        .resilience-banner {
            background: rgba(6, 78, 59, 0.5) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(16, 185, 129, 0.5) !important;
            border-left: 4px solid #10b981 !important;
            color: #6ee7b7 !important;
            border-radius: 8px !important;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
        }
        .metric-card {
            background: rgba(15, 23, 42, 0.85) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 12px !important;
            padding: 1.1rem 0.8rem;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.2s ease-in-out;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(0, 242, 254, 0.5) !important;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.25);
        }
        .metric-title {
            color: #94a3b8 !important;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 700;
        }
        .metric-value {
            color: #f8fafc !important;
            font-size: 1.8rem;
            font-weight: 800;
            text-shadow: 0 0 12px rgba(255, 255, 255, 0.2);
        }
        .metric-sub {
            color: #cbd5e1 !important;
            font-size: 0.8rem;
        }
        .badge-card {
            background: rgba(15, 23, 42, 0.85) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            padding: 12px 14px;
        }
        .badge-unlocked {
            border: 1px solid rgba(16, 185, 129, 0.6) !important;
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
        }
        .badge-locked {
            opacity: 0.5;
        }
        section[data-testid="stSidebar"] {
            background: #090d16 !important;
            border-right: 1px solid rgba(0, 242, 254, 0.2) !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            color: #00f2fe !important;
            font-weight: 700 !important;
        }
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {
            color: #e2e8f0 !important;
            font-weight: 500 !important;
        }
        </style>
        """
    else:
        return """
        <style>
        /* Enterprise Modern Light Mode (High Contrast & Clean Readability) */
        .stApp {
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        .main-header {
            font-size: 2.3rem;
            font-weight: 800;
            color: #0284c7;
            background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
            letter-spacing: -0.02em;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #475569;
            margin-bottom: 1rem;
            font-weight: 500;
        }
        .disclaimer-banner {
            background-color: #ffffff !important;
            border: 1px solid #bae6fd !important;
            border-left: 5px solid #0284c7 !important;
            border-radius: 8px !important;
            padding: 0.95rem 1.25rem;
            margin-bottom: 1.2rem;
            color: #0f172a !important;
            font-size: 0.92rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        .disclaimer-banner strong {
            color: #0284c7 !important;
        }
        .resilience-banner {
            background-color: #f0fdf4 !important;
            border: 1px solid #86efac !important;
            border-left: 5px solid #16a34a !important;
            border-radius: 8px !important;
            padding: 0.95rem 1.25rem;
            margin-bottom: 1.2rem;
            color: #14532d !important;
            font-weight: 600;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        .metric-card {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 1.1rem 0.9rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
            text-align: center;
            transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
            border-color: #cbd5e1 !important;
        }
        .metric-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
            color: #64748b !important;
            margin-bottom: 0.35rem;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: #0f172a !important;
            margin-bottom: 0.2rem;
        }
        .metric-sub {
            font-size: 0.82rem;
            color: #64748b !important;
            font-weight: 500;
        }
        .badge-card {
            background: #ffffff !important;
            border-radius: 10px;
            padding: 14px 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            margin-bottom: 10px;
            border: 1px solid #e2e8f0;
            height: 100%;
        }
        .badge-unlocked {
            border: 1px solid #86efac !important;
            background: #f0fdf4 !important;
        }
        .badge-locked {
            border: 1px solid #e2e8f0 !important;
            background: #f8fafc !important;
            opacity: 0.75;
        }
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0 !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {
            color: #334155 !important;
            font-weight: 600 !important;
        }
        </style>
        """
