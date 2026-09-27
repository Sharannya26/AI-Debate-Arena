import pytest

from debate_arena.debate.consistency_prompts import (
    build_consistency_prompt,
)


def test_consistency_prompt_contains_all_arguments():
    prompt = build_consistency_prompt(
        [
            "Students should have access to online education.",
            "Online learning gives students more opportunities.",
        ]
    )

    assert (
        "Students should have access to online education."
        in prompt
    )

    assert (
        "Online learning gives students more opportunities."
        in prompt
    )


def test_consistency_prompt_contains_round_labels():
    prompt = build_consistency_prompt(
        [
            "Students should have access to online education.",
            "Online learning gives students more opportunities.",
        ]
    )

    assert "Round 1:" in prompt
    assert "Round 2:" in prompt


def test_consistency_prompt_requests_json():
    prompt = build_consistency_prompt(
        [
            "Students should have access to online education.",
            "Online learning gives students more opportunities.",
        ]
    )

    assert '"consistency"' in prompt
    assert '"consistent_points"' in prompt
    assert '"inconsistent_points"' in prompt


def test_consistency_prompt_focuses_on_semantic_consistency():
    prompt = build_consistency_prompt(
        [
            "Students should have access to online education.",
            "Online learning gives students more opportunities.",
        ]
    )

    assert "semantically consistent" in prompt
    assert "keyword overlap" in prompt


def test_consistency_prompt_rejects_insufficient_arguments():
    with pytest.raises(
        ValueError,
        match="At least two user arguments are required",
    ):
        build_consistency_prompt(
            ["Only one argument."]
        )


def test_consistency_prompt_rejects_none():
    with pytest.raises(
        ValueError,
        match="User arguments cannot be None",
    ):
        build_consistency_prompt(None)