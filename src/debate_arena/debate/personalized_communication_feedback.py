from dataclasses import dataclass

from debate_arena.debate.communication_improvement_target import (
    CommunicationImprovementTarget,
)


@dataclass
class PersonalizedCommunicationFeedback:
    """
    Represents personalized communication coaching
    derived from a communication analysis.

    The primary improvement focus is represented by a
    CommunicationImprovementTarget so that the coaching
    system uses structured and type-safe improvement areas.
    """

    primary_focus: CommunicationImprovementTarget
    improvement_goal: str
    action_plan: list[str]

    def __post_init__(self) -> None:
        if not isinstance(
            self.primary_focus,
            CommunicationImprovementTarget,
        ):
            raise ValueError(
                "Primary communication focus must be a "
                "CommunicationImprovementTarget."
            )

        if not self.improvement_goal.strip():
            raise ValueError(
                "Communication improvement goal cannot be empty."
            )

        self.action_plan = [
            action.strip()
            for action in self.action_plan
            if action.strip()
        ]

        if not self.action_plan:
            raise ValueError(
                "At least one communication action is required."
            )

        self.improvement_goal = (
            self.improvement_goal.strip()
        )