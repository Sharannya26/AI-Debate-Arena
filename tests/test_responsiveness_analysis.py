import pytest

from debate_arena.debate.responsiveness_analysis import (
    ResponsivenessAnalysis,
)


def test_creates_responsiveness_analysis():
    analysis = ResponsivenessAnalysis(
        responsiveness="Directly addresses the previous argument.",
        addressed_points=["Cost"],
        ignored_points=["Reliability"],
    )

    assert (
        analysis.responsiveness
        == "Directly addresses the previous argument."
    )
    assert analysis.addressed_points == ["Cost"]
    assert analysis.ignored_points == ["Reliability"]


def test_responsiveness_is_stripped():
    analysis = ResponsivenessAnalysis(
        responsiveness="  Direct response  ",
        addressed_points=["  Cost  "],
        ignored_points=["  Reliability  "],
    )

    assert analysis.responsiveness == "Direct response"
    assert analysis.addressed_points == ["Cost"]
    assert analysis.ignored_points == ["Reliability"]


def test_empty_responsiveness_is_rejected():
    with pytest.raises(
        ValueError,
        match="Responsiveness cannot be empty.",
    ):
        ResponsivenessAnalysis(
            responsiveness="   ",
        )


def test_empty_points_are_removed():
    analysis = ResponsivenessAnalysis(
        responsiveness="Partial response.",
        addressed_points=[
            "Cost",
            "",
            "   ",
            "Reliability",
        ],
        ignored_points=[
            "",
            "Safety",
            "   ",
        ],
    )

    assert analysis.addressed_points == [
        "Cost",
        "Reliability",
    ]

    assert analysis.ignored_points == ["Safety"]


def test_default_points_are_empty():
    analysis = ResponsivenessAnalysis(
        responsiveness="No direct response.",
    )

    assert analysis.addressed_points == []
    assert analysis.ignored_points == []