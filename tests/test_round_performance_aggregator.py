import pytest

from debate_arena.debate.round_performance import (
    RoundPerformance,
)
from debate_arena.debate.round_performance_aggregator import (
    RoundPerformanceAggregator,
)


def create_round_performance(
    round_number: int,
    argument_quality: str = "Strong",
    communication_quality: str = "Clear",
    evidence_usage: str = "Moderate",
    reasoning_quality: str = "Strong",
    responsiveness: str = "Responsive",
) -> RoundPerformance:
    return RoundPerformance(
        round=round_number,
        argument_quality=argument_quality,
        communication_quality=communication_quality,
        evidence_usage=evidence_usage,
        reasoning_quality=reasoning_quality,
        responsiveness=responsiveness,
    )


def create_aggregator() -> RoundPerformanceAggregator:
    return RoundPerformanceAggregator()


def test_aggregator_sorts_rounds_by_round_number():
    aggregator = create_aggregator()

    performances = [
        create_round_performance(3),
        create_round_performance(1),
        create_round_performance(2),
    ]

    result = aggregator.aggregate(performances)

    assert [item.round for item in result] == [1, 2, 3]


def test_aggregator_preserves_round_performance_objects():
    aggregator = create_aggregator()

    first = create_round_performance(1)
    second = create_round_performance(2)

    result = aggregator.aggregate([second, first])

    assert result[0] is first
    assert result[1] is second


def test_strongest_round_returns_latest_round_for_now():
    aggregator = create_aggregator()

    performances = [
        create_round_performance(1),
        create_round_performance(2),
        create_round_performance(3),
    ]

    result = aggregator.strongest_round(performances)

    assert result is not None
    assert result.round == 3


def test_weakest_round_returns_earliest_round_for_now():
    aggregator = create_aggregator()

    performances = [
        create_round_performance(1),
        create_round_performance(2),
        create_round_performance(3),
    ]

    result = aggregator.weakest_round(performances)

    assert result is not None
    assert result.round == 1


def test_strongest_round_returns_none_for_empty_input():
    aggregator = create_aggregator()

    assert aggregator.strongest_round([]) is None


def test_weakest_round_returns_none_for_empty_input():
    aggregator = create_aggregator()

    assert aggregator.weakest_round([]) is None


def test_dimension_values_returns_ordered_values():
    aggregator = create_aggregator()

    performances = [
        create_round_performance(
            2,
            communication_quality="Strong",
        ),
        create_round_performance(
            1,
            communication_quality="Moderate",
        ),
        create_round_performance(
            3,
            communication_quality="Excellent",
        ),
    ]

    result = aggregator.dimension_values(
        performances,
        "communication_quality",
    )

    assert result == [
        "Moderate",
        "Strong",
        "Excellent",
    ]


def test_dimension_values_supports_all_dimensions():
    aggregator = create_aggregator()

    performance = create_round_performance(1)

    for dimension in (
        "argument_quality",
        "communication_quality",
        "evidence_usage",
        "reasoning_quality",
        "responsiveness",
    ):
        result = aggregator.dimension_values(
            [performance],
            dimension,
        )

        assert len(result) == 1


def test_aggregator_rejects_none_input():
    aggregator = create_aggregator()

    with pytest.raises(
        ValueError,
        match="Round performances cannot be None",
    ):
        aggregator.aggregate(None)


def test_aggregator_rejects_none_inside_list():
    aggregator = create_aggregator()

    with pytest.raises(
        ValueError,
        match="Round performances cannot contain None",
    ):
        aggregator.aggregate(
            [
                create_round_performance(1),
                None,
            ]
        )


def test_dimension_values_rejects_unsupported_dimension():
    aggregator = create_aggregator()

    with pytest.raises(
        ValueError,
        match="Unsupported performance dimension",
    ):
        aggregator.dimension_values(
            [create_round_performance(1)],
            "invalid_dimension",
        )