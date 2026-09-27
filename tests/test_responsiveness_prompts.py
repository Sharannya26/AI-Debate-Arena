import pytest

from debate_arena.debate.responsiveness_prompts import (
    build_responsiveness_prompt,
)


def test_builds_responsiveness_prompt():
    prompt = build_responsiveness_prompt(
        previous_ai_argument=(
            "Public transportation is too expensive."
        ),
        user_argument=(
            "Government subsidies could make transit more affordable."
        ),
    )

    assert "Public transportation is too expensive." in prompt
    assert (
        "Government subsidies could make transit more affordable."
        in prompt
    )

    assert "responsiveness" in prompt
    assert "addressed_points" in prompt
    assert "ignored_points" in prompt


def test_prompt_requires_previous_ai_argument():
    with pytest.raises(
        ValueError,
        match="Previous AI argument cannot be empty.",
    ):
        build_responsiveness_prompt(
            previous_ai_argument="   ",
            user_argument="Some response.",
        )


def test_prompt_requires_user_argument():
    with pytest.raises(
        ValueError,
        match="User argument cannot be empty.",
    ):
        build_responsiveness_prompt(
            previous_ai_argument="Some AI argument.",
            user_argument="   ",
        )


def test_prompt_strips_arguments():
    prompt = build_responsiveness_prompt(
        previous_ai_argument="  AI argument.  ",
        user_argument="  User response.  ",
    )

    assert "AI argument." in prompt
    assert "User response." in prompt

    assert "  AI argument.  " not in prompt
    assert "  User response.  " not in prompt


def test_prompt_requires_json_output():
    prompt = build_responsiveness_prompt(
        previous_ai_argument="AI argument.",
        user_argument="User response.",
    )

    assert "ONLY valid JSON" in prompt
    assert '"responsiveness"' in prompt
    assert '"addressed_points"' in prompt
    assert '"ignored_points"' in prompt