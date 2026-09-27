import pytest

from debate_arena.debate.semantic_moment_analysis import (
    SemanticMomentAnalysis,
)


def test_valid_semantic_moment_analysis():
    analysis = SemanticMomentAnalysis(
        strongest_interpretation=(
            "The strongest moments showed clear argument structure."
        ),
        weakest_interpretation=(
            "The weakest moments showed limited evidence support."
        ),
        key_insights=[
            "Argument structure was clearer in later rounds.",
        ],
    )

    assert (
        analysis.strongest_interpretation
        == "The strongest moments showed clear argument structure."
    )

    assert (
        analysis.weakest_interpretation
        == "The weakest moments showed limited evidence support."
    )

    assert analysis.key_insights == [
        "Argument structure was clearer in later rounds."
    ]


def test_whitespace_is_stripped():
    analysis = SemanticMomentAnalysis(
        strongest_interpretation="  Strong moments.  ",
        weakest_interpretation="  Weak moments.  ",
        key_insights=[
            "  Insight one.  ",
            "",
            "   ",
        ],
    )

    assert (
        analysis.strongest_interpretation
        == "Strong moments."
    )

    assert (
        analysis.weakest_interpretation
        == "Weak moments."
    )

    assert analysis.key_insights == [
        "Insight one."
    ]


def test_empty_strongest_interpretation_rejected():
    with pytest.raises(
        ValueError,
        match="Strongest interpretation cannot be empty.",
    ):
        SemanticMomentAnalysis(
            strongest_interpretation="",
            weakest_interpretation="Weak moments.",
        )


def test_empty_weakest_interpretation_rejected():
    with pytest.raises(
        ValueError,
        match="Weakest interpretation cannot be empty.",
    ):
        SemanticMomentAnalysis(
            strongest_interpretation="Strong moments.",
            weakest_interpretation="",
        )


def test_key_insights_default_to_empty_list():
    analysis = SemanticMomentAnalysis(
        strongest_interpretation="Strong moments.",
        weakest_interpretation="Weak moments.",
    )

    assert analysis.key_insights == []


def test_none_values_in_key_insights_are_filtered():
    analysis = SemanticMomentAnalysis(
        strongest_interpretation="Strong moments.",
        weakest_interpretation="Weak moments.",
        key_insights=[
            None,
            "Useful insight.",
            "",
        ],
    )

    assert analysis.key_insights == [
        "Useful insight."
    ]