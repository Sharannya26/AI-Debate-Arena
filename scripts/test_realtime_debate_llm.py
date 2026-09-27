from debate_arena.assemblyai.realtime import start_realtime_transcription
from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState
from debate_arena.voice.debate_listener import DebateListener


def handle_user_argument(
    engine: DebateEngine,
    transcript: str,
) -> None:
    """Process a final user transcript through the debate engine."""

    print("\n" + "-" * 60)
    print("🧠 PROCESSING USER ARGUMENT")
    print("-" * 60)

    print(f"\n👤 User:")
    print(transcript)

    rebuttal = engine.generate_and_submit_ai_rebuttal()

    print("\n🤖 AI REBUTTAL:")
    print(rebuttal)

    print("\n📊 DEBATE STATE")
    print(f"User arguments: {len(engine.state.user_arguments)}")
    print(f"AI arguments: {len(engine.state.ai_arguments)}")
    print(f"Current turn: {engine.state.current_turn}")


def main() -> None:
    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    engine = DebateEngine(state)

    def process_transcript(transcript: str) -> None:
        listener = DebateListener(engine)

        listener.handle_transcript(transcript)

        handle_user_argument(
            engine,
            transcript,
        )

    print("\n" + "=" * 60)
    print("🔥 AI DEBATE ARENA — REALTIME + GEMINI TEST")
    print("=" * 60)

    print(f"\nTopic: {state.topic}")
    print(f"User position: {state.user_position}")
    print(f"AI position: {state.ai_position}")

    print("\n🎤 Speak one complete argument.")
    print("Press Ctrl+C after the AI responds.")

    start_realtime_transcription(
        on_final_transcript=process_transcript,
    )


if __name__ == "__main__":
    main()