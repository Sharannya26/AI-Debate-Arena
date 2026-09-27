from debate_arena.debate.coaching_profile import CoachingProfile
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)


class PersonalizedImprovementPriorityAnalyzer:
    """
    Converts a CoachingProfile into personalized,
    structured improvement priorities.

    This analyzer is deterministic and does not call Gemini.
    """

    def analyze(
        self,
        profile: CoachingProfile,
    ) -> list[PersonalizedImprovementPriority]:
        if profile is None:
            raise ValueError(
                "Coaching profile cannot be None."
            )

        priorities: list[PersonalizedImprovementPriority] = []

        for improvement_area in profile.improvement_areas:
            priority = self._build_priority(
                improvement_area=improvement_area,
                coaching_priorities=profile.coaching_priorities,
                weakest_moments=profile.weakest_moments,
            )

            if priority is not None:
                priorities.append(priority)

        return priorities

    def _build_priority(
        self,
        improvement_area: str,
        coaching_priorities: list[str],
        weakest_moments: list[str],
    ) -> PersonalizedImprovementPriority | None:
        if not improvement_area.strip():
            return None

        dimension, summary = self._split_dimension_summary(
            improvement_area
        )

        matching_priority = self._find_matching_priority(
            dimension=dimension,
            coaching_priorities=coaching_priorities,
        )

        supporting_evidence = [summary]

        if weakest_moments:
            supporting_evidence.extend(
                weakest_moments
            )

        return PersonalizedImprovementPriority(
            priority=self._build_priority_title(
                dimension=dimension,
            ),
            reason=self._build_reason(
                dimension=dimension,
                summary=summary,
                matching_priority=matching_priority,
            ),
            focus_area=self._build_focus_area(
                dimension=dimension,
                matching_priority=matching_priority,
            ),
            supporting_evidence=supporting_evidence,
        )

    @staticmethod
    def _split_dimension_summary(
        improvement_area: str,
    ) -> tuple[str, str]:
        if ":" not in improvement_area:
            cleaned = improvement_area.strip()
            return cleaned, cleaned

        dimension, summary = improvement_area.split(
            ":",
            1,
        )

        dimension = dimension.strip()
        summary = summary.strip()

        return dimension, summary

    @staticmethod
    def _find_matching_priority(
        dimension: str,
        coaching_priorities: list[str],
    ) -> str | None:
        normalized_dimension = (
            dimension.strip().lower()
        )

        for priority in coaching_priorities:
            normalized_priority = (
                priority.strip().lower()
            )

            if (
                normalized_dimension
                in normalized_priority
            ):
                return priority

        return None

    @staticmethod
    def _build_priority_title(
        dimension: str,
    ) -> str:
        return (
            f"Improve {dimension.strip().lower()}"
        )

    @staticmethod
    def _build_reason(
        dimension: str,
        summary: str,
        matching_priority: str | None,
    ) -> str:
        if matching_priority:
            return (
                f"{summary} "
                f"Existing coaching guidance: "
                f"{matching_priority}"
            )

        return summary

    @staticmethod
    def _build_focus_area(
        dimension: str,
        matching_priority: str | None,
    ) -> str:
        if matching_priority:
            return matching_priority

        return (
            f"Strengthen {dimension.strip().lower()} "
            "during future debates."
        )