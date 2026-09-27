from dataclasses import dataclass, field


@dataclass
class PerformanceSummary:
    """
    Deterministic summary of a user's debate performance.

    This model combines already-computed performance information.
    It does not assign a numerical score.
    """

    overall_summary: str
    dimension_summaries: dict[str, str] = field(
        default_factory=dict
    )
    strongest_moments: list[str] = field(
        default_factory=list
    )
    weakest_moments: list[str] = field(
        default_factory=list
    )
    coaching_priorities: list[str] = field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        if not self.overall_summary.strip():
            raise ValueError(
                "Overall summary cannot be empty."
            )

        self.overall_summary = (
            self.overall_summary.strip()
        )

        self.dimension_summaries = {
            key.strip(): value.strip()
            for key, value in self.dimension_summaries.items()
            if key
            and key.strip()
            and value
            and value.strip()
        }

        self.strongest_moments = [
            moment.strip()
            for moment in self.strongest_moments
            if moment and moment.strip()
        ]

        self.weakest_moments = [
            moment.strip()
            for moment in self.weakest_moments
            if moment and moment.strip()
        ]

        self.coaching_priorities = [
            priority.strip()
            for priority in self.coaching_priorities
            if priority and priority.strip()
        ]