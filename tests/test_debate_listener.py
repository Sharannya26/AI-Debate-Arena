from debate_arena.debate.argument_analyzer import (
    ArgumentAnalysis,
)
from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState
from debate_arena.voice.debate_listener import DebateListener


class FakeArgumentAnalyzer:
    """Test double that avoids real Gemini API calls."""

    def analyze(
        self,
        argument: str,
    ) -> ArgumentAnalysis:
        return ArgumentAnalysis(
            claim=argument,
            reasoning="Test reasoning.",
            assumptions=[],
            evidence=[],
            weaknesses=[],
            argument_type="general",
        )


def create_engine() -> DebateEngine:
    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    return DebateEngine(
        state,
        argument_analyzer=FakeArgumentAnalyzer(),
    )


def test_transcript_is_sent_to_debate_engine() -> None:
    engine = create_engine()

    listener = DebateListener(engine)

    transcript = (
        "Social media should not be banned because "
        "students can use it for education."
    )

    listener.handle_transcript(transcript)

    assert len(engine.state.user_arguments) == 1
    assert engine.state.user_arguments[0].text == transcript
    assert engine.state.current_turn == "ai"


def test_empty_transcript_is_ignored() -> None:
    engine = create_engine()

    listener = DebateListener(engine)

    listener.handle_transcript("   ")

    assert len(engine.state.user_arguments) == 0


def test_transcript_callback_is_called() -> None:
    engine = create_engine()

    received: list[str] = []

    listener = DebateListener(
        engine,
        on_transcript=received.append,
    )

    listener.handle_transcript("This is a test argument.")

    assert received == ["This is a test argument."]