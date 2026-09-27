from dataclasses import dataclass


@dataclass
class ActionableCoachingRecommendation:
    """
    Represents one concrete coaching recommendation
    derived from a personalized improvement priority.

    This model stores structured coaching guidance.
    It does not perform analysis and does not call Gemini.
    """

    recommendation: str
    reason: str
    action: str
    related_priority: str

    def __post_init__(self) -> None:
        self.recommendation = self.recommendation.strip()
        self.reason = self.reason.strip()
        self.action = self.action.strip()
        self.related_priority = (
            self.related_priority.strip()
        )

        if not self.recommendation:
            raise ValueError(
                "Coaching recommendation cannot be empty."
            )

        if not self.reason:
            raise ValueError(
                "Coaching recommendation reason cannot be empty."
            )

        if not self.action:
            raise ValueError(
                "Coaching recommendation action cannot be empty."
            )

        if not self.related_priority:
            raise ValueError(
                "Related priority cannot be empty."
            )