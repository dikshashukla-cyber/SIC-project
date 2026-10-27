"""Synthesized Ambient Focus Soundscapes widget (Zero-dependency Web Audio API)."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components


def render_focus_soundscapes_widget():
    """
    Renders an in-browser synthesized ambient sound generator using the HTML5 Web Audio API.
    Zero external audio files or downloads needed—audio is generated via pure mathematical oscillators and white noise buffers!
    """
    soundscape_html = """
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px; margin-top: 10px;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.9rem; color: #0f172a;">🎧 Ambient Focus Soundscapes</div>
            <div id="audio-status" style="font-size: 0.78rem; font-weight: 600; color: #64748b;">Idle (Off)</div>
        </div>
        <div style="font-size: 0.8rem; color: #64748b; margin-bottom: 10px;">
            In-browser acoustic synthesis for calm review & concentration.
        </div>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <button onclick="playRain()" style="background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; border-radius: 6px; padding: 6px 10px; font-size: 0.8rem; cursor: pointer; font-weight: 600;">🌧️ Rain</button>
            <button onclick="playOcean()" style="background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; border-radius: 6px; padding: 6px 10px; font-size: 0.8rem; cursor: pointer; font-weight: 600;">🌊 Waves</button>
            <button onclick="playTone()" style="background: #f5f3ff; color: #6d28d9; border: 1px solid #ddd6fe; border-radius: 6px; padding: 6px 10px; font-size: 0.8rem; cursor: pointer; font-weight: 600;">🧠 432Hz Alpha</button>
            <button onclick="stopAudio()" style="background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px 10px; font-size: 0.8rem; cursor: pointer; font-weight: 600;">⏹️ Mute</button>
        </div>
    </div>

    <script>
    let audioCtx = null;
    let activeNodes = [];

    function initAudio() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
    }

    function stopAudio() {
        if (activeNodes.length > 0) {
            activeNodes.forEach(n => {
                try { n.stop ? n.stop() : n.disconnect(); } catch(e){}
            });
            activeNodes = [];
        }
        document.getElementById('audio-status').innerText = 'Idle (Off)';
        document.getElementById('audio-status').style.color = '#64748b';
    }

    function playRain() {
        initAudio();
        stopAudio();
        document.getElementById('audio-status').innerText = 'Playing: Rain';
        document.getElementById('audio-status').style.color = '#0284c7';

        const bufferSize = audioCtx.sampleRate * 2;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        let lastOut = 0.0;
        for (let i = 0; i < bufferSize; i++) {
            let white = Math.random() * 2 - 1;
            data[i] = (lastOut + (0.02 * white)) / 1.02;
            lastOut = data[i];
            data[i] *= 3.5;
        }

        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        noise.loop = true;

        const filter = audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(800, audioCtx.currentTime);

        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(audioCtx.destination);

        noise.start();
        activeNodes.push(noise, filter, gain);
    }

    function playOcean() {
        initAudio();
        stopAudio();
        document.getElementById('audio-status').innerText = 'Playing: Waves';
        document.getElementById('audio-status').style.color = '#059669';

        const bufferSize = audioCtx.sampleRate * 2;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }

        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        noise.loop = true;

        const filter = audioCtx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(400, audioCtx.currentTime);
        filter.Q.setValueAtTime(1.5, audioCtx.currentTime);

        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.05, audioCtx.currentTime);

        // Modulate filter for wave surge
        const osc = audioCtx.createOscillator();
        osc.frequency.setValueAtTime(0.12, audioCtx.currentTime);
        const oscGain = audioCtx.createGain();
        oscGain.gain.setValueAtTime(250, audioCtx.currentTime);
        osc.connect(oscGain);
        oscGain.connect(filter.frequency);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        noise.start();
        activeNodes.push(osc, noise, filter, gain);
    }

    function playTone() {
        initAudio();
        stopAudio();
        document.getElementById('audio-status').innerText = 'Playing: 432Hz Alpha';
        document.getElementById('audio-status').style.color = '#7c3aed';

        const osc = audioCtx.createOscillator();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(432, audioCtx.currentTime);

        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.04, audioCtx.currentTime);

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        activeNodes.push(osc, gain);
    }
    </script>
    """
    components.html(soundscape_html, height=135)
