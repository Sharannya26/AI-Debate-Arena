import pytest

from debate_arena.debate.evidence_analysis import (
    EvidenceAnalysis,
)


def test_evidence_analysis_stores_values():
    analysis = EvidenceAnalysis(
        evidence_quality="Strong evidence usage.",
        reasoning_quality="Clear reasoning.",
        evidence_points=[
            "Referenced educational benefits.",
        ],
        missing_evidence=[
            "No statistical evidence was provided.",
        ],
        reasoning_points=[
            "Connected educational access to the main claim.",
        ],
        reasoning_gaps=[
            "Did not explain the size of the claimed benefit.",
        ],
    )

    assert (
        analysis.evidence_quality
        == "Strong evidence usage."
    )

    assert (
        analysis.reasoning_quality
        == "Clear reasoning."
    )

    assert analysis.evidence_points == [
        "Referenced educational benefits.",
    ]

    assert analysis.missing_evidence == [
        "No statistical evidence was provided.",
    ]

    assert analysis.reasoning_points == [
        "Connected educational access to the main claim.",
    ]

    assert analysis.reasoning_gaps == [
        "Did not explain the size of the claimed benefit.",
    ]


def test_evidence_analysis_strips_whitespace():
    analysis = EvidenceAnalysis(
        evidence_quality="  Strong evidence.  ",
        reasoning_quality="  Clear reasoning.  ",
        evidence_points=[
            "  Evidence point  ",
            "",
            "   ",
        ],
        missing_evidence=[
            "  Missing evidence  ",
            "",
        ],
        reasoning_points=[
            "  Reasoning point  ",
        ],
        reasoning_gaps=[
            "  Reasoning gap  ",
            "",
        ],
    )

    assert (
        analysis.evidence_quality
        == "Strong evidence."
    )

    assert (
        analysis.reasoning_quality
        == "Clear reasoning."
    )

    assert analysis.evidence_points == [
        "Evidence point",
    ]

    assert analysis.missing_evidence == [
        "Missing evidence",
    ]

    assert analysis.reasoning_points == [
        "Reasoning point",
    ]

    assert analysis.reasoning_gaps == [
        "Reasoning gap",
    ]


def test_empty_evidence_quality_is_rejected():
    with pytest.raises(
        ValueError,
        match="Evidence quality cannot be empty",
    ):
        EvidenceAnalysis(
            evidence_quality="   ",
            reasoning_quality="Clear reasoning.",
        )


def test_empty_reasoning_quality_is_rejected():
    with pytest.raises(
        ValueError,
        match="Reasoning quality cannot be empty",
    ):
        EvidenceAnalysis(
            evidence_quality="Strong evidence.",
            reasoning_quality="   ",
        )


def test_empty_lists_are_allowed():
    analysis = EvidenceAnalysis(
        evidence_quality="No evidence identified.",
        reasoning_quality="No reasoning identified.",
    )

    assert analysis.evidence_points == []
    assert analysis.missing_evidence == []
    assert analysis.reasoning_points == []
    assert analysis.reasoning_gaps == []