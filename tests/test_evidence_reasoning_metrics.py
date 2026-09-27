import pytest

from debate_arena.debate.evidence_reasoning_metrics import (
    EvidenceReasoningMetrics,
)


def test_metrics_store_values():
    metrics = EvidenceReasoningMetrics(
        total_arguments=3,
        evidence_arguments=2,
        reasoning_arguments=3,
        evidence_coverage=2 / 3,
        reasoning_coverage=1.0,
    )

    assert metrics.total_arguments == 3
    assert metrics.evidence_arguments == 2
    assert metrics.reasoning_arguments == 3

    assert metrics.evidence_coverage == pytest.approx(
        2 / 3
    )

    assert metrics.reasoning_coverage == 1.0


def test_zero_arguments_are_allowed():
    metrics = EvidenceReasoningMetrics(
        total_arguments=0,
        evidence_arguments=0,
        reasoning_arguments=0,
        evidence_coverage=0.0,
        reasoning_coverage=0.0,
    )

    assert metrics.total_arguments == 0
    assert metrics.evidence_arguments == 0
    assert metrics.reasoning_arguments == 0
    assert metrics.evidence_coverage == 0.0
    assert metrics.reasoning_coverage == 0.0


def test_negative_total_arguments_are_rejected():
    with pytest.raises(
        ValueError,
        match="Total arguments cannot be negative",
    ):
        EvidenceReasoningMetrics(
            total_arguments=-1,
            evidence_arguments=0,
            reasoning_arguments=0,
            evidence_coverage=0.0,
            reasoning_coverage=0.0,
        )


def test_negative_evidence_arguments_are_rejected():
    with pytest.raises(
        ValueError,
        match="Evidence argument count cannot be negative",
    ):
        EvidenceReasoningMetrics(
            total_arguments=2,
            evidence_arguments=-1,
            reasoning_arguments=0,
            evidence_coverage=0.0,
            reasoning_coverage=0.0,
        )


def test_negative_reasoning_arguments_are_rejected():
    with pytest.raises(
        ValueError,
        match="Reasoning argument count cannot be negative",
    ):
        EvidenceReasoningMetrics(
            total_arguments=2,
            evidence_arguments=0,
            reasoning_arguments=-1,
            evidence_coverage=0.0,
            reasoning_coverage=0.0,
        )


def test_evidence_arguments_cannot_exceed_total():
    with pytest.raises(
        ValueError,
        match="Evidence argument count cannot exceed",
    ):
        EvidenceReasoningMetrics(
            total_arguments=2,
            evidence_arguments=3,
            reasoning_arguments=0,
            evidence_coverage=1.0,
            reasoning_coverage=0.0,
        )


def test_reasoning_arguments_cannot_exceed_total():
    with pytest.raises(
        ValueError,
        match="Reasoning argument count cannot exceed",
    ):
        EvidenceReasoningMetrics(
            total_arguments=2,
            evidence_arguments=0,
            reasoning_arguments=3,
            evidence_coverage=0.0,
            reasoning_coverage=1.0,
        )


def test_evidence_coverage_must_be_between_zero_and_one():
    with pytest.raises(
        ValueError,
        match="Evidence coverage must be between 0 and 1",
    ):
        EvidenceReasoningMetrics(
            total_arguments=2,
            evidence_arguments=1,
            reasoning_arguments=1,
            evidence_coverage=1.5,
            reasoning_coverage=0.5,
        )


def test_reasoning_coverage_must_be_between_zero_and_one():
    with pytest.raises(
        ValueError,
        match="Reasoning coverage must be between 0 and 1",
    ):
        EvidenceReasoningMetrics(
            total_arguments=2,
            evidence_arguments=1,
            reasoning_arguments=1,
            evidence_coverage=0.5,
            reasoning_coverage=-0.1,
        )