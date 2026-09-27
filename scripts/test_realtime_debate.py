from debate_arena.assemblyai.realtime import start_realtime_transcription
from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState
from debate_arena.voice.debate_listener import DebateListener


def main() -> None:
    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    engine = DebateEngine(state)

    listener = DebateListener(
        engine,
        on_transcript=lambda text: print(
            f"\n🧠 DebateListener received: {text}"
        ),
    )

    print("\n" + "=" * 60)
    print("🔥 AI DEBATE ARENA — REALTIME TRANSCRIPT TEST")
    print("=" * 60)

    print(f"\nTopic: {state.topic}")
    print(f"User position: {state.user_position}")
    print(f"AI position: {state.ai_position}")

    print("\n🎤 Speak one complete argument.")
    print("Press Ctrl+C when finished.")

    start_realtime_transcription(
        on_final_transcript=listener.handle_transcript,
    )


if __name__ == "__main__":
    main()