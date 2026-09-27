from __future__ import annotations

import html
import queue
import textwrap
import time

import streamlit as st

from debate_arena.config.settings import ASSEMBLYAI_API_KEY
from debate_arena.debate.debate_report import DebateReport
from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState
try:
    from debate_arena.voice.voice_agent import VoiceAgent
    LOCAL_VOICE_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    VoiceAgent = None
    LOCAL_VOICE_AVAILABLE = False

from debate_arena.voice.cloud_voice_agent import (
    CloudVoiceAgent,
)
from debate_arena.frontend.coaching_view import (
    build_coaching_view_data,
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Debate Arena",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# DEBATE CONFIGURATION
# ============================================================

TOPIC = "Should social media be banned for students?"

USER_POSITION = "NOT BANNED"

AI_POSITION = "SHOULD BAN"

MAX_ROUNDS = 3


# ============================================================
# HTML HELPER
# ============================================================

def render_html(content: str) -> None:
    st.html(
        textwrap.dedent(content)
    )


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 15% 0%,
                rgba(99, 102, 241, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(168, 85, 247, 0.06),
                transparent 30%
            ),
            #070912;

        color: #e8ebf4;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }

    h1,
    h2,
    h3 {
        color: #f3f4f8 !important;
    }

    p {
        color: #8992a6;
    }

    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.6rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .brand-icon {
        font-size: 1.55rem;
        filter:
            drop-shadow(
                0 0 12px rgba(139, 92, 246, 0.55)
            );
    }

    .brand-name {
        color: #f4f5fa;
        font-size: 1.55rem;
        line-height: 1;
        font-weight: 850;
        letter-spacing: -0.045em;
        text-shadow:
            0 0 24px rgba(139, 92, 246, 0.16);
    }

    .brand-subtitle {
        color: #7f899d;
        font-size: 0.54rem;
        margin-top: 0.28rem;
        letter-spacing: 0.075em;
        text-transform: uppercase;
    }

    .live-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.24rem 0.55rem;
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 999px;
        color: #45e7a1;
        background: rgba(16, 185, 129, 0.055);
        font-family: monospace;
        font-size: 0.52rem;
        letter-spacing: 0.08em;
    }

    .live-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #35e99a;
        box-shadow: 0 0 8px rgba(53, 233, 154, 0.8);
    }

    .topic-card {
        position: relative;
        overflow: hidden;

        padding: 1.45rem 1.8rem 1.6rem;

        border: 1px solid rgba(139, 92, 246, 0.24);
        border-radius: 18px;

        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(124, 58, 237, 0.16),
                transparent 48%
            ),
            linear-gradient(
                145deg,
                rgba(20, 24, 39, 0.92),
                rgba(8, 11, 21, 0.96)
            );

        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.035);

        text-align: center;
    }

    .topic-card::before {
        content: "";

        position: absolute;
        top: -80px;
        left: 50%;
        transform: translateX(-50%);

        width: 260px;
        height: 140px;

        background: rgba(124, 58, 237, 0.12);

        filter: blur(55px);
        pointer-events: none;
    }

    .topic-card::after {
        content: "";

        position: absolute;
        left: 12%;
        right: 12%;
        bottom: 0;

        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(139, 92, 246, 0.65),
                rgba(192, 92, 255, 0.65),
                transparent
            );

        opacity: 0.8;
    }

    .topic-label {
        color: #667086;
        font-family: monospace;
        font-size: 0.46rem;
        font-weight: 650;
        letter-spacing: 0.17em;
        text-transform: uppercase;
        margin-bottom: 0.42rem;
    }

    .topic-title {
        color: #edf0f7;
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.035em;
    }

    .position-card {
        position: relative;
        overflow: hidden;

        padding: 1.05rem 1.15rem;

        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 14px;

        background:
            linear-gradient(
                145deg,
                rgba(17, 22, 34, 0.88),
                rgba(9, 12, 21, 0.94)
            );

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.025);

        transition:
            transform 180ms ease,
            border-color 180ms ease,
            box-shadow 180ms ease;
    }

    .position-card:hover {
        transform: translateY(-2px);

        border-color: rgba(139, 92, 246, 0.28);

        box-shadow:
            0 16px 40px rgba(0, 0, 0, 0.28),
            0 0 30px rgba(99, 102, 241, 0.06);
    }

    .position-label {
        color: #687289;
        font-family: monospace;
        font-size: 0.46rem;
        letter-spacing: 0.12em;
        margin-bottom: 0.28rem;
    }

    .position-user {
        color: #8fc8ff;
        font-family: monospace;
        font-size: 0.65rem;
        font-weight: 750;
    }

    .position-ai {
        color: #d7a9ff;
        font-family: monospace;
        font-size: 0.65rem;
        font-weight: 750;
    }

    .round-section {
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    .round-label {
        color: #687289;
        font-family: monospace;
        font-size: 0.45rem;
        letter-spacing: 0.16em;
        margin-bottom: 0.28rem;
    }

    .round-number {
        color: #eef0f7;
        font-family: monospace;
        font-size: 0.7rem;
        font-weight: 750;
    }

    .round-progress {
        width: 112px;
        height: 2px;
        margin: 0.55rem auto 0;
        background:
            linear-gradient(
                90deg,
                #6366f1,
                #c05cff
            );
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
    }

    .status-card {
        position: relative;
        overflow: hidden;

        padding: 1.35rem 1rem;

        border: 1px solid rgba(99, 102, 241, 0.24);
        border-radius: 15px;

        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(99, 102, 241, 0.12),
                transparent 55%
            ),
            linear-gradient(
                145deg,
                rgba(17, 21, 39, 0.94),
                rgba(8, 11, 22, 0.97)
            );

        box-shadow:
            0 18px 45px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.035);

        text-align: center;

        margin-bottom: 1.25rem;
    }

    .status-card::before {
        content: "";

        position: absolute;

        top: 0;
        left: 20%;
        right: 20%;

        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(139, 92, 246, 0.75),
                transparent
            );
    }

    .status-icon {
        font-size: 1.1rem;
        margin-bottom: 0.35rem;
    }

    .status-title {
        color: #e9ebf4;
        font-size: 0.72rem;
        font-weight: 750;
    }

    .status-subtitle {
        color: #727b90;
        font-size: 0.47rem;
        margin-top: 0.22rem;
    }

    .voice-state-panel {
        position: relative;
        overflow: hidden;
        margin: 0.75rem 0 1rem;
        padding: 1.1rem 1.2rem;
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 16px;
        background: linear-gradient(
            145deg,
            rgba(15, 20, 34, 0.94),
            rgba(8, 11, 21, 0.98)
        );
        box-shadow:
            0 18px 45px rgba(0, 0, 0, 0.24),
            inset 0 1px 0 rgba(255,255,255,0.035);
        text-align: center;
    }

    .voice-state-panel::before {
        content: "";
        position: absolute;
        top: 0;
        left: 18%;
        right: 18%;
        height: 1px;
        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(139,92,246,0.75),
                transparent
            );
    }

    .voice-state-orb {
        width: 34px;
        height: 34px;
        margin: 0 auto 0.55rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        background: rgba(99,102,241,0.10);
        border: 1px solid rgba(99,102,241,0.28);
        box-shadow: 0 0 22px rgba(99,102,241,0.18);
    }

    .voice-state-panel.user {
        border-color: rgba(77,168,255,0.30);
    }

    .voice-state-panel.user .voice-state-orb {
        background: rgba(77,168,255,0.10);
        border-color: rgba(77,168,255,0.45);
        box-shadow: 0 0 24px rgba(77,168,255,0.25);
        animation: voicePulse 1.35s ease-in-out infinite;
    }

    .voice-state-panel.ai {
        border-color: rgba(192,92,255,0.30);
    }

    .voice-state-panel.ai .voice-state-orb {
        background: rgba(192,92,255,0.10);
        border-color: rgba(192,92,255,0.45);
        box-shadow: 0 0 24px rgba(192,92,255,0.25);
        animation: voicePulse 1.15s ease-in-out infinite;
    }

    .voice-state-panel.thinking .voice-state-orb {
        animation: voicePulse 1.5s ease-in-out infinite;
    }

    .voice-state-panel.complete {
        border-color: rgba(74,222,128,0.28);
    }

    .voice-state-panel.complete .voice-state-orb {
        background: rgba(34,197,94,0.10);
        border-color: rgba(74,222,128,0.40);
    }

    .voice-state-panel.error {
        border-color: rgba(248,113,113,0.30);
    }

    .voice-state-title {
        color: #f1f3f8;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.01em;
    }

    .voice-state-subtitle {
        color: #818ba0;
        font-size: 0.52rem;
        margin-top: 0.28rem;
    }

    .voice-state-kicker {
        color: #657086;
        font-family: monospace;
        font-size: 0.40rem;
        letter-spacing: 0.14em;
        margin-bottom: 0.35rem;
    }

    @keyframes voicePulse {
        0%, 100% {
            transform: scale(1);
            opacity: 0.82;
        }

        50% {
            transform: scale(1.08);
            opacity: 1;
        }
    }

    .arena-section-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
        margin-top: 1.35rem;
        margin-bottom: 0.65rem;
        color: #e7eaf2;
        font-family: monospace;
        font-size: 0.5rem;
        font-weight: 800;
        letter-spacing: 0.11em;
    }

    .arena-live-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.22rem 0.45rem;
        border: 1px solid rgba(74, 222, 128, 0.2);
        border-radius: 999px;
        color: #86efac;
        background: rgba(34, 197, 94, 0.06);
        font-size: 0.36rem;
        letter-spacing: 0.08em;
    }

    .section-label {
        color: #7a8498;
        font-family: monospace;
        font-size: 0.47rem;
        font-weight: 650;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }

    .argument-card {
        position: relative;
        overflow: hidden;
        padding: 0.95rem 1rem 1rem;
        border-radius: 14px;
        margin-bottom: 0.7rem;
        background: rgba(13, 18, 30, 0.82);
        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.16),
            inset 0 1px 0 rgba(255, 255, 255, 0.025);
    }

    .argument-user {
        margin-right: 8%;
        border: 1px solid rgba(77, 168, 255, 0.24);
        border-left: 3px solid #4da8ff;
        background:
            linear-gradient(
                145deg,
                rgba(14, 27, 48, 0.92),
                rgba(10, 17, 30, 0.88)
            );
    }

    .argument-ai {
        margin-left: 8%;
        border: 1px solid rgba(192, 92, 255, 0.24);
        border-left: 3px solid #c05cff;
        background:
            linear-gradient(
                145deg,
                rgba(31, 17, 43, 0.92),
                rgba(17, 12, 28, 0.88)
            );
    }

    .argument-user::after,
    .argument-ai::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        opacity: 0.55;
    }

    .argument-user::after {
        background: linear-gradient(90deg, #4da8ff, transparent 55%);
    }

    .argument-ai::after {
        background: linear-gradient(90deg, #c05cff, transparent 55%);
    }

    .argument-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.7rem;
        color: #7f899d;
        font-family: monospace;
        font-size: 0.42rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-bottom: 0.55rem;
    }

    .speaker-line {
        display: flex;
        align-items: center;
        gap: 0.38rem;
        min-width: 0;
    }

    .speaker-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        flex: 0 0 auto;
    }

    .user-dot {
        background: #4da8ff;
        box-shadow: 0 0 10px rgba(77, 168, 255, 0.75);
    }

    .ai-dot {
        background: #c05cff;
        box-shadow: 0 0 10px rgba(192, 92, 255, 0.75);
    }

    .speaker-name {
        color: #edf1f8;
        font-weight: 800;
        letter-spacing: 0.1em;
    }

    .speaker-role {
        color: #707b90;
        font-size: 0.37rem;
        letter-spacing: 0.09em;
    }

    .round-chip {
        flex: 0 0 auto;
        padding: 0.22rem 0.42rem;
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 999px;
        color: #7f899d;
        background: rgba(255, 255, 255, 0.025);
        font-size: 0.36rem;
        letter-spacing: 0.08em;
    }

    .argument-text {
        color: #e1e5ef;
        font-size: 0.72rem;
        line-height: 1.65;
        letter-spacing: 0.005em;
    }

    .strategy-card {
        padding: 0.8rem 0.9rem;
        border: 1px solid rgba(245, 158, 11, 0.22);
        border-radius: 9px;
        background: rgba(30, 22, 10, 0.72);
        margin-top: 0.7rem;
    }

    .strategy-label {
        color: #c99a34;
        font-family: monospace;
        font-size: 0.42rem;
        letter-spacing: 0.09em;
    }

    .strategy-value {
        color: #f2c45d;
        font-family: monospace;
        font-size: 0.57rem;
        font-weight: 750;
        margin-top: 0.25rem;
    }

    .report-summary {
        padding: 0.85rem 1rem;
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 10px;
        background: rgba(13, 17, 26, 0.72);
        margin-bottom: 0.85rem;
    }

    .report-label {
        color: #707b90;
        font-family: monospace;
        font-size: 0.42rem;
        letter-spacing: 0.09em;
        margin-bottom: 0.3rem;
    }

    .report-text {
        color: #dfe3ed;
        font-size: 0.68rem;
        line-height: 1.65;
        letter-spacing: 0.005em;
    }

    .report-card {
        padding: 0.8rem 0.9rem;
        border: 1px solid rgba(148, 163, 184, 0.13);
        border-radius: 9px;
        background: rgba(13, 17, 27, 0.72);
        min-height: 100px;
    }

    .report-card-title {
        color: #e9ebf3;
        font-size: 0.62rem;
        font-weight: 750;
        margin-bottom: 0.35rem;
    }

    .report-card-text {
        color: #aab2c2;
        font-size: 0.62rem;
        line-height: 1.6;
    }

    .report-list {
        color: #aab2c2;
        font-size: 0.61rem;
        line-height: 1.65;
        padding-left: 1.05rem;
    }

    .stButton > button {
        width: 100%;
        min-height: 38px;
        border: 1px solid rgba(139, 92, 246, 0.28) !important;
        border-radius: 9px !important;
        background:
            linear-gradient(
                135deg,
                rgba(99, 102, 241, 0.13),
                rgba(168, 85, 247, 0.08)
            ) !important;
        color: #e6e8f0 !important;
        font-family: monospace !important;
        font-size: 0.57rem !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover {
        border-color: #a970ff !important;
        background:
            linear-gradient(
                135deg,
                rgba(99, 102, 241, 0.23),
                rgba(168, 85, 247, 0.15)
            ) !important;
    }

    [data-testid="stMetric"] {
        background: rgba(13, 17, 27, 0.55);
        border: 1px solid rgba(148, 163, 184, 0.08);
        border-radius: 9px;
        padding: 0.65rem;
    }

    [data-testid="stMetricLabel"] {
        color: #697389 !important;
        font-family: monospace !important;
        font-size: 0.45rem !important;
    }

    [data-testid="stMetricValue"] {
        color: #e9ecf4 !important;
        font-family: monospace !important;
        font-size: 0.85rem !important;
    }

    .setup-card {
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding: 1.15rem 1.35rem;
        border: 1px solid rgba(139, 92, 246, 0.18);
        border-radius: 14px;
        background: rgba(10, 13, 24, 0.72);
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.20);
    }

    .setup-label {
        color: #7f8aa2;
        font-family: monospace;
        font-size: 0.48rem;
        font-weight: 800;
        letter-spacing: 0.13em;
        margin-bottom: 0.28rem;
    }

    .setup-title {
        color: #f2f4fa;
        font-size: 1.05rem;
        font-weight: 760;
        margin-bottom: 0.2rem;
    }

    .setup-subtitle {
        color: #78839a;
        font-size: 0.62rem;
        line-height: 1.55;
    }

    .setup-ai-note {
        margin-top: 0.65rem;
        padding: 0.65rem 0.8rem;
        border-radius: 9px;
        background: rgba(192, 92, 255, 0.06);
        border: 1px solid rgba(192, 92, 255, 0.14);
        color: #b7a9c8;
        font-family: monospace;
        font-size: 0.5rem;
    }

    /* ========================================================
       M10.4.1 — PERSONALIZED COACHING PROFILE
       ======================================================== */

    .coaching-profile-hero {
        position: relative;
        overflow: hidden;
        padding: 1.35rem 1.45rem 1.4rem;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(139, 92, 246, 0.24);
        border-radius: 14px;
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(192, 92, 255, 0.13),
                transparent 42%
            ),
            radial-gradient(
                circle at 10% 100%,
                rgba(99, 102, 241, 0.09),
                transparent 42%
            ),
            linear-gradient(
                145deg,
                rgba(18, 22, 38, 0.96),
                rgba(9, 12, 22, 0.97)
            );
        box-shadow:
            0 18px 45px rgba(0, 0, 0, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.035);
    }

    .coaching-profile-hero::after {
        content: "";
        position: absolute;
        left: 12%;
        right: 12%;
        bottom: 0;
        height: 1px;
        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(139, 92, 246, 0.72),
                rgba(192, 92, 255, 0.62),
                transparent
            );
    }

    .coaching-kicker {
        color: #a78bfa;
        font-family: monospace;
        font-size: 0.42rem;
        font-weight: 750;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.42rem;
    }

    .coaching-profile-title {
        color: #f1f3f8;
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: -0.025em;
    }

    .coaching-profile-summary {
        max-width: 820px;
        color: #9ea7ba;
        font-size: 0.62rem;
        line-height: 1.65;
        margin-top: 0.42rem;
    }

    .coaching-profile-card {
        padding: 0.9rem 1rem;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 10px;
        background: rgba(13, 17, 27, 0.72);
        min-height: 132px;
    }

    .coaching-profile-card.strengths {
        border-color: rgba(77, 168, 255, 0.16);
        background:
            linear-gradient(
                145deg,
                rgba(14, 27, 48, 0.72),
                rgba(10, 17, 30, 0.76)
            );
    }

    .coaching-profile-card.focus {
        border-color: rgba(192, 92, 255, 0.16);
        background:
            linear-gradient(
                145deg,
                rgba(31, 17, 43, 0.72),
                rgba(17, 12, 28, 0.76)
            );
    }

    .coaching-profile-card-title {
        color: #e9ecf4;
        font-size: 0.62rem;
        font-weight: 800;
        margin-bottom: 0.18rem;
    }

    .coaching-profile-card-subtitle {
        color: #697389;
        font-family: monospace;
        font-size: 0.38rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.48rem;
    }

    .coaching-profile-list {
        color: #aab2c2;
        font-size: 0.58rem;
        line-height: 1.58;
        padding-left: 1rem;
        margin: 0;
    }

    .coaching-focus-card {
        margin-top: 0.8rem;
        padding: 0.85rem 1rem;
        border: 1px solid rgba(245, 158, 11, 0.18);
        border-radius: 10px;
        background: rgba(30, 22, 10, 0.55);
    }

    .coaching-focus-title {
        color: #f2c45d;
        font-family: monospace;
        font-size: 0.44rem;
        font-weight: 750;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.55rem;
    }

    .coaching-priority {
        display: flex;
        gap: 0.7rem;
        align-items: flex-start;
        padding: 0.72rem 0;
        border-top: 1px solid rgba(148, 163, 184, 0.08);
    }

    .coaching-priority:first-child {
        border-top: 0;
        padding-top: 0;
    }

    .coaching-priority-number {
        flex: 0 0 auto;
        color: #a78bfa;
        font-family: monospace;
        font-size: 0.5rem;
        font-weight: 800;
        padding-top: 0.05rem;
    }

    .coaching-priority-name {
        color: #e9ecf4;
        font-size: 0.59rem;
        font-weight: 750;
    }

    .coaching-priority-reason {
        color: #8f98ab;
        font-size: 0.53rem;
        line-height: 1.5;
        margin-top: 0.16rem;
    }

    .coaching-moments-card {
        margin-top: 0.8rem;
        padding: 0.9rem 1rem;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 10px;
        background: rgba(13, 17, 27, 0.72);
    }

    .coaching-moment-title {
        color: #e9ecf4;
        font-size: 0.58rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }

    .coaching-moment {
        color: #9ea7ba;
        font-size: 0.55rem;
        line-height: 1.55;
        padding: 0.38rem 0;
        border-top: 1px solid rgba(148, 163, 184, 0.07);
    }

    .footer {
        color: #424b5d;
        font-family: monospace;
        font-size: 0.43rem;
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(148, 163, 184, 0.08);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ENGINE FACTORY
# ============================================================

def create_debate_engine(
    topic: str = TOPIC,
    user_position: str = USER_POSITION,
    ai_position: str = AI_POSITION,
) -> DebateEngine:
    state = DebateState(
        topic=topic.strip(),
        user_position=user_position.strip(),
        ai_position=ai_position.strip(),
        current_round=1,
        current_turn="user",
        max_rounds=MAX_ROUNDS,
    )

    return DebateEngine(
        state=state,
    )


# ============================================================
# SESSION STATE
# ============================================================

if "debate_engine" not in st.session_state:
    st.session_state.debate_engine = (
        create_debate_engine()
    )

if "voice_agent" not in st.session_state:
    st.session_state.voice_agent = None

if "voice_events" not in st.session_state:
    st.session_state.voice_events = queue.Queue()

if "voice_started" not in st.session_state:
    st.session_state.voice_started = False

if "voice_status" not in st.session_state:
    st.session_state.voice_status = "Ready"

if "voice_error" not in st.session_state:
    st.session_state.voice_error = ""

if "latest_user_transcript" not in st.session_state:
    st.session_state.latest_user_transcript = ""

if "latest_ai_transcript" not in st.session_state:
    st.session_state.latest_ai_transcript = ""

if "latest_ai_speech" not in st.session_state:
    st.session_state.latest_ai_speech = ""

if "voice_visual_state" not in st.session_state:
    st.session_state.voice_visual_state = "ready"

if "report" not in st.session_state:
    st.session_state.report = None

if "report_generation_in_progress" not in st.session_state:
    st.session_state.report_generation_in_progress = False

if "setup_topic" not in st.session_state:
    st.session_state.setup_topic = TOPIC

if "setup_position" not in st.session_state:
    st.session_state.setup_position = "OPPOSE"


engine: DebateEngine = (
    st.session_state.debate_engine
)


# ============================================================
# THREAD-SAFE VOICE EVENT BRIDGE
# ============================================================

def create_voice_agent() -> VoiceAgent:
    """
    Create the VoiceAgent and bind it to a LOCAL Queue.

    The VoiceAgent runs in a background thread.

    Therefore the callback functions MUST NOT access
    st.session_state.

    The queue itself is captured here before the thread starts.
    """

    event_queue = st.session_state.voice_events

    def push_event(
        event_type: str,
        payload: str,
    ) -> None:
        event_queue.put(
            {
                "type": event_type,
                "payload": payload,
                "timestamp": time.time(),
            }
        )

    def on_status(status: str) -> None:
        push_event(
            "status",
            status,
        )

    def on_user_transcript(text: str) -> None:
        push_event(
            "user_transcript",
            text,
        )
        push_event(
            "voice_visual_state",
            "user_speaking",
        )

    def on_ai_transcript(text: str) -> None:
        push_event(
            "ai_transcript",
            text,
        )

    def on_ai_speaking(text: str) -> None:
        # A new AI rebuttal marks the end of the current user turn.
        # Clear the live user transcript so it cannot bleed into the next turn.
        push_event(
            "user_transcript_clear",
            "",
        )
        push_event(
            "ai_speaking",
            text,
        )
        push_event(
            "voice_visual_state",
            "ai_speaking",
        )

    def on_error(error: str) -> None:
        push_event(
            "error",
            error,
        )

    return VoiceAgent(
        engine=engine,
        api_key=ASSEMBLYAI_API_KEY,
        on_user_transcript=on_user_transcript,
        on_ai_transcript=on_ai_transcript,
        on_ai_speaking=on_ai_speaking,
        on_status=on_status,
        on_error=on_error,
    )


# ============================================================
# DRAIN VOICE EVENTS
# ============================================================

def drain_voice_events() -> None:
    """
    This function runs in Streamlit's normal execution context.

    It transfers events from the thread-safe Queue into
    Streamlit session state.
    """

    event_queue = st.session_state.voice_events

    while True:
        try:
            event = event_queue.get_nowait()

        except queue.Empty:
            break

        event_type = event.get("type")

        payload = event.get(
            "payload",
            "",
        )

        if event_type == "status":
            status_text = str(payload)
            st.session_state.voice_status = status_text
            normalized = status_text.lower()

            if (
                "complete" in normalized
                or "finished" in normalized
            ):
                st.session_state.latest_user_transcript = ""
                st.session_state.voice_visual_state = (
                    "complete"
                )

            elif (
                "error" in normalized
                or "failed" in normalized
            ):
                st.session_state.voice_visual_state = (
                    "error"
                )

            elif (
                "listening" in normalized
                or "ready" in normalized
            ):
                st.session_state.voice_visual_state = (
                    "listening"
                    if st.session_state.voice_started
                    else "ready"
                )

            elif (
                "starting" in normalized
                or "connecting" in normalized
            ):
                st.session_state.voice_visual_state = (
                    "connecting"
                )

            elif (
                "reason" in normalized
                or "analy" in normalized
                or "thinking" in normalized
            ):
                st.session_state.voice_visual_state = (
                    "thinking"
                )

        elif event_type == "user_transcript":
            text = str(payload).strip()

            if text:
                # AssemblyAI sends progressively updated transcript text.
                # Each update is the latest version of the current utterance,
                # NOT a new sentence to append. Replacing it prevents the
                # same words from appearing repeatedly in LIVE USER SPEECH.
                st.session_state.latest_user_transcript = text

            st.session_state.voice_visual_state = (
                "user_speaking"
            )

        elif event_type == "user_transcript_clear":
            st.session_state.latest_user_transcript = ""

        elif event_type == "ai_transcript":
            text = str(payload).strip()

            # A completed AI transcript marks the end of the current
            # user turn. The live user speech card should represent
            # only the current argument, not every argument from the
            # entire debate.
            st.session_state.latest_user_transcript = ""

            if text:
                st.session_state.latest_ai_transcript = (
                    text
                )

        elif event_type == "ai_speaking":
            st.session_state.latest_ai_speech = (
                str(payload).strip()
            )
            st.session_state.voice_visual_state = (
                "ai_speaking"
            )

        elif event_type == "voice_visual_state":
            st.session_state.voice_visual_state = (
                str(payload)
            )

        elif event_type == "error":
            st.session_state.voice_error = (
                str(payload)
            )

            st.session_state.voice_status = (
                "Voice error"
            )


# ============================================================
# HELPERS
# ============================================================

def escape_text(value: str) -> str:
    return html.escape(
        str(value)
    )


def completed_rounds() -> int:
    return min(
        len(engine.state.user_arguments),
        len(engine.state.ai_arguments),
    )


def display_round() -> int:
    completed = completed_rounds()

    if engine.state.is_finished():
        return max(
            1,
            min(
                completed,
                MAX_ROUNDS,
            ),
        )

    return max(
        1,
        min(
            engine.state.current_round,
            MAX_ROUNDS,
        ),
    )


def format_strategy(strategy) -> str:
    if strategy is None:
        return "WAITING FOR ANALYSIS"

    value = getattr(
        strategy,
        "value",
        str(strategy),
    )

    return value.replace(
        "_",
        " ",
    ).upper()


# ============================================================
# ARGUMENT CARD
# ============================================================

def render_argument(
    speaker: str,
    text: str,
    round_number: int,
) -> None:

    if speaker == "user":
        render_html(
            f"""
            <div class="argument-card argument-user">

                <div class="argument-header">
                    <div class="speaker-line">
                        <span class="speaker-dot user-dot"></span>
                        <span class="speaker-name">YOU</span>
                        <span class="speaker-role">ARGUMENT</span>
                    </div>

                    <span class="round-chip">
                        ROUND {round_number}
                    </span>
                </div>

                <div class="argument-text">
                    {escape_text(text)}
                </div>

            </div>
            """
        )

    else:
        render_html(
            f"""
            <div class="argument-card argument-ai">

                <div class="argument-header">
                    <div class="speaker-line">
                        <span class="speaker-dot ai-dot"></span>
                        <span class="speaker-name">AI</span>
                        <span class="speaker-role">REBUTTAL</span>
                    </div>

                    <span class="round-chip">
                        ROUND {round_number}
                    </span>
                </div>

                <div class="argument-text">
                    {escape_text(text)}
                </div>

            </div>
            """
        )


# ============================================================
# REPORT
# ============================================================

def render_report(
    report: DebateReport,
) -> None:

    render_html(
        """
        <div class="section-label">
            📊 YOUR DEBATE REPORT
        </div>
        """
    )

    render_html(
        f"""
        <div class="report-summary">

            <div class="report-label">
                OVERALL SUMMARY
            </div>

            <div class="report-text">
                {escape_text(report.summary)}
            </div>

        </div>
        """
    )

    strongest, weakest = st.columns(2)

    with strongest:
        render_html(
            f"""
            <div class="report-card">

                <div class="report-card-title">
                    💪 Strongest Argument
                </div>

                <div class="report-card-text">
                    {escape_text(report.strongest_argument)}
                </div>

            </div>
            """
        )

    with weakest:
        render_html(
            f"""
            <div class="report-card">

                <div class="report-card-title">
                    ⚠️ Weakest Argument
                </div>

                <div class="report-card-text">
                    {escape_text(report.weakest_argument)}
                </div>

            </div>
            """
        )

    st.markdown("")

    strengths, weaknesses = st.columns(2)

    with strengths:
        strength_items = "".join(
            f"<li>{escape_text(item)}</li>"
            for item in report.strengths
        )

        render_html(
            f"""
            <div class="report-card">

                <div class="report-card-title">
                    ✅ Strengths
                </div>

                <ul class="report-list">
                    {strength_items}
                </ul>

            </div>
            """
        )

    with weaknesses:
        weakness_items = "".join(
            f"<li>{escape_text(item)}</li>"
            for item in report.weaknesses
        )

        render_html(
            f"""
            <div class="report-card">

                <div class="report-card-title">
                    🎯 Areas to Improve
                </div>

                <ul class="report-list">
                    {weakness_items}
                </ul>

            </div>
            """
        )

    st.markdown("")

    render_html(
        f"""
        <div class="report-card">

            <div class="report-card-title">
                📚 Evidence Usage
            </div>

            <div class="report-card-text">
                {escape_text(report.evidence_usage)}
            </div>

        </div>
        """
    )

    st.markdown("")

    render_html(
        f"""
        <div class="report-card">

            <div class="report-card-title">
                🔄 Consistency
            </div>

            <div class="report-card-text">
                {escape_text(report.consistency)}
            </div>

        </div>
        """
    )

    st.markdown("")

    render_html(
        f"""
        <div class="report-card">

            <div class="report-card-title">
                🎯 Responsiveness
            </div>

            <div class="report-card-text">
                {escape_text(report.responsiveness)}
            </div>

        </div>
        """
    )

    recommendations = "".join(
        f"<li>{escape_text(item)}</li>"
        for item in report.recommendations
    )

    render_html(
        f"""
        <div class="report-card" style="margin-top: 0.8rem;">

            <div class="report-card-title">
                💡 Recommendations
            </div>

            <ul class="report-list">
                {recommendations}
            </ul>

        </div>
        """
    )

    coaching_report = report.coaching_session_report

    if coaching_report is None:
        return

    coaching_data = build_coaching_view_data(
        coaching_report
    )

    render_html(
        """
        <div class="section-label" style="margin-top: 1.8rem;">
            🧠 PERSONALIZED COACHING
        </div>
        """
    )

    if coaching_data["session_summary"]:
        render_html(
            f"""
            <div class="report-summary">

                <div class="report-label">
                    COACHING SESSION SUMMARY
                </div>

                <div class="report-text">
                    {
                        escape_text(
                            coaching_data["session_summary"]
                        )
                    }
                </div>

            </div>
            """
        )

    profile = coaching_data["profile"]

    render_html(
        f"""
        <div class="coaching-profile-hero">

            <div class="coaching-kicker">
                🧠 AI COACHING ASSESSMENT
            </div>

            <div class="coaching-profile-title">
                Your Debate Coaching Profile
            </div>

            <div class="coaching-profile-summary">
                {escape_text(profile["overall_coaching_summary"])}
            </div>

        </div>
        """
    )

    profile_left, profile_right = st.columns(2)

    with profile_left:
        strength_items = "".join(
            f"<li>{escape_text(item)}</li>"
            for item in profile["strengths"]
        )

        render_html(
            f"""
            <div class="coaching-profile-card strengths">

                <div class="coaching-profile-card-title">
                    💪 Your Strengths
                </div>

                <div class="coaching-profile-card-subtitle">
                    What you already do well
                </div>

                <ul class="coaching-profile-list">
                    {strength_items}
                </ul>

            </div>
            """
        )

    with profile_right:
        improvement_items = "".join(
            f"<li>{escape_text(item)}</li>"
            for item in profile["improvement_areas"]
        )

        render_html(
            f"""
            <div class="coaching-profile-card focus">

                <div class="coaching-profile-card-title">
                    🔧 Improvement Areas
                </div>

                <div class="coaching-profile-card-subtitle">
                    Where your next gains can come from
                </div>

                <ul class="coaching-profile-list">
                    {improvement_items}
                </ul>

            </div>
            """
        )

    if coaching_data["priorities"]:
        priority_blocks = ""

        for index, priority in enumerate(
            coaching_data["priorities"],
            start=1,
        ):
            priority_blocks += f"""
            <div class="coaching-priority">

                <div class="coaching-priority-number">
                    {index:02d}
                </div>

                <div>

                    <div class="coaching-priority-name">
                        {escape_text(priority["priority"])}
                    </div>

                    <div class="coaching-priority-reason">
                        {escape_text(priority["reason"])}
                    </div>

                </div>

            </div>
            """

        render_html(
            f"""
            <div class="coaching-focus-card">

                <div class="coaching-focus-title">
                    🎯 Personalized Improvement Priorities
                </div>

                {priority_blocks}

            </div>
            """
        )

    if coaching_data["priorities"]:
        render_html(
            """
            <div class="report-card"
                 style="margin-top: 0.8rem;">

                <div class="report-card-title">
                    ⚡ Your Coaching Plan
                </div>

            </div>
            """
        )

        for index, priority in enumerate(
            coaching_data["priorities"],
            start=1,
        ):
            evidence_items = "".join(
                f"<li>{escape_text(item)}</li>"
                for item in priority["supporting_evidence"]
            )

            render_html(
                f"""
                <div class="report-card"
                     style="margin-top: 0.5rem;">

                    <div class="report-card-title">
                        {index}. {
                            escape_text(
                                priority["priority"]
                            )
                        }
                    </div>

                    <div class="report-card-text">
                        <strong>Why:</strong>
                        {
                            escape_text(
                                priority["reason"]
                            )
                        }
                    </div>

                    <div class="report-card-text"
                         style="margin-top: 0.5rem;">

                        <strong>Focus:</strong>
                        {
                            escape_text(
                                priority["focus_area"]
                            )
                        }

                    </div>

                    <ul class="report-list">
                        {evidence_items}
                    </ul>

                </div>
                """
            )

    if coaching_data["recommendations"]:
        render_html(
            """
            <div class="report-card"
                 style="margin-top: 0.8rem;">

                <div class="report-card-title">
                    🚀 Actionable Coaching Recommendations
                </div>

            </div>
            """
        )

        for recommendation in coaching_data["recommendations"]:
            render_html(
                f"""
                <div class="report-card"
                     style="margin-top: 0.5rem;">

                    <div class="report-card-title">
                        💡 {
                            escape_text(
                                recommendation["recommendation"]
                            )
                        }
                    </div>

                    <div class="report-card-text">
                        <strong>Why:</strong>
                        {
                            escape_text(
                                recommendation["reason"]
                            )
                        }
                    </div>

                    <div class="report-card-text"
                         style="margin-top: 0.5rem;">

                        <strong>Action:</strong>
                        {
                            escape_text(
                                recommendation["action"]
                            )
                        }

                    </div>

                    <div class="report-card-text"
                         style="margin-top: 0.5rem;">

                        <strong>Related priority:</strong>
                        {
                            escape_text(
                                recommendation["related_priority"]
                            )
                        }

                    </div>

                </div>
                """
            )

    if coaching_data["practice_exercises"]:
        render_html(
            """
            <div class="report-card"
                 style="margin-top: 0.8rem;">

                <div class="report-card-title">
                    🏋️ Practice Exercises
                </div>

            </div>
            """
        )

        for exercise in coaching_data["practice_exercises"]:
            render_html(
                f"""
                <div class="report-card"
                     style="margin-top: 0.5rem;">

                    <div class="report-card-title">
                        🏋️ {
                            escape_text(
                                exercise["exercise"]
                            )
                        }
                    </div>

                    <div class="report-card-text">
                        <strong>Objective:</strong>
                        {
                            escape_text(
                                exercise["objective"]
                            )
                        }
                    </div>

                    <div class="report-card-text"
                         style="margin-top: 0.5rem;">

                        <strong>Instructions:</strong>
                        {
                            escape_text(
                                exercise["instructions"]
                            )
                        }

                    </div>

                    <div class="report-card-text"
                         style="margin-top: 0.5rem;">

                        <strong>Related priority:</strong>
                        {
                            escape_text(
                                exercise["related_priority"]
                            )
                        }

                    </div>

                </div>
                """
            )


# ============================================================
# LIVE DASHBOARD
# ============================================================

@st.fragment(run_every=0.5)
def render_live_dashboard() -> None:

    drain_voice_events()

    rounds_done = completed_rounds()

    current_round = display_round()

    debate_finished = (
        engine.state.is_finished()
    )

    user_count = len(
        engine.state.user_arguments
    )

    ai_count = len(
        engine.state.ai_arguments
    )

    render_html(
        f"""
        <div class="round-section">

            <div class="round-label">
                CURRENT ROUND
            </div>

            <div class="round-number">
                ROUND {current_round} / {MAX_ROUNDS}
            </div>

            <div class="round-progress"></div>

        </div>
        """
    )

    if debate_finished:
        icon = "🏁"
        title = "Debate Complete"
        subtitle = "All rounds are complete."

    elif engine.is_ai_turn():
        icon = "🧠"
        title = "AI is reasoning"
        subtitle = (
            "Analyzing your argument and "
            "preparing a rebuttal."
        )

    elif st.session_state.voice_started:
        icon = "🎙️"
        title = "Listening"
        subtitle = "Speak your next argument."

    else:
        icon = "🎤"
        title = "Ready"
        subtitle = "Start the voice debate to begin."

    render_html(
        f"""
        <div class="status-card">

            <div class="status-icon">
                {icon}
            </div>

            <div class="status-title">
                {escape_text(title)}
            </div>

            <div class="status-subtitle">
                {escape_text(subtitle)}
            </div>

        </div>
        """
    )

    visual_state = st.session_state.voice_visual_state

    state_config = {
        "ready": (
            "🎤",
            "READY",
            "Start the voice debate to enter the arena.",
            "",
        ),
        "connecting": (
            "🔌",
            "CONNECTING",
            "Establishing the live voice session.",
            "thinking",
        ),
        "listening": (
            "🎙️",
            "YOUR TURN",
            "Speak your next argument.",
            "user",
        ),
        "user_speaking": (
            "🔵",
            "YOU'RE SPEAKING",
            "Your argument is being captured in real time.",
            "user",
        ),
        "thinking": (
            "🧠",
            "AI IS THINKING",
            "Analyzing your argument and preparing a rebuttal.",
            "thinking",
        ),
        "ai_speaking": (
            "🟣",
            "AI IS SPEAKING",
            "Listen to the AI rebuttal.",
            "ai",
        ),
        "complete": (
            "🏁",
            "DEBATE COMPLETE",
            "All 3 rounds are complete. Your report is ready.",
            "complete",
        ),
        "error": (
            "⚠️",
            "VOICE ERROR",
            "Check the voice status below.",
            "error",
        ),
    }

    (
        state_icon,
        state_title,
        state_subtitle,
        state_class,
    ) = state_config.get(
        visual_state,
        state_config["ready"],
    )

    render_html(
        f"""
        <div class="voice-state-panel {state_class}">

            <div class="voice-state-kicker">
                LIVE VOICE STATE
            </div>

            <div class="voice-state-orb">
                {state_icon}
            </div>

            <div class="voice-state-title">
                {escape_text(state_title)}
            </div>

            <div class="voice-state-subtitle">
                {escape_text(state_subtitle)}
            </div>

        </div>
        """
    )

    render_html(
        f"""
        <div class="argument-card">

            <div class="argument-header">
                🎧 VOICE AGENT STATUS
            </div>

            <div class="argument-text">
                {escape_text(
                    st.session_state.voice_status
                )}
            </div>

        </div>
        """
    )

    if st.session_state.voice_error:
        st.error(
            st.session_state.voice_error
        )

    if st.session_state.latest_user_transcript:
        render_html(
            """
            <div class="section-label">
                🎙️ LIVE USER SPEECH
            </div>
            """
        )

        render_html(
            f"""
            <div class="argument-card argument-user">

                <div class="argument-header">
                    🎙️ LISTENING
                </div>

                <div class="argument-text">
                    {escape_text(
                        st.session_state.latest_user_transcript
                    )}
                </div>

            </div>
            """
        )

    if st.session_state.latest_ai_speech:
        render_html(
            """
            <div class="section-label">
                🔊 LIVE AI SPEECH
            </div>
            """
        )

        render_html(
            f"""
            <div class="argument-card argument-ai">

                <div class="argument-header">
                    🔊 AI SPEAKING
                </div>

                <div class="argument-text">
                    {escape_text(
                        st.session_state.latest_ai_speech
                    )}
                </div>

            </div>
            """
        )

    render_html(
        """
        <div class="arena-section-heading">

            <span>⚔️ LIVE DEBATE ARENA</span>

            <span class="arena-live-badge">
                <span class="live-dot"></span>
                LIVE
            </span>

        </div>
        """
    )

    history = (
        engine.state.get_history()
    )

    if not history:
        render_html(
            """
            <div class="argument-card">

                <div class="argument-text">
                    Your debate arguments will appear here in real time.
                </div>

            </div>
            """
        )

    else:
        for argument in history:
            render_argument(
                speaker=argument.speaker,
                text=argument.text,
                round_number=argument.round,
            )

    if engine.last_strategy is not None:
        render_html(
            f"""
            <div class="strategy-card">

                <div class="strategy-label">
                    🧠 CURRENT DEBATE STRATEGY
                </div>

                <div class="strategy-value">
                    {escape_text(
                        format_strategy(
                            engine.last_strategy
                        )
                    )}
                </div>

            </div>
            """
        )

    render_html(
        """
        <div class="section-label">
            LIVE METRICS
        </div>
        """
    )

    metric_one, metric_two, metric_three = (
        st.columns(3)
    )

    with metric_one:
        st.metric(
            "ROUNDS COMPLETED",
            f"{rounds_done} / {MAX_ROUNDS}",
        )

    with metric_two:
        st.metric(
            "YOUR ARGUMENTS",
            user_count,
        )

    with metric_three:
        st.metric(
            "AI REBUTTALS",
            ai_count,
        )

    render_html(
        """
        <div class="section-label">
            📊 DEBATE REPORT
        </div>
        """
    )

    if st.session_state.report is None:

        if not debate_finished:
            render_html(
                """
                <div class="report-card-text"
                     style="margin-top: 0.35rem; margin-bottom: 0.8rem;">

                    Complete all 3 debate rounds to unlock your visual report.

                </div>
                """
            )

        elif st.session_state.voice_visual_state != "complete":
            render_html(
                """
                <div class="report-card"
                     style="margin-bottom: 0.8rem;">

                    <div class="report-card-title">
                        🏁 Debate Complete
                    </div>

                    <div class="report-card-text">
                        Finishing the final AI rebuttal... your report will
                        appear automatically.
                    </div>

                </div>
                """
            )

        elif not st.session_state.report_generation_in_progress:
            # The final AI rebuttal has finished. Generate the report once
            # automatically instead of requiring the user to press a button.
            st.session_state.report_generation_in_progress = True

            try:
                with st.spinner(
                    "Analyzing the complete debate and building your coaching report..."
                ):
                    report = engine.generate_debate_report()

                st.session_state.report = report

            except Exception as exc:
                st.session_state.report_generation_in_progress = False
                st.error(
                    f"Could not generate report: {exc}"
                )

        if st.session_state.report is not None:
            render_report(
                st.session_state.report
            )

    else:
        render_report(
            st.session_state.report
        )


# ============================================================
# HEADER
# ============================================================

render_html(
    """
    <div class="topbar">

        <div class="brand">

            <div class="brand-icon">
                ⚔️
            </div>

            <div>

                <div class="brand-name">
                    AI Debate Arena
                </div>

                <div class="brand-subtitle">
                    Voice-first AI debate training · Real-time rebuttals · Personalized coaching
                </div>

            </div>

        </div>

        <div class="live-pill">

            <span class="live-dot"></span>

            LIVE

        </div>

    </div>
    """
)


# ============================================================
# DEBATE SETUP / TOPIC
# ============================================================

setup_locked = (
    st.session_state.voice_started
)

render_html(
    """
    <div class="setup-card">

        <div class="setup-label">
            DEBATE SETUP
        </div>

        <div class="setup-title">
            📝 Choose your battlefield
        </div>

        <div class="setup-subtitle">
            Enter any topic and choose your side. The AI will automatically
            defend the opposite position.
        </div>

    </div>
    """
)

setup_topic = st.text_input(
    "DEBATE TOPIC",
    value=st.session_state.setup_topic,
    placeholder="e.g. Should AI replace human teachers?",
    disabled=setup_locked,
    key="debate_topic_input",
)

setup_position = st.radio(
    "YOUR POSITION",
    options=["SUPPORT", "OPPOSE"],
    index=(
        0
        if st.session_state.setup_position == "SUPPORT"
        else 1
    ),
    horizontal=True,
    disabled=setup_locked,
    key="debate_position_input",
)

if not setup_locked:
    st.session_state.setup_topic = (
        setup_topic.strip()
    )

    st.session_state.setup_position = (
        setup_position
    )

user_position_preview = (
    st.session_state.setup_position
)

ai_position_preview = (
    "OPPOSE"
    if user_position_preview == "SUPPORT"
    else "SUPPORT"
)

render_html(
    f"""
    <div class="setup-ai-note">
        🤖 AI POSITION → {escape_text(ai_position_preview)}
    </div>
    """
)

render_html(
    f"""
    <div class="topic-card">

        <div class="topic-label">
            TODAY'S DEBATE
        </div>

        <div class="topic-title">
            {escape_text(
                engine.state.topic
                if st.session_state.voice_started
                else (
                    st.session_state.setup_topic
                    or TOPIC
                )
            )}
        </div>

    </div>
    """
)

st.markdown("")

left, right = st.columns(2)

with left:
    render_html(
        f"""
        <div class="position-card">

            <div class="position-label">
                👤 YOUR POSITION
            </div>

            <div class="position-user">
                {escape_text(
                    engine.state.user_position
                    if st.session_state.voice_started
                    else user_position_preview
                )}
            </div>

        </div>
        """
    )

with right:
    render_html(
        f"""
        <div class="position-card">

            <div class="position-label">
                🤖 AI POSITION
            </div>

            <div class="position-ai">
                {escape_text(
                    engine.state.ai_position
                    if st.session_state.voice_started
                    else ai_position_preview
                )}
            </div>

        </div>
        """
    )


# ============================================================
# CONTROLS
# ============================================================

st.markdown("")

control_one, control_two = st.columns(2)


# ============================================================
# START
# ============================================================

with control_one:

    start_disabled = (
        not bool(ASSEMBLYAI_API_KEY)
        or st.session_state.voice_started
        or engine.state.is_finished()
    )

    if st.button(
        "🎙️ START VOICE DEBATE",
        key="start_voice",
        disabled=start_disabled,
    ):
        st.session_state.voice_error = ""

        try:
            topic = (
                st.session_state.setup_topic.strip()
            )

            if not topic:
                st.session_state.voice_error = (
                    "Please enter a debate topic before starting."
                )
                st.stop()

            user_position = (
                st.session_state.setup_position
            )

            ai_position = (
                "OPPOSE"
                if user_position == "SUPPORT"
                else "SUPPORT"
            )

            engine = create_debate_engine(
                topic=topic,
                user_position=user_position,
                ai_position=ai_position,
            )

            st.session_state.debate_engine = (
                engine
            )

            voice_agent = create_voice_agent()

            st.session_state.voice_agent = (
                voice_agent
            )

            st.session_state.voice_started = (
                True
            )

            st.session_state.voice_status = (
                "Starting Voice Agent..."
            )

            st.session_state.latest_ai_speech = ""

            voice_agent.start()

        except Exception as exc:
            st.session_state.voice_started = (
                False
            )

            st.session_state.voice_status = (
                "Failed to start"
            )

            st.session_state.voice_error = (
                f"{type(exc).__name__}: {exc}"
            )


# ============================================================
# RESET
# ============================================================

with control_two:

    if st.button(
        "↻ RESET DEBATE",
        key="reset_debate",
    ):
        voice_agent = (
            st.session_state.voice_agent
        )

        if (
            voice_agent is not None
            and voice_agent.is_running()
        ):
            try:
                voice_agent.stop()
            except Exception:
                pass

        st.session_state.debate_engine = (
            create_debate_engine()
        )

        st.session_state.voice_agent = None

        st.session_state.voice_events = (
            queue.Queue()
        )

        st.session_state.voice_started = (
            False
        )

        st.session_state.voice_status = (
            "Ready"
        )

        st.session_state.voice_error = ""

        st.session_state.latest_user_transcript = ""

        st.session_state.latest_ai_transcript = ""

        st.session_state.latest_ai_speech = ""

        st.session_state.voice_visual_state = (
            "ready"
        )

        st.session_state.report = None

        st.session_state.report_generation_in_progress = False

        st.session_state.setup_topic = TOPIC
        st.session_state.setup_position = "OPPOSE"

        st.rerun()


# ============================================================
# API KEY CHECK
# ============================================================

if not ASSEMBLYAI_API_KEY:
    st.warning(
        "ASSEMBLYAI_API_KEY is not configured. "
        "Please add it to your .env file."
    )


# ============================================================
# LIVE DASHBOARD
# ============================================================

render_live_dashboard()


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">
        AI DEBATE ARENA · ASSEMBLYAI VOICE AGENT · GEMINI DEBATE ENGINE
    </div>
    """
)
