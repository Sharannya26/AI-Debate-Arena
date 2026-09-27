import pytest

from debate_arena.debate.moment_analyzer import MomentAnalyzer
from debate_arena.debate.moment_analysis import MomentAnalysis
from debate_arena.debate.round_performance import RoundPerformance


def create_round(
    round_number: int,
    argument_quality: str = "Moderate argument quality.",
    communication_quality: str = "Moderate communication quality.",
    evidence_usage: str = "Moderate evidence usage.",
    reasoning_quality: str = "Moderate reasoning quality.",
    responsiveness: str | None = "Partially responsive.",
) -> RoundPerformance:
    return RoundPerformance(
        round=round_number,
        argument_quality=argument_quality,
        communication_quality=communication_quality,
        evidence_usage=evidence_usage,
        reasoning_quality=reasoning_quality,
        responsiveness=responsiveness,
    )


def test_detects_strong_argument_moment():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            argument_quality="Strong argument quality.",
        )
    ]

    strongest, weakest = analyzer.analyze(rounds)

    assert (
        "Round 1: Strong argument quality — "
        "Strong argument quality."
    ) in strongest

    assert weakest == []


def test_detects_weak_argument_moment():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            argument_quality="Limited argument quality.",
        )
    ]

    strongest, weakest = analyzer.analyze(rounds)

    assert strongest == []

    assert (
        "Round 1: Weak argument quality — "
        "Limited argument quality."
    ) in weakest


def test_detects_strong_communication():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            communication_quality="Excellent communication.",
        )
    ]

    strongest, _ = analyzer.analyze(rounds)

    assert any(
        "Strong communication quality" in moment
        for moment in strongest
    )


def test_detects_weak_evidence_usage():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            evidence_usage="Limited evidence usage.",
        )
    ]

    _, weakest = analyzer.analyze(rounds)

    assert any(
        "Weak evidence usage" in moment
        for moment in weakest
    )


def test_detects_strong_reasoning():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            reasoning_quality="Strong reasoning structure.",
        )
    ]

    strongest, _ = analyzer.analyze(rounds)

    assert any(
        "Strong reasoning quality" in moment
        for moment in strongest
    )


def test_detects_weak_responsiveness():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            responsiveness="Not responsive to the opposing point.",
        )
    ]

    _, weakest = analyzer.analyze(rounds)

    assert any(
        "Weak responsiveness" in moment
        for moment in weakest
    )


def test_detects_multiple_moments_across_rounds():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            argument_quality="Strong argument quality.",
        ),
        create_round(
            2,
            evidence_usage="Limited evidence usage.",
        ),
        create_round(
            3,
            reasoning_quality="Excellent reasoning.",
        ),
    ]

    strongest, weakest = analyzer.analyze(rounds)

    assert len(strongest) >= 2
    assert len(weakest) >= 1


def test_ignores_moderate_values():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            argument_quality="Moderate argument quality.",
            communication_quality="Clear communication.",
            evidence_usage="Moderate evidence usage.",
            reasoning_quality="Moderate reasoning.",
        )
    ]

    strongest, weakest = analyzer.analyze(rounds)

    assert strongest == []
    assert weakest == []


def test_ignores_missing_responsiveness():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            responsiveness=None,
        )
    ]

    strongest, weakest = analyzer.analyze(rounds)

    assert isinstance(strongest, list)
    assert isinstance(weakest, list)


def test_handles_empty_input():
    analyzer = MomentAnalyzer()

    strongest, weakest = analyzer.analyze([])

    assert strongest == []
    assert weakest == []


def test_rejects_none_input():
    analyzer = MomentAnalyzer()

    with pytest.raises(
        ValueError,
        match="Round performances cannot be None",
    ):
        analyzer.analyze(None)


def test_rejects_none_round_performance():
    analyzer = MomentAnalyzer()

    with pytest.raises(
        ValueError,
        match="Round performances cannot contain None",
    ):
        analyzer.analyze([None])


def test_detects_multiple_dimensions_in_same_round():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            argument_quality="Strong argument quality.",
            communication_quality="Excellent communication.",
            reasoning_quality="Strong reasoning.",
        )
    ]

    strongest, _ = analyzer.analyze(rounds)

    assert len(strongest) == 3

def test_structured_analysis_returns_moment_analysis():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            argument_quality="Strong argument quality.",
            evidence_usage="Limited evidence usage.",
        )
    ]

    analysis = analyzer.analyze_structured(rounds)

    assert isinstance(analysis, MomentAnalysis)

    assert analysis.strongest_moments == [
        "Round 1: Strong argument quality — Strong argument quality."
    ]

    assert analysis.weakest_moments == [
        "Round 1: Weak evidence usage — Limited evidence usage."
    ]


def test_structured_analysis_handles_empty_input():
    analyzer = MomentAnalyzer()

    analysis = analyzer.analyze_structured([])

    assert isinstance(analysis, MomentAnalysis)
    assert analysis.strongest_moments == []
    assert analysis.weakest_moments == []
    assert analysis.key_insights == []


def test_structured_analysis_detects_multiple_dimensions():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            2,
            argument_quality="Excellent argument quality.",
            communication_quality="Strong communication.",
            reasoning_quality="Strong reasoning.",
        )
    ]

    analysis = analyzer.analyze_structured(rounds)

    assert len(analysis.strongest_moments) == 3

    assert any(
        "argument quality" in moment
        for moment in analysis.strongest_moments
    )

    assert any(
        "communication quality" in moment
        for moment in analysis.strongest_moments
    )

    assert any(
        "reasoning quality" in moment
        for moment in analysis.strongest_moments
    )


def test_structured_analysis_ignores_moderate_values():
    analyzer = MomentAnalyzer()

    rounds = [
        create_round(
            1,
            argument_quality="Moderate argument quality.",
            communication_quality="Clear communication.",
            evidence_usage="Moderate evidence usage.",
            reasoning_quality="Moderate reasoning.",
        )
    ]

    analysis = analyzer.analyze_structured(rounds)

    assert analysis.strongest_moments == []
    assert analysis.weakest_moments == []


def test_structured_analysis_rejects_none_input():
    analyzer = MomentAnalyzer()

    try:
        analyzer.analyze_structured(None)
    except ValueError as error:
        assert str(error) == (
            "Round performances cannot be None."
        )
    else:
        raise AssertionError(
            "Expected ValueError."
        )