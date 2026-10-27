"""
Interactive Coherent Breathwork & Vagal Tone HRV Sync Engine.
Renders directly via HTML5/CSS3 keyframe animations.
"""

from __future__ import annotations
import streamlit as st
import streamlit.components.v1 as components


def render_breathwork_widget(dark_mode: bool = False):
    """
    Renders an interactive animated breathwork trainer widget
    supporting Box Breathing, 4-7-8 Induction, and 5.5s Coherence.
    """
    st.subheader("🧘 Coherent Breathwork & Vagal Tone HRV Sync Trainer")
    st.caption("Interactive parasympathetic nervous system regulator. Synchronize your breathing to optimize heart rate variability.")

    c1, c2 = st.columns([1, 2])

    with c1:
        technique = st.selectbox(
            "Select Breathing Protocol:",
            options=[
                "Box Breathing (4-4-4-4 Focus & Clarity)",
                "4-7-8 Relaxation (Parasympathetic Deep Reset)",
                "Coherent 5.5s (Optimal HRV Synchronization)",
            ],
            index=0,
            key="breath_tech_select",
        )

        st.markdown(
            """
            <div style="background: rgba(14, 165, 233, 0.08); border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 6px; font-size: 0.85rem; margin-top: 10px;">
                <strong>💡 Clinical Research Basis:</strong> Controlled resonant breathing increases respiratory sinus arrhythmia (RSA), lowers baseline cortisol by up to 23%, and elevates vagal nerve stimulation for sustained cognitive endurance.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        if "Box Breathing" in technique:
            inhale_time, hold1_time, exhale_time, hold2_time = 4, 4, 4, 4
            anim_name = "box"
            total_duration = 16
        elif "4-7-8" in technique:
            inhale_time, hold1_time, exhale_time, hold2_time = 4, 7, 8, 0
            anim_name = "relax"
            total_duration = 19
        else:
            inhale_time, hold1_time, exhale_time, hold2_time = 5.5, 0, 5.5, 0
            anim_name = "coherent"
            total_duration = 11

        bg_card = "#0f172a" if dark_mode else "#ffffff"
        ring_color = "#00f2fe" if dark_mode else "#0284c7"
        text_color = "#f8fafc" if dark_mode else "#0f172a"
        sub_color = "#94a3b8" if dark_mode else "#64748b"

        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <style>
            body {{
                margin: 0;
                padding: 10px;
                background: transparent;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .breath-container {{
                background: {bg_card};
                border: 1px solid rgba(148, 163, 184, 0.25);
                border-radius: 12px;
                padding: 16px;
                width: 100%;
                max-width: 440px;
                text-align: center;
                box-shadow: 0 4px 16px rgba(0,0,0,0.12);
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .orb-wrapper {{
                position: relative;
                width: 170px;
                height: 170px;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 10px 0;
            }}
            .glow-ring {{
                position: absolute;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: radial-gradient(circle, {ring_color} 0%, rgba(16, 185, 129, 0.2) 65%, transparent 75%);
                filter: blur(8px);
                opacity: 0.6;
                animation: pulse-{anim_name} {total_duration}s ease-in-out infinite;
            }}
            .breathing-orb {{
                width: 90px;
                height: 90px;
                border-radius: 50%;
                background: linear-gradient(135deg, {ring_color}, #10b981);
                border: 3px solid rgba(255,255,255,0.7);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: #ffffff;
                box-shadow: 0 0 25px rgba(2, 132, 199, 0.45);
                animation: breathe-{anim_name} {total_duration}s ease-in-out infinite;
                z-index: 2;
            }}
            .phase-text {{
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                text-shadow: 0 1px 3px rgba(0,0,0,0.4);
            }}
            .phase-sub {{
                font-size: 10px;
                opacity: 0.9;
                margin-top: 2px;
            }}
            .timer-readout {{
                font-size: 11px;
                color: {sub_color};
                margin-top: 6px;
                letter-spacing: 0.04em;
            }}
            
            /* Box Breathing Keyframes (4s Inhale, 4s Hold, 4s Exhale, 4s Hold) */
            @keyframes breathe-box {{
                0% {{ transform: scale(0.75); }}
                25% {{ transform: scale(1.35); }}
                50% {{ transform: scale(1.35); }}
                75% {{ transform: scale(0.75); }}
                100% {{ transform: scale(0.75); }}
            }}
            @keyframes pulse-box {{
                0% {{ transform: scale(0.8); opacity: 0.3; }}
                25% {{ transform: scale(1.6); opacity: 0.8; }}
                50% {{ transform: scale(1.6); opacity: 0.8; }}
                75% {{ transform: scale(0.8); opacity: 0.3; }}
                100% {{ transform: scale(0.8); opacity: 0.3; }}
            }}

            /* 4-7-8 Relaxation Keyframes (4s Inhale, 7s Hold, 8s Exhale) */
            @keyframes breathe-relax {{
                0% {{ transform: scale(0.75); }}
                21% {{ transform: scale(1.4); }}
                58% {{ transform: scale(1.4); }}
                100% {{ transform: scale(0.75); }}
            }}
            @keyframes pulse-relax {{
                0% {{ transform: scale(0.8); opacity: 0.3; }}
                21% {{ transform: scale(1.65); opacity: 0.9; }}
                58% {{ transform: scale(1.65); opacity: 0.9; }}
                100% {{ transform: scale(0.8); opacity: 0.3; }}
            }}

            /* Coherent 5.5s Keyframes */
            @keyframes breathe-coherent {{
                0% {{ transform: scale(0.8); }}
                50% {{ transform: scale(1.35); }}
                100% {{ transform: scale(0.8); }}
            }}
            @keyframes pulse-coherent {{
                0% {{ transform: scale(0.85); opacity: 0.4; }}
                50% {{ transform: scale(1.55); opacity: 0.85; }}
                100% {{ transform: scale(0.85); opacity: 0.4; }}
            }}
        </style>
        </head>
        <body>
            <div class="breath-container">
                <div style="font-size: 13px; font-weight: 700; color: {text_color}; margin-bottom: 4px;">
                    {technique.split('(')[0].strip()}
                </div>
                <div class="orb-wrapper">
                    <div class="glow-ring"></div>
                    <div class="breathing-orb">
                        <div class="phase-text" id="statusLabel">SYNCING</div>
                        <div class="phase-sub" id="secCounter">●</div>
                    </div>
                </div>
                <div class="timer-readout" id="cueText">
                    Inhale through nose &bull; Expand diaphragm &bull; Slow smooth exhale
                </div>
            </div>

            <script>
                // Dynamic label updates synchronized with animation cycle
                const total = {total_duration};
                const inh = {inhale_time};
                const h1 = {hold1_time};
                const exh = {exhale_time};
                const h2 = {hold2_time};

                function updateLabels() {{
                    const now = (Date.now() / 1000) % total;
                    const lbl = document.getElementById('statusLabel');
                    const cue = document.getElementById('cueText');

                    if (now < inh) {{
                        lbl.innerText = "INHALE";
                        cue.innerText = "Breathe in deeply through the nose (" + Math.ceil(inh - now) + "s)";
                    }} else if (now < inh + h1) {{
                        lbl.innerText = "HOLD";
                        cue.innerText = "Suspend breath gently at the crown (" + Math.ceil(inh + h1 - now) + "s)";
                    }} else if (now < inh + h1 + exh) {{
                        lbl.innerText = "EXHALE";
                        cue.innerText = "Slow gentle release through mouth (" + Math.ceil(inh + h1 + exh - now) + "s)";
                    }} else {{
                        lbl.innerText = "REST / HOLD";
                        cue.innerText = "Keep lungs empty and relaxed (" + Math.ceil(total - now) + "s)";
                    }}
                }}
                setInterval(updateLabels, 150);
                updateLabels();
            </script>
        </body>
        </html>
        """
        components.html(html_code, height=270)
