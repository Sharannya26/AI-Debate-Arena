import pytest

from debate_arena.debate.performance_summary import (
    PerformanceSummary,
)
from debate_arena.debate.semantic_performance_prompts import (
    build_semantic_performance_prompt,
)


def create_summary():
    return PerformanceSummary(
        overall_summary="Performance improved.",
        dimension_summaries={
            "evidence usage":
                "Evidence usage improved across the debate.",
            "reasoning quality":
                "Reasoning quality remained consistent.",
        },
        strongest_moments=[
            "Round 2: Strong reasoning."
        ],
        weakest_moments=[
            "Round 1: Weak evidence usage."
        ],
        coaching_priorities=[
            "Support major claims with evidence."
        ],
    )


def test_prompt_contains_overall_summary():
    prompt = build_semantic_performance_prompt(
        create_summary()
    )

    assert "Performance improved." in prompt


def test_prompt_contains_dimension_summaries():
    prompt = build_semantic_performance_prompt(
        create_summary()
    )

    assert "evidence usage" in prompt
    assert "reasoning quality" in prompt


def test_prompt_contains_strongest_moments():
    prompt = build_semantic_performance_prompt(
        create_summary()
    )

    assert "Round 2: Strong reasoning." in prompt


def test_prompt_contains_weakest_moments():
    prompt = build_semantic_performance_prompt(
        create_summary()
    )

    assert "Round 1: Weak evidence usage." in prompt


def test_prompt_contains_coaching_priorities():
    prompt = build_semantic_performance_prompt(
        create_summary()
    )

    assert (
        "Support major claims with evidence."
        in prompt
    )


def test_prompt_requires_json():
    prompt = build_semantic_performance_prompt(
        create_summary()
    )

    assert "Return ONLY valid JSON" in prompt
    assert '"overall_interpretation"' in prompt
    assert '"key_insights"' in prompt


def test_prompt_contains_safety_constraints():
    prompt = build_semantic_performance_prompt(
        create_summary()
    )

    assert "Do NOT invent new evidence." in prompt
    assert "Do NOT introduce numerical scores." in prompt


def test_prompt_handles_empty_sections():
    summary = PerformanceSummary(
        overall_summary="Baseline performance.",
    )

    prompt = build_semantic_performance_prompt(
        summary
    )

    assert "No dimension summaries available." in prompt
    assert "No strongest moments identified." in prompt
    assert "No weakest moments identified." in prompt
    assert "No coaching priorities identified." in prompt


def test_prompt_rejects_none_summary():
    with pytest.raises(
        ValueError,
        match="Performance summary cannot be None",
    ):
        build_semantic_performance_prompt(None)