from dataclasses import dataclass, field

from debate_arena.debate.actionable_coaching_recommendation import (
    ActionableCoachingRecommendation,
)
from debate_arena.debate.coaching_profile import (
    CoachingProfile,
)
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)
from debate_arena.debate.practice_exercise import (
    PracticeExercise,
)


@dataclass
class CoachingSessionReport:
    """
    Structured report for a personalized coaching session.

    This model groups the user's coaching profile,
    improvement priorities, recommendations, and
    practice exercises into one reusable report.

    It does not perform analysis and does not call Gemini.
    """

    coaching_profile: CoachingProfile

    improvement_priorities: list[
        PersonalizedImprovementPriority
    ] = field(default_factory=list)

    recommendations: list[
        ActionableCoachingRecommendation
    ] = field(default_factory=list)

    practice_exercises: list[
        PracticeExercise
    ] = field(default_factory=list)

    session_summary: str = ""

    def __post_init__(self) -> None:
        self.session_summary = (
            self.session_summary.strip()
        )

        if self.coaching_profile is None:
            raise ValueError(
                "Coaching profile cannot be None."
            )

        self.improvement_priorities = [
            priority
            for priority in self.improvement_priorities
            if priority is not None
        ]

        self.recommendations = [
            recommendation
            for recommendation in self.recommendations
            if recommendation is not None
        ]

        self.practice_exercises = [
            exercise
            for exercise in self.practice_exercises
            if exercise is not None
        ]