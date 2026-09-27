import pytest

from debate_arena.debate.adaptive_mini_debate import (
    AdaptiveMiniDebate,
)


def make_mini_debate() -> AdaptiveMiniDebate:
    return AdaptiveMiniDebate(
        topic="Should college education be free?",
        focus_area="Improve evidence usage",
        user_prompt=(
            "Make one claim and support it with "
            "concrete evidence."
        ),
    )


def test_adaptive_mini_debate_stores_values():
    debate = make_mini_debate()

    assert (
        debate.topic
        == "Should college education be free?"
    )

    assert (
        debate.focus_area
        == "Improve evidence usage"
    )

    assert (
        debate.user_prompt
        == (
            "Make one claim and support it with "
            "concrete evidence."
        )
    )

    assert debate.current_turn == "user"
    assert debate.round_number == 1
    assert debate.max_rounds == 2
    assert debate.user_responses == []
    assert debate.ai_responses == []


def test_adaptive_mini_debate_strips_whitespace():
    debate = AdaptiveMiniDebate(
        topic="  Debate topic  ",
        focus_area="  Improve evidence usage  ",
        user_prompt="  Make an argument.  ",
        ai_prompt="  Challenge the evidence.  ",
        current_turn=" AI ",
    )

    assert debate.topic == "Debate topic"
    assert debate.focus_area == "Improve evidence usage"
    assert debate.user_prompt == "Make an argument."
    assert debate.ai_prompt == "Challenge the evidence."
    assert debate.current_turn == "ai"


def test_add_user_response_updates_state():
    debate = make_mini_debate()

    debate.add_user_response(
        "College education should be free because it improves access."
    )

    assert debate.user_responses == [
        "College education should be free because it improves access."
    ]

    assert debate.current_turn == "ai"


def test_add_ai_response_updates_state():
    debate = make_mini_debate()

    debate.add_ai_response(
        "What evidence supports that claim?"
    )

    assert debate.ai_responses == [
        "What evidence supports that claim?"
    ]

    assert debate.current_turn == "user"


def test_add_responses_strips_whitespace():
    debate = make_mini_debate()

    debate.add_user_response(
        "  My claim has supporting evidence.  "
    )

    debate.add_ai_response(
        "  Can you explain that evidence?  "
    )

    assert debate.user_responses == [
        "My claim has supporting evidence."
    ]

    assert debate.ai_responses == [
        "Can you explain that evidence?"
    ]


def test_advance_round():
    debate = make_mini_debate()

    assert debate.round_number == 1

    debate.advance_round()

    assert debate.round_number == 2


def test_mini_debate_is_not_finished_initially():
    debate = make_mini_debate()

    assert debate.is_finished() is False


def test_mini_debate_is_finished_after_max_rounds():
    debate = make_mini_debate()

    debate.advance_round()
    debate.advance_round()

    assert debate.round_number == 3
    assert debate.is_finished() is True


@pytest.mark.parametrize(
    "field,value,error_message",
    [
        (
            "topic",
            "",
            "Mini-debate topic cannot be empty.",
        ),
        (
            "focus_area",
            "",
            "Mini-debate focus area cannot be empty.",
        ),
        (
            "user_prompt",
            "",
            "Mini-debate user prompt cannot be empty.",
        ),
    ],
)
def test_mini_debate_rejects_empty_required_fields(
    field,
    value,
    error_message,
):
    values = {
        "topic": "Practice debate",
        "focus_area": "Improve reasoning quality",
        "user_prompt": "Make an argument.",
    }

    values[field] = value

    with pytest.raises(
        ValueError,
        match=error_message,
    ):
        AdaptiveMiniDebate(**values)


def test_mini_debate_rejects_invalid_turn():
    with pytest.raises(
        ValueError,
        match="Mini-debate current turn must be 'user' or 'ai'.",
    ):
        AdaptiveMiniDebate(
            topic="Practice debate",
            focus_area="Improve reasoning quality",
            user_prompt="Make an argument.",
            current_turn="invalid",
        )


def test_mini_debate_rejects_invalid_round_number():
    with pytest.raises(
        ValueError,
        match="Mini-debate round number must be at least 1.",
    ):
        AdaptiveMiniDebate(
            topic="Practice debate",
            focus_area="Improve reasoning quality",
            user_prompt="Make an argument.",
            round_number=0,
        )


def test_mini_debate_rejects_invalid_max_rounds():
    with pytest.raises(
        ValueError,
        match="Mini-debate max rounds must be at least 1.",
    ):
        AdaptiveMiniDebate(
            topic="Practice debate",
            focus_area="Improve reasoning quality",
            user_prompt="Make an argument.",
            max_rounds=0,
        )


def test_add_user_response_rejects_empty_response():
    debate = make_mini_debate()

    with pytest.raises(
        ValueError,
        match="Mini-debate user response cannot be empty.",
    ):
        debate.add_user_response("")


def test_add_ai_response_rejects_empty_response():
    debate = make_mini_debate()

    with pytest.raises(
        ValueError,
        match="Mini-debate AI response cannot be empty.",
    ):
        debate.add_ai_response("")


def test_mini_debate_is_dataclass():
    debate = make_mini_debate()

    assert hasattr(
        debate,
        "__dataclass_fields__",
    )