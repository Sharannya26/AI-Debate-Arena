import pytest

from debate_arena.debate.performance_dimension_aggregator import (
    PerformanceDimensionAggregator,
)
from debate_arena.debate.round_performance import (
    RoundPerformance,
)


def create_round_performance(
    round_number: int,
    argument_quality: str = "Strong",
    communication_quality: str = "Clear",
    evidence_usage: str = "Moderate evidence usage.",
    reasoning_quality: str = "Strong reasoning structure.",
    responsiveness: str = "Highly responsive.",
) -> RoundPerformance:
    return RoundPerformance(
        round=round_number,
        argument_quality=argument_quality,
        communication_quality=communication_quality,
        evidence_usage=evidence_usage,
        reasoning_quality=reasoning_quality,
        responsiveness=responsiveness,
    )


def test_aggregate_detects_improvement():
    aggregator = PerformanceDimensionAggregator()

    result = aggregator.aggregate(
        [
            "Limited evidence usage.",
            "Moderate evidence usage.",
            "Strong evidence usage.",
        ],
        "evidence usage",
    )

    assert result == (
        "Evidence usage improved across the debate."
    )


def test_aggregate_detects_decline():
    aggregator = PerformanceDimensionAggregator()

    result = aggregator.aggregate(
        [
            "Strong reasoning structure.",
            "Moderate reasoning structure.",
            "Limited reasoning structure.",
        ],
        "reasoning quality",
    )

    assert result == (
        "Reasoning quality declined across the debate."
    )


def test_aggregate_detects_consistency():
    aggregator = PerformanceDimensionAggregator()

    result = aggregator.aggregate(
        [
            "Strong evidence usage.",
            "Strong evidence usage.",
            "Strong evidence usage.",
        ],
        "evidence usage",
    )

    assert result == (
        "Evidence usage remained consistently "
        "strong evidence usage."
    )


def test_aggregate_detects_variation():
    aggregator = PerformanceDimensionAggregator()

    result = aggregator.aggregate(
        [
            "Strong evidence usage.",
            "Limited evidence usage.",
            "Strong evidence usage.",
        ],
        "evidence usage",
    )

    assert result == (
        "Evidence usage varied across the debate."
    )


def test_aggregate_returns_single_value_unchanged():
    aggregator = PerformanceDimensionAggregator()

    result = aggregator.aggregate(
        ["Strong evidence usage."],
        "evidence usage",
    )

    assert result == "Strong evidence usage."


def test_aggregate_handles_empty_values():
    aggregator = PerformanceDimensionAggregator()

    result = aggregator.aggregate(
        [],
        "evidence usage",
    )

    assert result == (
        "No evidence usage data available."
    )


def test_aggregate_ignores_blank_values():
    aggregator = PerformanceDimensionAggregator()

    result = aggregator.aggregate(
        [
            "",
            "  ",
            "Strong evidence usage.",
        ],
        "evidence usage",
    )

    assert result == "Strong evidence usage."


def test_aggregate_round_performances_returns_all_dimensions():
    aggregator = PerformanceDimensionAggregator()

    rounds = [
        create_round_performance(1),
        create_round_performance(2),
    ]

    result = aggregator.aggregate_round_performances(
        rounds
    )

    assert set(result.keys()) == {
        "argument quality",
        "communication quality",
        "evidence usage",
        "reasoning quality",
        "responsiveness",
    }


def test_aggregate_round_performances_handles_empty_input():
    aggregator = PerformanceDimensionAggregator()

    assert (
        aggregator.aggregate_round_performances([])
        == {}
    )


def test_aggregate_round_performances_handles_missing_responsiveness():
    aggregator = PerformanceDimensionAggregator()

    rounds = [
        create_round_performance(
            1,
            responsiveness=None,
        ),
        create_round_performance(
            2,
            responsiveness=None,
        ),
    ]

    result = aggregator.aggregate_round_performances(
        rounds
    )

    assert (
        result["responsiveness"]
        == "No responsiveness data available."
    )


def test_quality_score_recognizes_quality_levels():
    aggregator = PerformanceDimensionAggregator()

    assert aggregator._quality_score("Limited evidence") == 2
    assert aggregator._quality_score("Moderate evidence") == 3
    assert aggregator._quality_score("Strong evidence") == 4
    assert aggregator._quality_score("Highly responsive") == 5


def test_aggregate_rejects_none_values():
    aggregator = PerformanceDimensionAggregator()

    with pytest.raises(
        ValueError,
        match="Dimension values cannot be None",
    ):
        aggregator.aggregate(
            None,
            "evidence usage",
        )


