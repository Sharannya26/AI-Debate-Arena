from debate_arena.debate.advanced_debate_analysis import (
    AdvancedDebateAnalysis,
)
from debate_arena.debate.debate_performance import DebatePerformance
from debate_arena.debate.performance_summary import PerformanceSummary
from debate_arena.debate.round_performance import RoundPerformance
from debate_arena.debate.advanced_debate_prompts import (
    build_advanced_debate_analysis_prompt,
)


def create_performance():
    return DebatePerformance(
        round_performances=[
            RoundPerformance(
                round=1,
                argument_quality="Argument contains a clear claim.",
                communication_quality="Speech was delivered clearly.",
                evidence_usage="Limited evidence was identified.",
                reasoning_quality="Reasoning was identified.",
                responsiveness="Response addressed the opponent's point.",
            ),
            RoundPerformance(
                round=2,
                argument_quality="Argument contains a clear claim supported by reasoning.",
                communication_quality="Speech was delivered clearly.",
                evidence_usage="Moderate evidence usage was identified.",
                reasoning_quality="Strong reasoning was identified.",
                responsiveness="Response addressed the opponent's main point.",
            ),
        ],
        argument_quality="Argument quality improved across the debate.",
        communication_quality="Communication remained clear.",
        responsiveness="Responsiveness remained strong.",
        consistency="Mostly consistent.",
        evidence_usage="Evidence usage improved across the debate.",
        reasoning_quality="Reasoning improved across the debate.",
        strongest_moments=[
            "Strong reasoning was identified in round 2."
        ],
        weakest_moments=[
            "Limited evidence was identified in round 1."
        ],
        coaching_priorities=[
            "Support major claims with concrete evidence."
        ],
    )


def create_summary():
    return PerformanceSummary(
        overall_summary="The user's performance improved across the debate.",
        dimension_summaries={
            "argument quality": "Argument quality improved.",
            "communication quality": "Communication remained clear.",
            "responsiveness": "Responsiveness remained strong.",
            "consistency": "Mostly consistent.",
            "evidence usage": "Evidence usage improved.",
            "reasoning quality": "Reasoning improved.",
        },
        strongest_moments=[
            "Strong reasoning was identified in round 2."
        ],
        weakest_moments=[
            "Limited evidence was identified in round 1."
        ],
        coaching_priorities=[
            "Support major claims with concrete evidence."
        ],
    )


def test_prompt_contains_performance_data():
    prompt = build_advanced_debate_analysis_prompt(
        create_performance(),
        create_summary(),
    )

    assert "Argument quality improved across the debate." in prompt
    assert "Mostly consistent." in prompt
    assert "Strong reasoning was identified in round 2." in prompt


def test_prompt_contains_summary_data():
    prompt = build_advanced_debate_analysis_prompt(
        create_performance(),
        create_summary(),
    )

    assert "The user's performance improved across the debate." in prompt
    assert "Evidence usage improved." in prompt


def test_prompt_requires_cross_dimension_patterns():
    prompt = build_advanced_debate_analysis_prompt(
        create_performance(),
        create_summary(),
    )

    assert "Cross-dimension patterns" in prompt


def test_prompt_requires_round_patterns():
    prompt = build_advanced_debate_analysis_prompt(
        create_performance(),
        create_summary(),
    )

    assert "Round patterns" in prompt


def test_prompt_forbids_numerical_scores():
    prompt = build_advanced_debate_analysis_prompt(
        create_performance(),
        create_summary(),
    )

    assert "Do NOT introduce numerical scores." in prompt


def test_prompt_forbids_invented_information():
    prompt = build_advanced_debate_analysis_prompt(
        create_performance(),
        create_summary(),
    )

    assert "Do NOT invent evidence, examples, statistics, or events." in prompt


def test_prompt_forbids_fact_checking():
    prompt = build_advanced_debate_analysis_prompt(
        create_performance(),
        create_summary(),
    )

    assert "Do NOT fact-check the debate." in prompt


def test_prompt_requires_json_structure():
    prompt = build_advanced_debate_analysis_prompt(
        create_performance(),
        create_summary(),
    )

    assert '"overall_interpretation": "string"' in prompt
    assert '"cross_dimension_patterns": ["string"]' in prompt
    assert '"round_patterns": ["string"]' in prompt
    assert '"key_insights": ["string"]' in prompt


def test_prompt_rejects_none_performance():
    summary = create_summary()

    try:
        build_advanced_debate_analysis_prompt(None, summary)
    except ValueError as exc:
        assert str(exc) == "Debate performance cannot be None."
    else:
        raise AssertionError("Expected ValueError.")


def test_prompt_rejects_none_summary():
    performance = create_performance()

    try:
        build_advanced_debate_analysis_prompt(performance, None)
    except ValueError as exc:
        assert str(exc) == "Performance summary cannot be None."
    else:
        raise AssertionError("Expected ValueError.")