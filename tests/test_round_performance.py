import pytest

from debate_arena.debate.round_performance import (
    RoundPerformance,
)


def test_round_performance_creation() -> None:
    performance = RoundPerformance(
        round=1,
        argument_quality="Strong central claim.",
        communication_quality="Clear and concise.",
        responsiveness="Directly addressed the opponent.",
        evidence_usage="Used a relevant example.",
        reasoning_quality="Reasoning was logically structured.",
    )

    assert performance.round == 1
    assert performance.argument_quality == (
        "Strong central claim."
    )
    assert performance.communication_quality == (
        "Clear and concise."
    )
    assert performance.responsiveness == (
        "Directly addressed the opponent."
    )
    assert performance.evidence_usage == (
        "Used a relevant example."
    )
    assert performance.reasoning_quality == (
        "Reasoning was logically structured."
    )


def test_round_performance_strips_whitespace() -> None:
    performance = RoundPerformance(
        round=1,
        argument_quality="  Strong claim.  ",
        communication_quality="  Clear.  ",
        responsiveness="  Direct response.  ",
        evidence_usage="  Good example.  ",
        reasoning_quality="  Logical reasoning.  ",
    )

    assert performance.argument_quality == "Strong claim."
    assert performance.communication_quality == "Clear."
    assert performance.responsiveness == "Direct response."
    assert performance.evidence_usage == "Good example."
    assert performance.reasoning_quality == "Logical reasoning."


def test_round_must_be_at_least_one() -> None:
    with pytest.raises(ValueError):
        RoundPerformance(
            round=0,
            argument_quality="Good.",
            communication_quality="Clear.",
            responsiveness="Direct.",
            evidence_usage="Good.",
            reasoning_quality="Logical.",
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "argument_quality",
        "communication_quality",
        "responsiveness",
        "evidence_usage",
        "reasoning_quality",
    ],
)
def test_performance_fields_cannot_be_empty(
    field_name: str,
) -> None:
    values = {
        "argument_quality": "Good.",
        "communication_quality": "Clear.",
        "responsiveness": "Direct.",
        "evidence_usage": "Good.",
        "reasoning_quality": "Logical.",
    }

    values[field_name] = "   "

    with pytest.raises(ValueError):
        RoundPerformance(
            round=1,
            **values,
        )