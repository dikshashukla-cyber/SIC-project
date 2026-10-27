"""
Academic Defense Room & Viva Voce Preparation Suite.
Provides mathematical derivations, LaTeX formulas, architecture maps, and model Q&As for evaluators.
"""

from __future__ import annotations
import streamlit as st


def render_academic_defense_tab():
    """Renders the comprehensive Academic Defense & Viva Voce Room."""
    st.markdown("### 🎓 Academic Defense Room & Evaluation Guide")
    st.caption("Theoretical frameworks, mathematical derivations, architecture breakdown, and model viva answers.")

    viva_sub1, viva_sub2, viva_sub3, viva_sub4 = st.tabs([
        "📐 Mathematical Formulations",
        "🎙️ Viva Voce Q&A Simulator",
        "🏛️ System Architecture",
        "🛡️ Data Quality Rules (DQR)",
    ])

    # ---------------- SUBTAB 1: MATHEMATICAL FORMULATIONS ----------------
    with viva_sub1:
        st.markdown("#### 1. Longitudinal Moving Averages & Trend Filtering")
        st.markdown(
            r"""
            To isolate authentic habitual behavioral patterns from diurnal random noise, we compute a 7-day backward rolling simple moving average ($\text{SMA}_{7d}$):
            $$\mu_{7d}(t) = \frac{1}{7} \sum_{i=0}^{6} x(t - i)$$
            Where $x(t)$ represents the raw biometric record (sleep hours, step volume, water glasses) on date $t$.
            """
        )

        st.markdown("---")
        st.markdown("#### 2. Composite Behavioral Consistency Index (BCI)")
        st.markdown(
            r"""
            The composite wellness score $S \in [0, 100]$ weights four non-correlated behavioral pillars:
            $$S = 0.25 \cdot f_{\text{sleep}}(s) + 0.25 \cdot f_{\text{steps}}(n) + 0.25 \cdot f_{\text{water}}(w) + 0.25 \cdot f_{\text{mood}}(m)$$
            Where each sub-function normalizes raw records against user-configured physiological bounds:
            $$f_{\text{sleep}}(s) = \min\left(100, \frac{s}{s_{\text{target}}} \times 100\right), \quad f_{\text{steps}}(n) = \min\left(100, \frac{n}{n_{\text{target}}} \times 100\right)$$
            $$f_{\text{water}}(w) = \min\left(100, \frac{w}{w_{\text{target}}} \times 100\right), \quad f_{\text{mood}}(m) = \frac{m}{5.0} \times 100$$
            """
        )

        st.markdown("---")
        st.markdown("#### 3. Autonomic Habit Resiliency & MTTR Engine")
        st.markdown(
            r"""
            Borrowing from high-availability mainframe engineering, Habit Availability ($A_{\text{habit}}$) and Mean Time to Recovery ($\text{MTTR}$) quantify psychological elasticity:
            $$A_{\text{habit}} = \left( \frac{\sum_{i=1}^{N} \mathbb{I}(\text{Target Met}_i)}{N} \right) \times 100\%$$
            $$\text{MTTR} = \frac{\sum_{k=1}^{M} \text{Downtime Days in Outage } k}{M}$$
            Where $\mathbb{I}$ is the indicator function and $M$ is the count of distinct habit failure interruptions.
            """
        )

        st.markdown("---")
        st.markdown("#### 4. Bivariate Pearson Correlation Matrix")
        st.markdown(
            r"""
            The linear covariance between habit dimensions $(X, Y)$ is computed via:
            $$r_{xy} = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2} \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}, \quad r \in [-1, +1]$$
            """
        )

    # ---------------- SUBTAB 2: VIVA VOCE Q&A SIMULATOR ----------------
    with viva_sub2:
        st.markdown("#### 🎯 Frequently Asked Viva Voce Questions & Model Responses")
        
        vivas = [
            (
                "Q1: Why is this system strictly non-medical and how is that enforced in the architecture?",
                "This platform is categorized as an educational lifestyle habit analytics system rather than a Software as a Medical Device (SaMD). Architecturally, this is enforced by: (1) Mandatory disclaimer banners on every view, (2) No clinical predictive claims or disease diagnostics, and (3) Focusing exclusively on behavioral consistency metrics (sleep regularity, step volume, hydration targets) rather than physiological biomarkers."
            ),
            (
                "Q2: How does the local Z-Cognitive Habit Assistant process natural language queries without cloud APIs?",
                "The assistant uses an offline rule-based semantic parser and token matching engine. It extracts intent keywords (e.g., 'sleep', 'weekend', 'steps', 'streak', 'resilience') and runs analytical vectorized queries directly across the in-memory pandas DataFrame. This delivers zero latency, absolute data sovereignty, and prevents sensitive health telemetry from leaking to cloud LLM providers."
            ),
            (
                "Q3: Explain the mathematical distinction between Mean Time to Recovery (MTTR) and Habit Uptime.",
                "Habit Uptime measures the raw percentage of active days where personal goals were preserved across the entire observation window. In contrast, MTTR (Mean Time to Recovery) measures behavioral elasticity: when a habit is broken, how many days does it take the user on average to return to target compliance? A user can have 80% uptime but an MTTR of 5 days (slow to recover), versus an MTTR of 1 day (rapid rebound)."
            ),
            (
                "Q4: How do you handle outliers and spurious sensor logging errors?",
                "The data ingestion pipeline applies rigorous Data Quality Rules (DQR): Sleep hours must be between 0.0 and 24.0, daily steps between 0 and 60,000, water glasses between 0 and 30, and dates must be unique ISO format strings. Records violating these boundaries trigger anomaly warnings and are sanitized before metric calculation."
            ),
            (
                "Q5: What is 'Social Jetlag' and how does the Circadian Clock calculate it?",
                "Social Jetlag is the discrepancy between an individual's biological circadian rhythm and their social schedule, measured by the difference in sleep midpoints between workdays (Monday–Friday) and weekends (Saturday–Sunday). A shift of greater than 1.5 hours suggests circadian disruption, which the dashboard flags with targeted phase stabilization recommendations."
            ),
        ]

        for q, a in vivas:
            with st.expander(f"📌 {q}", expanded=False):
                st.markdown(f"**Model Response:**\n\n{a}")

    # ---------------- SUBTAB 3: SYSTEM ARCHITECTURE ----------------
    with viva_sub3:
        st.markdown("#### 🏛️ 4-Tier Decoupled System Architecture")
        st.markdown(
            """
            ```
            ┌─────────────────────────────────────────────────────────────┐
            │                  TIER 1: PRESENTATION LAYER                  │
            │  • Streamlit Reactive UI Engine (Responsive Grid & Tabs)    │
            │  • Interactive Plotly 3D Phase Space & Radar Polygons       │
            │  • HTML5 Web Audio Synthesizer & Canvas Breathwork Trainer  │
            └──────────────────────────────┬──────────────────────────────┘
                                           │
            ┌──────────────────────────────▼──────────────────────────────┐
            │                   TIER 2: ANALYTICS & LOGIC                  │
            │  • Z-Cognitive Query Assistant (Zero-API Natural Language)   │
            │  • Autonomic Resiliency & MTTR Engine                       │
            │  • Circadian Chronotype & Social Jetlag Analyzer            │
            │  • Bio-Digital Twin & Neuro-Momentum Physics Engine         │
            └──────────────────────────────┬──────────────────────────────┘
                                           │
            ┌──────────────────────────────▼──────────────────────────────┐
            │                 TIER 3: DATA VALIDATION & DQR               │
            │  • Ingestion Schema Verifier (Date, Range & Type Guards)    │
            │  • Z-Score Anomaly Detector & Missing Value Interpolation   │
            │  • Evaluator Persona Generator (Active, Night Owl, Balanced)│
            └──────────────────────────────┬──────────────────────────────┘
                                           │
            ┌──────────────────────────────▼──────────────────────────────┐
            │                 TIER 4: PERSISTENCE & PRIVACY               │
            │  • In-Memory Ephemeral Data Storage                         │
            │  • SHA-256 Provenance Fingerprint & Cryptographic Shredding │
            │  • Standalone Executive HTML & CSV Report Exporter          │
            └─────────────────────────────────────────────────────────────┘
            ```
            """
        )

    # ---------------- SUBTAB 4: DATA QUALITY RULES (DQR) ----------------
    with viva_sub4:
        st.markdown("#### 🛡️ Data Quality Rules (DQR) Ingestion Matrix")
        dqr_data = {
            "Rule ID": ["DQR-01", "DQR-02", "DQR-03", "DQR-04", "DQR-05", "DQR-06"],
            "Column / Target": ["date", "sleep_hours", "steps", "water_glasses", "mood_score", "activity_minutes"],
            "Allowed Type": ["ISO Date (YYYY-MM-DD)", "Float", "Integer", "Integer", "Integer (Optional)", "Integer (Optional)"],
            "Permitted Bounds": ["Past or Today (No Future)", "[0.0, 24.0] hrs", "[0, 60,000] steps", "[0, 30] glasses", "[1, 5] rating", "[0, 1440] mins"],
            "Violation Action": ["Rejection / Error Flag", "Truncate or Flag Anomaly", "Flag High-Volume Outlier", "Reject Negative Values", "Default to None", "Default to None"],
        }
        st.table(dqr_data)
