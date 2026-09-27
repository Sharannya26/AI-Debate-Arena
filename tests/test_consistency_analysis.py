import pytest

from debate_arena.debate.consistency_analysis import (
    ConsistencyAnalysis,
)


def test_consistency_analysis_stores_values():
    analysis = ConsistencyAnalysis(
        consistency="Mostly consistent.",
        consistent_points=[
            "Maintained the same position.",
            "Continued supporting responsible usage.",
        ],
        inconsistent_points=[
            "Changed position in round three.",
        ],
    )

    assert analysis.consistency == "Mostly consistent."

    assert analysis.consistent_points == [
        "Maintained the same position.",
        "Continued supporting responsible usage.",
    ]

    assert analysis.inconsistent_points == [
        "Changed position in round three.",
    ]


def test_consistency_analysis_strips_whitespace():
    analysis = ConsistencyAnalysis(
        consistency="  Mostly consistent.  ",
        consistent_points=[
            "  Same position  ",
            "",
            "   ",
        ],
        inconsistent_points=[
            "  Changed position  ",
            "",
        ],
    )

    assert analysis.consistency == "Mostly consistent."

    assert analysis.consistent_points == [
        "Same position",
    ]

    assert analysis.inconsistent_points == [
        "Changed position",
    ]


def test_empty_consistency_is_rejected():
    with pytest.raises(ValueError, match="Consistency cannot be empty"):
        ConsistencyAnalysis(
            consistency="   ",
        )