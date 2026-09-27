from dataclasses import dataclass, field


@dataclass
class PersonalizedImprovementPriority:
    """
    Represents one personalized improvement priority
    derived from a user's debate coaching profile.

    This model stores structured coaching information.
    It does not perform analysis and does not call Gemini.
    """

    priority: str
    reason: str
    focus_area: str
    supporting_evidence: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.priority = self.priority.strip()
        self.reason = self.reason.strip()
        self.focus_area = self.focus_area.strip()

        self.supporting_evidence = [
            evidence.strip()
            for evidence in self.supporting_evidence
            if evidence and evidence.strip()
        ]

        if not self.priority:
            raise ValueError(
                "Improvement priority cannot be empty."
            )

        if not self.reason:
            raise ValueError(
                "Improvement priority reason cannot be empty."
            )

        if not self.focus_area:
            raise ValueError(
                "Improvement priority focus area cannot be empty."
            )