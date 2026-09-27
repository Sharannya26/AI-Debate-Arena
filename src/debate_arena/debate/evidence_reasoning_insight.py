from dataclasses import dataclass, field

from debate_arena.debate.evidence_analysis import EvidenceAnalysis
from debate_arena.debate.evidence_reasoning_metrics import (
    EvidenceReasoningMetrics,
)


@dataclass
class EvidenceReasoningInsight:
    """
    Combined evidence and reasoning insight.

    Combines objective deterministic metrics with
    semantic interpretation.
    """

    metrics: EvidenceReasoningMetrics
    analysis: EvidenceAnalysis
    evidence_coverage: float
    reasoning_coverage: float
    evidence_strength: str
    reasoning_strength: str
    coaching_points: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.metrics is None:
            raise ValueError("Metrics cannot be None.")

        if self.analysis is None:
            raise ValueError("Analysis cannot be None.")

        if not 0 <= self.evidence_coverage <= 1:
            raise ValueError(
                "Evidence coverage must be between 0 and 1."
            )

        if not 0 <= self.reasoning_coverage <= 1:
            raise ValueError(
                "Reasoning coverage must be between 0 and 1."
            )

        if not self.evidence_strength.strip():
            raise ValueError(
                "Evidence strength cannot be empty."
            )

        if not self.reasoning_strength.strip():
            raise ValueError(
                "Reasoning strength cannot be empty."
            )

        self.evidence_strength = (
            self.evidence_strength.strip()
        )

        self.reasoning_strength = (
            self.reasoning_strength.strip()
        )

        self.coaching_points = [
            point.strip()
            for point in self.coaching_points
            if point and point.strip()
        ]