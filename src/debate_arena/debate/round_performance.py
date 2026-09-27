from dataclasses import dataclass


@dataclass
class RoundPerformance:
    """
    Represents the user's performance during one debate round.

    Responsiveness is optional for now because it will be
    calculated separately in M9.2.
    """

    round: int
    argument_quality: str
    communication_quality: str
    evidence_usage: str
    reasoning_quality: str
    responsiveness: str | None = None

    def __post_init__(self) -> None:
        if self.round < 1:
            raise ValueError("Round must be at least 1.")

        if not self.argument_quality.strip():
            raise ValueError("Argument quality cannot be empty.")

        if not self.communication_quality.strip():
            raise ValueError("Communication quality cannot be empty.")

        if not self.evidence_usage.strip():
            raise ValueError("Evidence usage cannot be empty.")

        if not self.reasoning_quality.strip():
            raise ValueError("Reasoning quality cannot be empty.")

        if (
            self.responsiveness is not None
            and not self.responsiveness.strip()
        ):
            raise ValueError("Responsiveness cannot be empty.")

        self.argument_quality = self.argument_quality.strip()
        self.communication_quality = self.communication_quality.strip()
        self.evidence_usage = self.evidence_usage.strip()
        self.reasoning_quality = self.reasoning_quality.strip()

        if self.responsiveness is not None:
            self.responsiveness = self.responsiveness.strip()