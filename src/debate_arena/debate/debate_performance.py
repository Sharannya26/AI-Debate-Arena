from dataclasses import dataclass, field

from debate_arena.debate.round_performance import (
    RoundPerformance,
)


@dataclass
class DebatePerformance:
    """
    Structured representation of a user's overall
    debate performance.

    This model intentionally keeps individual performance
    dimensions separate instead of collapsing everything
    into a single score.
    """

    round_performances: list[RoundPerformance] = field(
        default_factory=list
    )

    argument_quality: str = ""
    communication_quality: str = ""
    responsiveness: str = ""
    consistency: str = ""
    evidence_usage: str = ""
    reasoning_quality: str = ""

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
        self.argument_quality = (
            self.argument_quality.strip()
        )

        self.communication_quality = (
            self.communication_quality.strip()
        )

        self.responsiveness = (
            self.responsiveness.strip()
        )

        self.consistency = (
            self.consistency.strip()
        )

        self.evidence_usage = (
            self.evidence_usage.strip()
        )

        self.reasoning_quality = (
            self.reasoning_quality.strip()
        )

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