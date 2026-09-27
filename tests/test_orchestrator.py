from unittest.mock import Mock

from debate_arena.debate.debate_response import DebateResponse
from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState
from debate_arena.debate.strategy import DebateStrategy
from debate_arena.voice.orchestrator import DebateOrchestrator


def create_engine() -> DebateEngine:
    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    llm = Mock()

    llm.generate_debate_response.return_value = DebateResponse(
        strategy=DebateStrategy.DIRECT_COUNTER,
        rebuttal=(
            "Students may benefit from social media, "
            "but unrestricted access can cause distraction."
        ),
    )

    return DebateEngine(
        state=state,
        llm=llm,
    )


def test_orchestrator_processes_user_argument() -> None:
    engine = create_engine()

    tts = Mock()

    engine.tts = tts

    orchestrator = DebateOrchestrator(
        engine=engine,
    )

    orchestrator.handle_final_transcript(
        "Social media should not be banned because "
        "students can use it for education."
    )

    assert len(
        engine.state.user_arguments
    ) == 1

    assert len(
        engine.state.ai_arguments
    ) == 1

    assert (
        engine.state.current_turn
        == "user"
    )

    tts.speak_stream.assert_called_once()


def test_empty_transcript_is_ignored() -> None:
    engine = create_engine()

    tts = Mock()

    engine.tts = tts

    orchestrator = DebateOrchestrator(
        engine=engine,
    )

    orchestrator.handle_final_transcript(
        "   "
    )

    assert len(
        engine.state.user_arguments
    ) == 0

    assert len(
        engine.state.ai_arguments
    ) == 0

    tts.speak_stream.assert_not_called()