def test_aggregate_rejects_empty_dimension_name():
    aggregator = PerformanceDimensionAggregator()

    with pytest.raises(
        ValueError,
        match="Dimension name cannot be empty",
    ):
        aggregator.aggregate(
            ["Strong evidence"],
            "",
        )


def test_aggregate_round_performances_rejects_none():
    aggregator = PerformanceDimensionAggregator()

    with pytest.raises(
        ValueError,
        match="Round performances cannot be None",
    ):
        aggregator.aggregate_round_performances(None)

def test_aggregate_round_performances_real_argument_quality():
    aggregator = PerformanceDimensionAggregator()

    rounds = [
        create_round_performance(
            1,
            argument_quality=(
                "Argument contains identifiable weaknesses."
            ),
        ),
        create_round_performance(
            2,
            argument_quality=(
                "Argument contains a clear claim "
                "supported by reasoning."
            ),
        ),
        create_round_performance(
            3,
            argument_quality=(
                "Argument contains a clear claim "
                "supported by reasoning."
            ),
        ),
    ]

    result = aggregator.aggregate_round_performances(
        rounds
    )

    assert result["argument quality"] == (
        "Argument quality improved across the debate."
    )


def test_aggregate_round_performances_real_evidence_usage():
    aggregator = PerformanceDimensionAggregator()

    rounds = [
        create_round_performance(
            1,
            evidence_usage=(
                "The argument used 0 identified "
                "piece(s) of evidence."
            ),
        ),
        create_round_performance(
            2,
            evidence_usage=(
                "The argument used 1 identified "
                "piece(s) of evidence."
            ),
        ),
        create_round_performance(
            3,
            evidence_usage=(
                "The argument used 2 identified "
                "piece(s) of evidence."
            ),
        ),
    ]

    result = aggregator.aggregate_round_performances(
        rounds
    )

    assert result["evidence usage"] == (
        "Evidence usage improved across the debate."
    )


def test_aggregate_round_performances_real_reasoning_quality():
    aggregator = PerformanceDimensionAggregator()

    rounds = [
        create_round_performance(
            1,
            reasoning_quality=(
                "No explicit reasoning structure "
                "was identified."
            ),
        ),
        create_round_performance(
            2,
            reasoning_quality=(
                "Reasoning was identified in the argument."
            ),
        ),
        create_round_performance(
            3,
            reasoning_quality=(
                "Reasoning was identified in the argument."
            ),
        ),
    ]

    result = aggregator.aggregate_round_performances(
        rounds
    )

    assert result["reasoning quality"] == (
        "Reasoning quality improved across the debate."
    )


def test_aggregate_round_performances_real_communication_quality():
    aggregator = PerformanceDimensionAggregator()

    rounds = [
        create_round_performance(
            1,
            communication_quality=(
                "Speech was delivered at a fast pace."
            ),
        ),
        create_round_performance(
            2,
            communication_quality=(
                "Speech was delivered at a moderate pace."
            ),
        ),
        create_round_performance(
            3,
            communication_quality=(
                "Speech was delivered at a fast pace."
            ),
        ),
    ]

    result = aggregator.aggregate_round_performances(
        rounds
    )

    assert result["communication quality"] == (
        "Communication quality varied across the debate."
    )
    
def test_aggregate_round_performances_consistent_argument_quality_is_natural():
    aggregator = PerformanceDimensionAggregator()

    rounds = [
        create_round_performance(
            1,
            argument_quality=(
                "Argument contains identifiable weaknesses."
            ),
        ),
        create_round_performance(
            2,
            argument_quality=(
                "Argument contains identifiable weaknesses."
            ),
        ),
        create_round_performance(
            3,
            argument_quality=(
                "Argument contains identifiable weaknesses."
            ),
        ),
    ]

    result = aggregator.aggregate_round_performances(
        rounds
    )

    assert result["argument quality"] == (
        "Argument quality remained consistently "
        "weak across the debate."
    )


def test_aggregate_round_performances_consistent_responsiveness_is_natural():
    aggregator = PerformanceDimensionAggregator()

    rounds = [
        create_round_performance(
            1,
            responsiveness="Minimally responsive.",
        ),
        create_round_performance(
            2,
            responsiveness="Minimally responsive.",
        ),
        create_round_performance(
            3,
            responsiveness="Minimally responsive.",
        ),
    ]

    result = aggregator.aggregate_round_performances(
        rounds
    )

    assert result["responsiveness"] == (
        "Responsiveness remained consistently "
        "limited across the debate."
    )


