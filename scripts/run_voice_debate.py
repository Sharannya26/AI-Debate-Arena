from debate_arena.assemblyai.realtime import start_realtime_transcription
from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState
from debate_arena.voice.orchestrator import DebateOrchestrator


def main() -> None:
    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    engine = DebateEngine(state)

    orchestrator = DebateOrchestrator(
        engine=engine,
    )

    print("\n" + "=" * 60)
    print("🔥 AI DEBATE ARENA — LIVE VOICE DEBATE")
    print("=" * 60)

    print(f"\n📌 Topic: {state.topic}")
    print(f"👤 Your position: {state.user_position}")
    print(f"🤖 AI position: {state.ai_position}")

    print("\n🎤 Speak your argument.")
    print("🤖 The AI will listen, reason, and respond.")
    print("Press Ctrl+C to stop.\n")

    start_realtime_transcription(
        on_final_transcript=orchestrator.handle_final_transcript,
    )


if __name__ == "__main__":
    main()