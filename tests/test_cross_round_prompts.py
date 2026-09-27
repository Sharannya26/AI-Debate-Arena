import pytest

from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis
from debate_arena.debate.cross_round_prompts import (
    build_cross_round_analysis_prompt,
)


def make_analysis() -> CrossRoundAnalysis:
    return CrossRoundAnalysis(
        overall_trajectory="Performance improved across the debate.",
        improvement_patterns=[
            "Reasoning quality improved across the debate."
        ],
        decline_patterns=[
            "Communication quality declined across the debate."
        ],
        stable_patterns=[
            "Responsiveness remained stable across the debate."
        ],
        recurring_patterns=[
            "Evidence usage remained consistently Limited across the rounds."
        ],
        cross_dimension_patterns=[
            "Reasoning improved while evidence usage remained limited."
        ],
        key_insights=[
            "Later rounds showed stronger reasoning."
        ],
    )


def test_prompt_requires_analysis():
    with pytest.raises(ValueError):
        build_cross_round_analysis_prompt(None)


def test_prompt_contains_overall_trajectory():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert "Performance improved across the debate." in prompt


def test_prompt_contains_improvement_patterns():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert "Reasoning quality improved across the debate." in prompt


def test_prompt_contains_decline_patterns():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert "Communication quality declined across the debate." in prompt


def test_prompt_contains_stable_patterns():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert "Responsiveness remained stable across the debate." in prompt


def test_prompt_contains_recurring_patterns():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert (
        "Evidence usage remained consistently Limited across the rounds."
        in prompt
    )


def test_prompt_contains_cross_dimension_patterns():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert (
        "Reasoning improved while evidence usage remained limited."
        in prompt
    )


def test_prompt_prohibits_numerical_scores():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert "Do NOT introduce numerical scores." in prompt


def test_prompt_prohibits_invented_information():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert "Do NOT invent evidence, examples, statistics, events, or arguments." in prompt


def test_prompt_prohibits_fact_checking():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert "Do NOT fact-check the debate." in prompt


def test_prompt_prohibits_political_judgment():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert "Do NOT judge political positions." in prompt


def test_prompt_requires_json_output():
    prompt = build_cross_round_analysis_prompt(make_analysis())

    assert "Return ONLY valid JSON" in prompt
    assert '"overall_interpretation": "string"' in prompt
    assert '"improvement_interpretation": "string"' in prompt
    assert '"decline_interpretation": "string"' in prompt
    assert '"stability_interpretation": "string"' in prompt
    assert '"recurring_interpretation": "string"' in prompt
    assert '"cross_dimension_interpretation": "string"' in prompt
    assert '"key_insights": ["string"]' in prompt