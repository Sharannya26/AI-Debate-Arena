from debate_arena.debate.argument import Argument
from debate_arena.debate.state import DebateState


def test_debate_state_initializes():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    assert state.topic == "Should social media be banned for teenagers?"
    assert state.user_position == "Against"
    assert state.ai_position == "For"
    assert state.current_round == 1
    assert state.current_turn == "user"


def test_arguments_are_stored():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    user_argument = Argument(
        speaker="user",
        text="Social media has educational benefits.",
        round=1,
        turn=1,
    )

    ai_argument = Argument(
        speaker="ai",
        text="Those benefits do not eliminate its risks.",
        round=1,
        turn=2,
    )

    state.add_user_argument(user_argument)
    state.add_ai_argument(ai_argument)

    assert len(state.user_arguments) == 1
    assert len(state.ai_arguments) == 1

    assert state.user_arguments[0].text == (
        "Social media has educational benefits."
    )
    assert state.ai_arguments[0].text == (
        "Those benefits do not eliminate its risks."
    )


def test_round_and_turn_can_change():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    state.switch_turn()
    assert state.current_turn == "ai"

    state.advance_round()
    assert state.current_round == 2

def test_debate_finishes_after_max_rounds():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    assert not state.is_finished()

    state.advance_round()
    assert not state.is_finished()

    state.advance_round()
    assert not state.is_finished()

    state.advance_round()
    assert state.is_finished()

def test_history_preserves_argument_order():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    user_argument_1 = Argument(
        speaker="user",
        text="Social media provides educational opportunities.",
        round=1,
        turn=1,
    )

    ai_argument_1 = Argument(
        speaker="ai",
        text="Those benefits do not eliminate its risks.",
        round=1,
        turn=1,
    )

    user_argument_2 = Argument(
        speaker="user",
        text="The real issue is how social media is used.",
        round=2,
        turn=2,
    )

    ai_argument_2 = Argument(
        speaker="ai",
        text="Usage controls are difficult to enforce consistently.",
        round=2,
        turn=2,
    )

    state.add_user_argument(user_argument_1)
    state.add_ai_argument(ai_argument_1)
    state.add_user_argument(user_argument_2)
    state.add_ai_argument(ai_argument_2)

    assert len(state.history) == 4

    assert state.history[0] == user_argument_1
    assert state.history[1] == ai_argument_1
    assert state.history[2] == user_argument_2
    assert state.history[3] == ai_argument_2

def test_get_history_returns_chronological_copy():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    user_argument = Argument(
        speaker="user",
        text="Social media has educational benefits.",
        round=1,
        turn=1,
    )

    ai_argument = Argument(
        speaker="ai",
        text="Those benefits do not remove the risks.",
        round=1,
        turn=1,
    )

    state.add_user_argument(user_argument)
    state.add_ai_argument(ai_argument)

    history = state.get_history()

    assert history == [user_argument, ai_argument]

    # Verify that the returned list is a copy.
    assert history is not state.history

def test_get_context_formats_debate_history():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
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

    context = state.get_context()

    assert "Topic: Should social media be banned for teenagers?" in context
    assert "User position: Against" in context
    assert "AI position: For" in context

    assert (
        "Round 1 - User: "
        "Social media provides educational opportunities."
    ) in context

    assert (
        "Round 1 - AI: "
        "Those benefits do not eliminate its risks."
    ) in context

def test_get_context_preserves_multiple_rounds_in_order():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
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
            text="The issue is how social media is used.",
            round=2,
            turn=2,
        )
    )

    state.add_ai_argument(
        Argument(
            speaker="ai",
            text="Usage controls are difficult to enforce.",
            round=2,
            turn=2,
        )
    )

    context = state.get_context()

    user_round_1 = context.index(
        "Round 1 - User: Social media provides educational opportunities."
    )

    ai_round_1 = context.index(
        "Round 1 - AI: Those benefits do not eliminate its risks."
    )

    user_round_2 = context.index(
        "Round 2 - User: The issue is how social media is used."
    )

    ai_round_2 = context.index(
        "Round 2 - AI: Usage controls are difficult to enforce."
    )

    assert user_round_1 < ai_round_1 < user_round_2 < ai_round_2