from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)
from debate_arena.debate.practice_exercise import (
    PracticeExercise,
)


class PracticeExerciseAnalyzer:
    """
    Converts personalized improvement priorities into
    structured practice exercises.

    This analyzer is deterministic and does not call Gemini.
    """

    EXERCISE_GUIDANCE = {
        "argument quality": {
            "exercise": (
                "Build a complete argument."
            ),
            "objective": (
                "Improve argument quality."
            ),
            "instructions": (
                "State one clear claim, give one reason "
                "supporting it, and finish with one "
                "concrete example."
            ),
        },
        "communication quality": {
            "exercise": (
                "Practice delivering a concise argument."
            ),
            "objective": (
                "Improve communication quality."
            ),
            "instructions": (
                "Explain one important point in one or "
                "two clear sentences before adding "
                "any additional detail."
            ),
        },
        "evidence usage": {
            "exercise": (
                "Practice supporting a claim with evidence."
            ),
            "objective": (
                "Improve evidence usage."
            ),
            "instructions": (
                "State one claim and support it with "
                "one concrete example, fact, or statistic."
            ),
        },
        "reasoning quality": {
            "exercise": (
                "Practice connecting evidence to conclusions."
            ),
            "objective": (
                "Improve reasoning quality."
            ),
            "instructions": (
                "State one claim, provide supporting evidence, "
                "and explain why that evidence supports "
                "your conclusion."
            ),
        },
        "responsiveness": {
            "exercise": (
                "Practice responding directly to an opponent."
            ),
            "objective": (
                "Improve responsiveness."
            ),
            "instructions": (
                "Identify the opponent's main claim and "
                "begin your response by directly addressing "
                "that claim before introducing your own point."
            ),
        },
    }

    def analyze(
        self,
        priorities: list[PersonalizedImprovementPriority],
    ) -> list[PracticeExercise]:
        if priorities is None:
            raise ValueError(
                "Improvement priorities cannot be None."
            )

        exercises = []

        for priority in priorities:
            if priority is None:
                raise ValueError(
                    "Improvement priorities cannot contain None."
                )

            exercise = self._build_exercise(priority)

            if exercise is not None:
                exercises.append(exercise)

        return exercises

    def _build_exercise(
        self,
        priority: PersonalizedImprovementPriority,
    ) -> PracticeExercise | None:
        focus_area = priority.focus_area.strip().lower()

        dimension = self._extract_dimension(
            focus_area=focus_area,
            priority=priority.priority,
        )

        guidance = self.EXERCISE_GUIDANCE.get(
            dimension
        )

        if guidance is None:
            return PracticeExercise(
                exercise=priority.priority,
                objective=priority.reason,
                instructions=(
                    "Apply this improvement priority "
                    "deliberately during a short practice debate."
                ),
                related_priority=priority.priority,
            )

        return PracticeExercise(
            exercise=guidance["exercise"],
            objective=guidance["objective"],
            instructions=guidance["instructions"],
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