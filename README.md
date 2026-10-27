# SIC-project

# Personal Wellness Dashboard: Single-User Longitudinal Behavioral Analytics

An enterprise-grade, single-user **Personal Wellness Dashboard** engineered with Python, Streamlit, and Plotly. Developed for longitudinal biometric tracking, autonomic habit resilience, circadian chronotype evaluation, and 3D phase-space habit dynamics.

---

## 🌟 Key Features & Capabilities

- **Executive Cockpit & KPIs**:
  - Live biometric tracking: Sleep duration, Physical steps, Cellular hydration, Subjective mood, and Active exercise minutes.
  - **Composite Behavioral Consistency Index (BCI)**: Transparent, rule-based formula measuring consistency across 4 orthogonal pillars (Sleep 30%, Steps 30%, Water 20%, Logging 20%).
  - **Habit Streaks Tracker**: Active and longest consecutive daily streaks.
  - **Habit Vitality & Next-Day Readiness**: Dynamic readiness forecasting based on recent behavioral momentum.

- **Autonomic Habit Resiliency Engine**:
  - Mainframe-inspired high-availability metrics: Habit Availability / Uptime % and Mean Time to Recovery (MTTR).
  - Self-healing behavioral resilience categorization.

- **Interactive Visualizations & Longitudinal Trends**:
  - **7-Day Rolling Moving Averages (SMA)** for variance smoothing.
  - **GitHub-Style Contribution Heatmap**: Visualizing multi-target fulfillment across weeks and days.
  - **Circadian 24-Hour Polar Clock Dial & Social Jetlag Analyzer**: Measures behavioral sleep midpoint shifts between workdays and weekends.
  - **Bivariate Pearson Correlation Heatmap** & Rule-Based Trend Observations.
  - **IQR Statistical Outlier / Anomaly Detection**.

- **Bio-Digital Twin & 3D Phase Space**:
  - **Interactive 3D Habit Phase Orbit**: Trajectory spline visualizing sequential day-by-day evolution through state space alongside target attractor basin.
  - **Biological Vitality Age Delta**: Estimates biological age relative to chronological baseline.
  - **Neuro-Momentum Newtonian Kinematics**: Models habit momentum using mass (streak length) × velocity (target adherence).

- **What-If Routine Simulator**:
  - Interactive scenario modeling: Adjust sleep, steps, and water intake to view real-time projected Composite Score and Uptime % gains.

- **Mind-Body Vagal Tone Reset (Breathwork)**:
  - Interactive animated breathing ring: Box Breathing (4-4-4-4), 4-7-8 Relaxation, and Coherent 5.5s Resonant breathing.

- **Z-Cognitive Habit Assistant**:
  - 100% offline, deterministic natural language query engine. Zero external cloud API calls, zero telemetry, full privacy.

- **Gamified Milestone Badges**:
  - Six unlockable achievement badges celebrating habit discipline.

- **Pervasive Privacy & Ephemeral Data Vault**:
  - Cryptographic SHA-256 session provenance fingerprinting.
  - Zero PII retained, ephemeral in-memory processing.

- **Executive Dossier & Academic Defense Room**:
  - Standalone HTML printable executive summary export (save to PDF with Ctrl+P).
  - Complete Academic Defense Tab with LaTeX mathematical formulations, architecture diagrams, and Viva Voce model Q&As.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.9+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Dashboard
Simply double-click:
```bash
run_dashboard.bat
```
Or run directly from the terminal:
```bash
python -m streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 📁 Project Structure

```
projectD/
├── app.py                     # Main interactive Streamlit application
├── data_loader.py             # CSV ingestion, parsing & template utilities
├── metrics.py                 # Core statistical engine, BCI index & streaks
├── validation.py              # Data schema rules & IQR anomaly detector
├── insights.py                # Rule-based longitudinal trend comparisons
├── resilience.py              # Autonomic habit availability & MTTR engine
├── chronotype.py              # Circadian chronotype & social jetlag analyzer
├── clock_visualizer.py        # 24-hour polar circadian clock visualizer
├── calendar_heatmap.py        # GitHub-style activity contribution calendar
├── bio_twin.py                # 3D habit phase orbit & neuro-momentum engine
├── simulation.py              # What-If routine scenario simulator
├── vitality.py                # Habit vitality & next-day readiness forecast
├── badges.py                  # Gamified achievement badges evaluator
├── breathwork.py              # Interactive CSS3 animated breathwork widget
├── soundscapes.py             # Web Audio API ambient audio synthesizer
├── security.py                # Cryptographic SHA-256 privacy audit vault
├── personas.py                # Evaluator persona datasets generator
├── report_generator.py        # Executive HTML printable report compiler
├── assistant.py               # Deterministic local NLP query assistant
├── viva_defense.py            # Academic defense suite & Viva Voce Q&As
├── theme.py                   # Carbon & Cyberpunk multi-theme injector
├── sample_wellness_data.csv   # Benchmark synthetic longitudinal dataset
├── requirements.txt           # Python dependency specification
├── run_dashboard.bat          # One-click Windows application launcher
└── src/                       # Package namespace forwarding modules
```

---

## 🔒 Privacy & Non-Medical Disclaimer

- **Privacy Guarantee**: All processing occurs strictly within ephemeral local memory on the user's workstation. No analytics, tracking beacons, or telemetry data are collected or transmitted.
- **Educational Notice**: This project is developed exclusively for educational purposes as part of academic coursework. It is not a clinical medical diagnostic tool and does not provide medical advice.
