from dataclasses import dataclass


@dataclass
class EvidenceReasoningMetrics:
    """
    Objective measurements of evidence and reasoning usage
    across the user's debate arguments.
    """

    total_arguments: int
    evidence_arguments: int
    reasoning_arguments: int
    evidence_coverage: float
    reasoning_coverage: float

    def __post_init__(self) -> None:
        if self.total_arguments < 0:
            raise ValueError(
                "Total arguments cannot be negative."
            )

        if self.evidence_arguments < 0:
            raise ValueError(
                "Evidence argument count cannot be negative."
            )

        if self.reasoning_arguments < 0:
            raise ValueError(
                "Reasoning argument count cannot be negative."
            )

        if self.evidence_arguments > self.total_arguments:
            raise ValueError(
                "Evidence argument count cannot exceed "
                "total arguments."
            )

        if self.reasoning_arguments > self.total_arguments:
            raise ValueError(
                "Reasoning argument count cannot exceed "
                "total arguments."
            )

        if not 0 <= self.evidence_coverage <= 1:
            raise ValueError(
                "Evidence coverage must be between 0 and 1."
            )

        if not 0 <= self.reasoning_coverage <= 1:
            raise ValueError(
                "Reasoning coverage must be between 0 and 1."
            )