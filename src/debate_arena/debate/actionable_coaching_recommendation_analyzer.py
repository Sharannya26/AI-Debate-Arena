from debate_arena.debate.actionable_coaching_recommendation import (
    ActionableCoachingRecommendation,
)
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)


class ActionableCoachingRecommendationAnalyzer:
    """
    Converts personalized improvement priorities into
    concrete, actionable coaching recommendations.

    This analyzer is deterministic and does not call Gemini.
    """

    RECOMMENDATION_GUIDANCE = {
        "argument quality": {
            "recommendation": (
                "Structure each argument around a clear "
                "claim, reason, and supporting example."
            ),
            "action": (
                "Before your next debate, prepare your main "
                "claim and at least one reason and example "
                "to support it."
            ),
        },
        "communication quality": {
            "recommendation": (
                "Deliver your arguments using concise and "
                "clearly structured sentences."
            ),
            "action": (
                "Practice explaining each major point in "
                "one or two clear sentences before expanding "
                "with additional detail."
            ),
        },
        "evidence usage": {
            "recommendation": (
                "Support important claims with concrete "
                "evidence, examples, or statistics."
            ),
            "action": (
                "Prepare two or three relevant examples, "
                "facts, or statistics before your next debate."
            ),
        },
        "reasoning quality": {
            "recommendation": (
                "Make the logical connection between your "
                "claims, reasons, and conclusions explicit."
            ),
            "action": (
                "For each major claim, practice explaining "
                "why your evidence supports your conclusion."
            ),
        },
        "responsiveness": {
            "recommendation": (
                "Address the opponent's main argument directly "
                "before presenting your counterargument."
            ),
            "action": (
                "Listen for the opponent's central claim and "
                "state how your response addresses that claim "
                "before introducing new points."
            ),
        },
    }

    def analyze(
        self,
        priorities: list[PersonalizedImprovementPriority],
    ) -> list[ActionableCoachingRecommendation]:
        if priorities is None:
            raise ValueError(
                "Improvement priorities cannot be None."
            )

        recommendations = []

        for priority in priorities:
            if priority is None:
                raise ValueError(
                    "Improvement priorities cannot contain None."
                )

            recommendation = self._build_recommendation(
                priority
            )

            if recommendation is not None:
                recommendations.append(recommendation)

        return recommendations

    def _build_recommendation(
        self,
        priority: PersonalizedImprovementPriority,
    ) -> ActionableCoachingRecommendation | None:
        focus_area = priority.focus_area.strip().lower()

        dimension = self._extract_dimension(
            focus_area=focus_area,
            priority=priority.priority,
        )

        guidance = self.RECOMMENDATION_GUIDANCE.get(
            dimension
        )

        if guidance is None:
            return ActionableCoachingRecommendation(
                recommendation=priority.priority,
                reason=priority.reason,
                action=(
                    "Apply this improvement priority "
                    "deliberately during your next debate."
                ),
                related_priority=priority.priority,
            )

        return ActionableCoachingRecommendation(
            recommendation=guidance["recommendation"],
            reason=priority.reason,
            action=guidance["action"],
            related_priority=priority.priority,
        )

    @staticmethod
    def _extract_dimension(
        focus_area: str,
        priority: str,
    ) -> str:
        known_dimensions = (
            "argument quality",
            "communication quality",
            "evidence usage",
            "reasoning quality",
            "responsiveness",
        )

        for dimension in known_dimensions:
            if dimension in focus_area:
                return dimension

        normalized_priority = priority.strip().lower()

        for dimension in known_dimensions:
            if dimension in normalized_priority:
                return dimension

        return ""