from dataclasses import dataclass, field


@dataclass
class EvidenceAnalysis:
    """
    Represents the evidence and reasoning quality found
    across the user's debate arguments.
    """

    evidence_quality: str
    reasoning_quality: str

    evidence_points: list[str] = field(
        default_factory=list
    )

    missing_evidence: list[str] = field(
        default_factory=list
    )

    reasoning_points: list[str] = field(
        default_factory=list
    )

    reasoning_gaps: list[str] = field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        if (
            not self.evidence_quality
            or not self.evidence_quality.strip()
        ):
            raise ValueError(
                "Evidence quality cannot be empty."
            )

        if (
            not self.reasoning_quality
            or not self.reasoning_quality.strip()
        ):
            raise ValueError(
                "Reasoning quality cannot be empty."
            )

        self.evidence_quality = (
            self.evidence_quality.strip()
        )

        self.reasoning_quality = (
            self.reasoning_quality.strip()
        )

        self.evidence_points = [
            point.strip()
            for point in self.evidence_points
            if point and point.strip()
        ]

        self.missing_evidence = [
            point.strip()
            for point in self.missing_evidence
            if point and point.strip()
        ]

        self.reasoning_points = [
            point.strip()
            for point in self.reasoning_points
            if point and point.strip()
        ]

        self.reasoning_gaps = [
            point.strip()
            for point in self.reasoning_gaps
            if point and point.strip()
        ]