import pytest

from debate_arena.debate.semantic_performance_analysis import (
    SemanticPerformanceAnalysis,
)


def test_creates_semantic_performance_analysis():
    analysis = SemanticPerformanceAnalysis(
        overall_interpretation="Performance improved.",
        strengths_interpretation="Reasoning was strong.",
        weaknesses_interpretation="Evidence was inconsistent.",
        coaching_interpretation="Use more concrete evidence.",
        key_insights=[
            "Reasoning improved across rounds.",
        ],
    )

    assert (
        analysis.overall_interpretation
        == "Performance improved."
    )

    assert analysis.key_insights == [
        "Reasoning improved across rounds."
    ]


def test_strips_text_fields():
    analysis = SemanticPerformanceAnalysis(
        overall_interpretation="  Performance improved.  ",
        strengths_interpretation="  Strong reasoning. ",
        weaknesses_interpretation=" Evidence gaps. ",
        coaching_interpretation=" Use examples. ",
    )

    assert (
        analysis.overall_interpretation
        == "Performance improved."
    )

    assert (
        analysis.strengths_interpretation
        == "Strong reasoning."
    )

    assert (
        analysis.weaknesses_interpretation
        == "Evidence gaps."
    )

    assert (
        analysis.coaching_interpretation
        == "Use examples."
    )


def test_filters_blank_key_insights():
    analysis = SemanticPerformanceAnalysis(
        overall_interpretation="Performance improved.",
        key_insights=[
            "Reasoning improved.",
            "",
            "  ",
            "Evidence improved.",
        ],
    )

    assert analysis.key_insights == [
        "Reasoning improved.",
        "Evidence improved.",
    ]


def test_rejects_empty_overall_interpretation():
    with pytest.raises(
        ValueError,
        match="Overall interpretation cannot be empty",
    ):
        SemanticPerformanceAnalysis(
            overall_interpretation="   "
        )