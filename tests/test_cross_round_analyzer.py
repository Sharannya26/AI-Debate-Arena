import pytest

from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis
from debate_arena.debate.cross_round_analyzer import CrossRoundAnalyzer
from debate_arena.debate.round_performance import RoundPerformance


def make_round(
    round_number: int,
    argument_quality: str = "Moderate",
    communication_quality: str = "Moderate",
    evidence_usage: str = "Moderate",
    reasoning_quality: str = "Moderate",
    responsiveness: str = "Moderate",
) -> RoundPerformance:
    return RoundPerformance(
        round=round_number,
        argument_quality=argument_quality,
        communication_quality=communication_quality,
        evidence_usage=evidence_usage,
        reasoning_quality=reasoning_quality,
        responsiveness=responsiveness,
    )


def test_analyzer_requires_round_performances():
    analyzer = CrossRoundAnalyzer()

    with pytest.raises(ValueError):
        analyzer.analyze(None)


def test_analyzer_requires_at_least_one_round():
    analyzer = CrossRoundAnalyzer()

    with pytest.raises(ValueError):
        analyzer.analyze([])


def test_analyzer_detects_improvement():
    analyzer = CrossRoundAnalyzer()

    rounds = [
        make_round(1, reasoning_quality="Limited"),
        make_round(2, reasoning_quality="Moderate"),
        make_round(3, reasoning_quality="Strong"),
    ]

    result = analyzer.analyze(rounds)

    assert isinstance(result, CrossRoundAnalysis)
    assert "Reasoning quality improved across the debate." in (
        result.improvement_patterns
    )


def test_analyzer_detects_decline():
    analyzer = CrossRoundAnalyzer()

    rounds = [
        make_round(1, communication_quality="Strong"),
        make_round(2, communication_quality="Moderate"),
        make_round(3, communication_quality="Limited"),
    ]

    result = analyzer.analyze(rounds)

    assert "Communication quality declined across the debate." in (
        result.decline_patterns
    )


def test_analyzer_detects_stability():
    analyzer = CrossRoundAnalyzer()

    rounds = [
        make_round(1, responsiveness="Strong"),
        make_round(2, responsiveness="Strong"),
        make_round(3, responsiveness="Strong"),
    ]

    result = analyzer.analyze(rounds)

    assert "Responsiveness remained stable across the debate." in (
        result.stable_patterns
    )


def test_analyzer_detects_recurring_pattern():
    analyzer = CrossRoundAnalyzer()

    rounds = [
        make_round(1, evidence_usage="Limited"),
        make_round(2, evidence_usage="Limited"),
        make_round(3, evidence_usage="Limited"),
    ]

    result = analyzer.analyze(rounds)

    assert (
        "Evidence usage remained consistently Limited across the rounds."
        in result.recurring_patterns
    )


def test_analyzer_detects_overall_improvement():
    analyzer = CrossRoundAnalyzer()

    rounds = [
        make_round(
            1,
            argument_quality="Limited",
            reasoning_quality="Limited",
        ),
        make_round(
            2,
            argument_quality="Strong",
            reasoning_quality="Strong",
        ),
    ]

    result = analyzer.analyze(rounds)

    assert result.overall_trajectory == (
        "Performance improved across the debate."
    )


def test_analyzer_detects_overall_decline():
    analyzer = CrossRoundAnalyzer()

    rounds = [
        make_round(
            1,
            argument_quality="Strong",
            reasoning_quality="Strong",
        ),
        make_round(
            2,
            argument_quality="Limited",
            reasoning_quality="Limited",
        ),
    ]

    result = analyzer.analyze(rounds)

    assert result.overall_trajectory == (
        "Performance declined across the debate."
    )


def test_analyzer_detects_mixed_changes():
    analyzer = CrossRoundAnalyzer()

    rounds = [
        make_round(
            1,
            argument_quality="Limited",
            communication_quality="Strong",
        ),
        make_round(
            2,
            argument_quality="Strong",
            communication_quality="Limited",
        ),
    ]

    result = analyzer.analyze(rounds)

    assert result.overall_trajectory == (
        "Performance showed mixed changes across the debate."
    )


def test_analyzer_orders_rounds_before_comparing():
    analyzer = CrossRoundAnalyzer()

    rounds = [
        make_round(3, reasoning_quality="Strong"),
        make_round(1, reasoning_quality="Limited"),
        make_round(2, reasoning_quality="Moderate"),
    ]

    result = analyzer.analyze(rounds)

    assert "Reasoning quality improved across the debate." in (
        result.improvement_patterns
    )


def test_analyzer_handles_single_round():
    analyzer = CrossRoundAnalyzer()

    result = analyzer.analyze(
        [make_round(1, reasoning_quality="Strong")]
    )

    assert result.improvement_patterns == []
    assert result.decline_patterns == []
    assert result.stable_patterns == []
    assert result.recurring_patterns == []
    assert result.overall_trajectory == (
        "Performance trajectory could not be determined from the available data."
    )


def test_analyzer_can_detect_multiple_dimension_patterns():
    analyzer = CrossRoundAnalyzer()

    rounds = [
        make_round(
            1,
            argument_quality="Limited",
            reasoning_quality="Limited",
            communication_quality="Strong",
        ),
        make_round(
            2,
            argument_quality="Strong",
            reasoning_quality="Strong",
            communication_quality="Limited",
        ),
    ]

    result = analyzer.analyze(rounds)

    assert "Argument quality improved across the debate." in (
        result.improvement_patterns
    )
    assert "Reasoning quality improved across the debate." in (
        result.improvement_patterns
    )
    assert "Communication quality declined across the debate." in (
        result.decline_patterns
    )