"""IBM Z Carbon Design System & Multi-Theme Injector."""

from __future__ import annotations


def get_theme_css(theme_mode: str) -> str:
    """Returns CSS styles matching Enterprise Light, IBM Z Mainframe Terminal Dark, or Cyberpunk Bio-Hacker Neon."""
    if theme_mode == "IBM Z Mainframe (Dark)":
        return """
        <style>
        /* IBM Z Mainframe Terminal Mode */
        .stApp {
            background-color: #121619 !important;
            color: #f4f4f4 !important;
            font-family: 'IBM Plex Sans', -apple-system, sans-serif !important;
        }
        .main-header {
            color: #78a9ff !important;
            font-family: 'IBM Plex Mono', monospace !important;
            letter-spacing: -0.02em;
            font-size: 2.2rem;
            font-weight: 700;
        }
        .sub-header {
            color: #8d8d8d !important;
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 1.05rem;
            margin-bottom: 1rem;
        }
        .disclaimer-banner {
            background-color: #1e1e1e !important;
            border-left: 4px solid #0f62fe !important;
            color: #e0e0e0 !important;
            border-radius: 4px !important;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.2rem;
        }
        .disclaimer-banner strong {
            color: #78a9ff !important;
        }
        .resilience-banner {
            background-color: #0f2317 !important;
            border: 1px solid #198038 !important;
            border-left: 4px solid #24a148 !important;
            color: #42be65 !important;
            border-radius: 4px !important;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.2rem;
        }
        .metric-card {
            background: #262626 !important;
            border: 1px solid #393939 !important;
            color: #f4f4f4 !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
            border-radius: 6px !important;
            padding: 1rem 0.8rem;
            text-align: center;
        }
        .metric-title {
            color: #8d8d8d !important;
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 0.78rem;
            text-transform: uppercase;
        }
        .metric-value {
            color: #ffffff !important;
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 1.7rem;
            font-weight: 700;
        }
        .metric-sub {
            color: #c6c6c6 !important;
            font-size: 0.8rem;
        }
        .badge-card {
            background: #262626 !important;
            border: 1px solid #393939 !important;
            color: #f4f4f4 !important;
            padding: 12px 14px;
            border-radius: 8px;
        }
        .badge-unlocked {
            border: 1px solid #24a148 !important;
            background: #0f2317 !important;
        }
        .badge-locked {
            border: 1px solid #393939 !important;
            background: #1e1e1e !important;
            opacity: 0.65;
        }
        section[data-testid="stSidebar"] {
            background-color: #161616 !important;
            border-right: 1px solid #393939 !important;
        }
        </style>
        """
    elif theme_mode == "Cyberpunk Bio-Hacker (Neon Glass)":
        return """
        <style>
        /* Cyberpunk Bio-Hacker Neon Glass Mode */
        .stApp {
            background: radial-gradient(circle at top left, #0d1322 0%, #060911 100%) !important;
            color: #e2e8f0 !important;
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
            background: rgba(15, 23, 42, 0.75) !important;
            backdrop-filter: blur(12px) !important;
            border-left: 4px solid #00f2fe !important;
            border: 1px solid rgba(0, 242, 254, 0.25);
            color: #cbd5e1 !important;
            border-radius: 8px !important;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.1);
        }
        .disclaimer-banner strong {
            color: #00f2fe !important;
        }
        .resilience-banner {
            background: rgba(6, 78, 59, 0.35) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(16, 185, 129, 0.4) !important;
            border-left: 4px solid #10b981 !important;
            color: #34d399 !important;
            border-radius: 8px !important;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
        }
        .metric-card {
            background: rgba(15, 23, 42, 0.65) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 1.1rem 0.8rem;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.2s ease-in-out;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(0, 242, 254, 0.4) !important;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
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
            color: #64748b !important;
            font-size: 0.8rem;
        }
        .badge-card {
            background: rgba(15, 23, 42, 0.65) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
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
            background: rgba(6, 9, 17, 0.95) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        </style>
        """
    else:
        return """
        <style>
        /* Enterprise Light Mode */
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #475569;
            margin-bottom: 1rem;
        }
        .disclaimer-banner {
            background-color: #f8fafc;
            border-left: 4px solid #0284c7;
            border-radius: 6px;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.2rem;
            color: #1e293b;
            font-size: 0.92rem;
        }
        .disclaimer-banner strong {
            color: #0369a1;
        }
        .resilience-banner {
            background-color: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-left: 4px solid #16a34a;
            border-radius: 8px;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.2rem;
            color: #14532d;
        }
        .metric-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1rem 0.8rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            text-align: center;
            transition: transform 0.15s ease-in-out;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.08);
        }
        .metric-title {
            font-size: 0.78rem;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
            color: #64748b;
            margin-bottom: 0.3rem;
        }
        .metric-value {
            font-size: 1.7rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.2rem;
        }
        .metric-sub {
            font-size: 0.8rem;
            color: #64748b;
        }
        .badge-card {
            background: #ffffff;
            border-radius: 8px;
            padding: 12px 14px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            margin-bottom: 10px;
            height: 100%;
        }
        .badge-unlocked {
            border: 1px solid #86efac;
            background: #f0fdf4;
        }
        .badge-locked {
            border: 1px solid #e2e8f0;
            background: #f8fafc;
            opacity: 0.75;
        }
        </style>
        """
