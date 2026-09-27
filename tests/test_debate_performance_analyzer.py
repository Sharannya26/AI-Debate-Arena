import pytest

from debate_arena.debate.debate_performance import (
    DebatePerformance,
)
from debate_arena.debate.debate_performance_analyzer import (
    DebatePerformanceAnalyzer,
)
from debate_arena.debate.round_performance import (
    RoundPerformance,
)


def create_round_performance(
    round_number: int,
) -> RoundPerformance:
    return RoundPerformance(
        round=round_number,
        argument_quality="Strong",
        communication_quality="Clear",
        evidence_usage="Moderate",
        reasoning_quality="Strong",
        responsiveness="Responsive",
    )


def create_analyzer() -> DebatePerformanceAnalyzer:
    return DebatePerformanceAnalyzer()


def test_analyzer_combines_all_performance_dimensions():
    analyzer = create_analyzer()

    rounds = [
        create_round_performance(1),
        create_round_performance(2),
    ]

    result = analyzer.analyze(
        round_performances=rounds,
        argument_quality="Strong arguments.",
        communication_quality="Clear communication.",
        responsiveness="Highly responsive.",
        consistency="Mostly consistent.",
        evidence_usage="Moderate evidence usage.",
        reasoning_quality="Strong reasoning.",
    )

    assert isinstance(result, DebatePerformance)

    assert result.round_performances == rounds
    assert result.argument_quality == "Strong arguments."
    assert result.communication_quality == (
        "Clear communication."
    )
    assert result.responsiveness == "Highly responsive."
    assert result.consistency == "Mostly consistent."
    assert result.evidence_usage == (
        "Moderate evidence usage."
    )
    assert result.reasoning_quality == "Strong reasoning."


def test_analyzer_preserves_insight_lists():
    analyzer = create_analyzer()

    result = analyzer.analyze(
        round_performances=[
            create_round_performance(1),
        ],
        argument_quality="Strong",
        communication_quality="Clear",
        responsiveness="Responsive",
        consistency="Consistent",
        evidence_usage="Moderate",
        reasoning_quality="Strong",
        strongest_moments=[
            "Strong rebuttal",
            "Clear example",
        ],
        weakest_moments=[
            "Weak evidence",
        ],
        coaching_priorities=[
            "Use more evidence",
            "Improve reasoning",
        ],
    )

    assert result.strongest_moments == [
        "Strong rebuttal",
        "Clear example",
    ]

    assert result.weakest_moments == [
        "Weak evidence",
    ]

    assert result.coaching_priorities == [
        "Use more evidence",
        "Improve reasoning",
    ]


def test_analyzer_defaults_optional_lists_to_empty():
    analyzer = create_analyzer()

    result = analyzer.analyze(
        round_performances=[],
        argument_quality="Strong",
        communication_quality="Clear",
        responsiveness="Responsive",
        consistency="Consistent",
        evidence_usage="Moderate",
        reasoning_quality="Strong",
    )

    assert result.strongest_moments == []
    assert result.weakest_moments == []
    assert result.coaching_priorities == []


def test_analyzer_rejects_none_round_performances():
    analyzer = create_analyzer()

    with pytest.raises(
        ValueError,
        match="Round performances cannot be None",
    ):
        analyzer.analyze(
            round_performances=None,
            argument_quality="Strong",
            communication_quality="Clear",
            responsiveness="Responsive",
            consistency="Consistent",
            evidence_usage="Moderate",
            reasoning_quality="Strong",
        )


def test_analyzer_rejects_none_round_performance():
    analyzer = create_analyzer()

    with pytest.raises(
        ValueError,
        match="Round performances cannot contain None",
    ):
        analyzer.analyze(
            round_performances=[
                create_round_performance(1),
                None,
            ],
            argument_quality="Strong",
            communication_quality="Clear",
            responsiveness="Responsive",
            consistency="Consistent",
            evidence_usage="Moderate",
            reasoning_quality="Strong",
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "argument_quality",
        "communication_quality",
        "responsiveness",
        "consistency",
        "evidence_usage",
        "reasoning_quality",
    ],
)
def test_analyzer_rejects_none_required_dimension(
    field_name: str,
):
    analyzer = create_analyzer()

    kwargs = {
        "round_performances": [
            create_round_performance(1),
        ],
        "argument_quality": "Strong",
        "communication_quality": "Clear",
        "responsiveness": "Responsive",
        "consistency": "Consistent",
        "evidence_usage": "Moderate",
        "reasoning_quality": "Strong",
    }

    kwargs[field_name] = None

    with pytest.raises(
        ValueError,
        match="cannot be None",
    ):
        analyzer.analyze(**kwargs)