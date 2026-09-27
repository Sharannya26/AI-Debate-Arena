from debate_arena.debate.debate_performance import (
    DebatePerformance,
)
from debate_arena.debate.round_performance import (
    RoundPerformance,
)


def create_round_performance(
    round_number: int,
) -> RoundPerformance:
    return RoundPerformance(
        round=round_number,
        argument_quality="Good",
        communication_quality="Clear",
        evidence_usage="Moderate",
        reasoning_quality="Strong",
        responsiveness="Responsive",
    )


def test_debate_performance_stores_round_performances():
    rounds = [
        create_round_performance(1),
        create_round_performance(2),
    ]

    performance = DebatePerformance(
        round_performances=rounds,
    )

    assert performance.round_performances == rounds


def test_debate_performance_stores_overall_dimensions():
    performance = DebatePerformance(
        argument_quality="Strong arguments.",
        communication_quality="Clear communication.",
        responsiveness="Highly responsive.",
        consistency="Mostly consistent.",
        evidence_usage="Moderate evidence usage.",
        reasoning_quality="Strong reasoning.",
    )

    assert performance.argument_quality == (
        "Strong arguments."
    )

    assert performance.communication_quality == (
        "Clear communication."
    )

    assert performance.responsiveness == (
        "Highly responsive."
    )

    assert performance.consistency == (
        "Mostly consistent."
    )

    assert performance.evidence_usage == (
        "Moderate evidence usage."
    )

    assert performance.reasoning_quality == (
        "Strong reasoning."
    )


def test_debate_performance_cleans_moment_lists():
    performance = DebatePerformance(
        strongest_moments=[
            "  Strong rebuttal  ",
            "",
            "Clear example",
        ],
        weakest_moments=[
            "  Weak evidence  ",
            "",
        ],
        coaching_priorities=[
            "  Add more evidence  ",
            "",
            "Improve reasoning",
        ],
    )

    assert performance.strongest_moments == [
        "Strong rebuttal",
        "Clear example",
    ]

    assert performance.weakest_moments == [
        "Weak evidence",
    ]

    assert performance.coaching_priorities == [
        "Add more evidence",
        "Improve reasoning",
    ]


def test_debate_performance_defaults_to_empty_lists():
    performance = DebatePerformance()

    assert performance.round_performances == []
    assert performance.strongest_moments == []
    assert performance.weakest_moments == []
    assert performance.coaching_priorities == []


def test_debate_performance_strips_overall_dimensions():
    performance = DebatePerformance(
        argument_quality="  Strong  ",
        communication_quality="  Clear  ",
        responsiveness="  Responsive  ",
        consistency="  Consistent  ",
        evidence_usage="  Strong evidence  ",
        reasoning_quality="  Strong reasoning  ",
    )

    assert performance.argument_quality == "Strong"
    assert performance.communication_quality == "Clear"
    assert performance.responsiveness == "Responsive"
    assert performance.consistency == "Consistent"
    assert performance.evidence_usage == "Strong evidence"
    assert performance.reasoning_quality == "Strong reasoning"