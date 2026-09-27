import os
import time

from dotenv import load_dotenv

from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState
from debate_arena.voice.voice_agent import VoiceAgent


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

assemblyai_api_key = os.getenv(
    "ASSEMBLYAI_API_KEY"
)

if not assemblyai_api_key:

    raise RuntimeError(
        "ASSEMBLYAI_API_KEY is not configured."
    )


# ============================================================
# DEBATE ENGINE
# ============================================================

engine = DebateEngine(
    state=DebateState(
        topic=(
            "Should social media be banned "
            "for students?"
        ),
        user_position="Not banned",
        ai_position="Should ban",
        max_rounds=3,
    )
)


# ============================================================
# CALLBACKS
# ============================================================

def on_user_transcript(
    transcript: str,
) -> None:

    print()
    print("-" * 60)
    print("👤 USER")
    print("-" * 60)
    print(transcript)


def on_ai_transcript(
    transcript: str,
) -> None:

    print()
    print("-" * 60)
    print("🤖 AI")
    print("-" * 60)
    print(transcript)


def on_status(
    status: str,
) -> None:

    print(
        f"\n🔵 STATUS: {status}"
    )


def on_error(
    error: str,
) -> None:

    print(
        f"\n❌ ERROR: {error}"
    )


# ============================================================
# VOICE AGENT
# ============================================================

agent = VoiceAgent(
    engine=engine,
    api_key=assemblyai_api_key,
    on_user_transcript=on_user_transcript,
    on_ai_transcript=on_ai_transcript,
    on_status=on_status,
    on_error=on_error,
)


# ============================================================
# RUN
# ============================================================

print("=" * 70)
print("⚔️ AI DEBATE ARENA — EXTRACTED VOICE AGENT TEST")
print("=" * 70)
print()
print(
    "Topic: Should social media be banned for students?"
)
print()
print(
    "Speak normally."
)
print(
    "Press Ctrl+C to stop."
)
print()

agent.start()

try:

    while agent.is_running():

        time.sleep(0.5)

except KeyboardInterrupt:

    print()
    print(
        "🛑 Stopping Voice Agent..."
    )

finally:

    agent.stop()

    print(
        "✅ Voice Agent stopped."
    )