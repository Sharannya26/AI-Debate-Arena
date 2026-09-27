import pytest

from debate_arena.debate.debate_performance import (
    DebatePerformance,
)
from debate_arena.debate.performance_summary_analyzer import (
    PerformanceSummaryAnalyzer,
)


def create_performance(
    strongest_moments=None,
    weakest_moments=None,
    coaching_priorities=None,
):
    return DebatePerformance(
        argument_quality="Strong",
        communication_quality="Clear",
        responsiveness="Highly responsive",
        consistency="Mostly consistent",
        evidence_usage="Moderate",
        reasoning_quality="Strong",
        strongest_moments=(
            strongest_moments
            if strongest_moments is not None
            else []
        ),
        weakest_moments=(
            weakest_moments
            if weakest_moments is not None
            else []
        ),
        coaching_priorities=(
            coaching_priorities
            if coaching_priorities is not None
            else []
        ),
    )


def test_builds_summary_with_strongest_moments():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance(
        strongest_moments=[
            "Round 2: Strong reasoning."
        ]
    )

    result = analyzer.analyze(performance)

    assert (
        result.overall_summary
        == "The debate demonstrated several "
        "notable strengths."
    )

    assert result.strongest_moments == [
        "Round 2: Strong reasoning."
    ]


def test_builds_summary_with_weakest_moments():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance(
        weakest_moments=[
            "Round 3: Weak evidence usage."
        ]
    )

    result = analyzer.analyze(performance)

    assert (
        result.overall_summary
        == "The debate identified several "
        "areas for improvement."
    )

    assert result.weakest_moments == [
        "Round 3: Weak evidence usage."
    ]


def test_builds_balanced_summary():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance(
        strongest_moments=[
            "Round 2: Strong reasoning."
        ],
        weakest_moments=[
            "Round 3: Weak evidence usage."
        ],
    )

    result = analyzer.analyze(performance)

    assert (
        result.overall_summary
        == "The debate showed a mix of "
        "performance strengths and areas "
        "for improvement."
    )


def test_builds_baseline_summary_without_moments():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance()

    result = analyzer.analyze(performance)

    assert (
        result.overall_summary
        == "The debate performance data provides "
        "a baseline for further analysis."
    )


def test_detects_improving_performance():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance()

    dimensions = {
        "evidence usage":
            "Evidence usage improved across the debate.",
        "reasoning quality":
            "Reasoning quality improved across the debate.",
        "communication quality":
            "Communication quality varied across the debate.",
    }

    result = analyzer.analyze(
        performance,
        dimensions,
    )

    assert (
        result.overall_summary
        == "Performance improved across "
        "multiple debate dimensions."
    )


def test_detects_declining_performance():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance()

    dimensions = {
        "evidence usage":
            "Evidence usage declined across the debate.",
        "reasoning quality":
            "Reasoning quality declined across the debate.",
        "communication quality":
            "Communication quality varied across the debate.",
    }

    result = analyzer.analyze(
        performance,
        dimensions,
    )

    assert (
        result.overall_summary
        == "Performance declined across "
        "multiple debate dimensions."
    )


def test_detects_variation():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance()

    dimensions = {
        "evidence usage":
            "Evidence usage varied across the debate.",
    }

    result = analyzer.analyze(
        performance,
        dimensions,
    )

    assert (
        result.overall_summary
        == "Performance varied across "
        "the debate."
    )


def test_preserves_dimension_summaries():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance()

    dimensions = {
        "evidence usage":
            "Evidence usage improved across the debate.",
        "reasoning quality":
            "Reasoning quality remained consistent.",
    }

    result = analyzer.analyze(
        performance,
        dimensions,
    )

    assert result.dimension_summaries == dimensions


def test_preserves_coaching_priorities():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance(
        coaching_priorities=[
            "Support major claims with evidence.",
            "Make logical connections explicit.",
        ]
    )

    result = analyzer.analyze(performance)

    assert result.coaching_priorities == [
        "Support major claims with evidence.",
        "Make logical connections explicit.",
    ]


def test_cleans_dimension_summaries():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance()

    dimensions = {
        " evidence usage ":
            " Evidence usage improved across the debate. ",
        "":
            "",
    }

    result = analyzer.analyze(
        performance,
        dimensions,
    )

    assert result.dimension_summaries == {
        "evidence usage":
            "Evidence usage improved across the debate."
    }


def test_rejects_none_performance():
    analyzer = PerformanceSummaryAnalyzer()

    with pytest.raises(
        ValueError,
        match="Performance cannot be None",
    ):
        analyzer.analyze(None)


def test_handles_none_dimension_summaries():
    analyzer = PerformanceSummaryAnalyzer()

    performance = create_performance()

    result = analyzer.analyze(
        performance,
        None,
    )

    assert result.dimension_summaries == {}


def test_copies_lists_without_sharing_references():
    analyzer = PerformanceSummaryAnalyzer()

    strongest = [
        "Round 1: Strong communication."
    ]

    weakest = [
        "Round 3: Weak evidence."
    ]

    priorities = [
        "Use more evidence."
    ]

    performance = create_performance(
        strongest_moments=strongest,
        weakest_moments=weakest,
        coaching_priorities=priorities,
    )

    result = analyzer.analyze(performance)

    assert result.strongest_moments == strongest
    assert result.weakest_moments == weakest
    assert result.coaching_priorities == priorities

    assert (
        result.strongest_moments
        is not performance.strongest_moments
    )

    assert (
        result.weakest_moments
        is not performance.weakest_moments
    )

    assert (
        result.coaching_priorities
        is not performance.coaching_priorities
    )