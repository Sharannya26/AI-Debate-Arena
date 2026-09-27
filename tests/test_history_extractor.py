from debate_arena.debate.argument import Argument
from debate_arena.debate.history_extractor import (
    DebateHistoryExtractor,
)
from debate_arena.debate.state import DebateState


def create_test_state() -> DebateState:
    """Create a sample completed debate state."""

    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    state.add_user_argument(
        Argument(
            speaker="user",
            text="Social media provides educational opportunities.",
            round=1,
            turn=1,
        )
    )

    state.add_ai_argument(
        Argument(
            speaker="ai",
            text="Those benefits do not eliminate its risks.",
            round=1,
            turn=1,
        )
    )

    state.add_user_argument(
        Argument(
            speaker="user",
            text="Students can learn responsible social media usage.",
            round=2,
            turn=2,
        )
    )

    state.add_ai_argument(
        Argument(
            speaker="ai",
            text="Responsible usage is difficult to maintain.",
            round=2,
            turn=2,
        )
    )

    return state


def test_extracts_complete_debate_history():
    state = create_test_state()

    extractor = DebateHistoryExtractor()

    history = extractor.extract(state)

    assert len(history) == 4

    assert history[0] == {
        "speaker": "user",
        "text": "Social media provides educational opportunities.",
        "round": 1,
        "turn": 1,
    }

    assert history[1] == {
        "speaker": "ai",
        "text": "Those benefits do not eliminate its risks.",
        "round": 1,
        "turn": 1,
    }

    assert history[2] == {
        "speaker": "user",
        "text": "Students can learn responsible social media usage.",
        "round": 2,
        "turn": 2,
    }

    assert history[3] == {
        "speaker": "ai",
        "text": "Responsible usage is difficult to maintain.",
        "round": 2,
        "turn": 2,
    }


def test_extracts_empty_history():
    state = DebateState(
        topic="Test topic",
        user_position="Against",
        ai_position="For",
    )

    extractor = DebateHistoryExtractor()

    history = extractor.extract(state)

    assert history == []


def test_extracted_history_is_independent_from_state_history():
    state = create_test_state()

    extractor = DebateHistoryExtractor()

    history = extractor.extract(state)

    history.append(
        {
            "speaker": "user",
            "text": "Extra argument.",
            "round": 3,
            "turn": 3,
        }
    )

    assert len(history) == 5
    assert len(state.history) == 4


def test_extractor_rejects_none_state():
    extractor = DebateHistoryExtractor()

    try:
        extractor.extract(None)
    except ValueError as exc:
        assert "Debate state cannot be None." in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for None debate state."
        )