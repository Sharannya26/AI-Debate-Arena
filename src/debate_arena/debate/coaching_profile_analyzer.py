from debate_arena.debate.coaching_profile import CoachingProfile
from debate_arena.debate.performance_summary import PerformanceSummary


class CoachingProfileAnalyzer:
    """
    Builds a structured CoachingProfile from an existing
    PerformanceSummary.

    This analyzer is deterministic and does not call Gemini.

    Strengths and improvement areas are derived from observable
    performance evidence already present in the PerformanceSummary.

    The logic is topic-independent.
    """

    def analyze(
        self,
        summary: PerformanceSummary,
    ) -> CoachingProfile:
        if summary is None:
            raise ValueError(
                "Performance summary cannot be None."
            )

        strengths = self._extract_strengths(
            strongest_moments=summary.strongest_moments,
            dimension_summaries=summary.dimension_summaries,
        )

        improvement_areas = (
            self._extract_improvement_areas(
                dimension_summaries=summary.dimension_summaries,
            )
        )

        overall_coaching_summary = (
            self._build_overall_coaching_summary(
                strengths=strengths,
                improvement_areas=improvement_areas,
                coaching_priorities=summary.coaching_priorities,
            )
        )

        return CoachingProfile(
            strengths=strengths,
            improvement_areas=improvement_areas,
            coaching_priorities=list(
                summary.coaching_priorities
            ),
            strongest_moments=list(
                summary.strongest_moments
            ),
            weakest_moments=list(
                summary.weakest_moments
            ),
            overall_coaching_summary=(
                overall_coaching_summary
            ),
        )

    @classmethod
    def _extract_strengths(
        cls,
        strongest_moments: list[str],
        dimension_summaries: dict[str, str],
    ) -> list[str]:
        """
        Extract strengths from positive performance evidence.

        Dimension summaries are the primary source because they
        provide structured performance information.

        Strongest moments are used as a fallback when no explicit
        positive dimension summary is available.
        """

        strengths: list[str] = []

        # ---------------------------------------------------------
        # 1. Prefer explicit positive dimension summaries.
        # ---------------------------------------------------------
        for dimension, summary in dimension_summaries.items():
            cleaned_summary = str(summary).strip()

            if not cleaned_summary:
                continue

            normalized = cleaned_summary.lower()

            if cls._is_explicit_strength_signal(normalized):
                strengths.append(
                    f"{dimension}: {cleaned_summary}"
                )

        # ---------------------------------------------------------
        # 2. If no structured strength was found, use the
        #    strongest moments identified by the pipeline.
        # ---------------------------------------------------------
        if not strengths:
            for moment in strongest_moments:
                cleaned_moment = str(moment).strip()

                if not cleaned_moment:
                    continue

                strengths.append(cleaned_moment)

        return cls._deduplicate(strengths)

    @classmethod
    def _extract_improvement_areas(
        cls,
        dimension_summaries: dict[str, str],
    ) -> list[str]:
        """
        Extract improvement areas from dimension summaries.

        Weakest moments are intentionally NOT converted into
        improvement areas here.

        They remain available separately through
        CoachingProfile.weakest_moments.

        This keeps "improvement areas" and "weakest moments"
        conceptually distinct.
        """

        improvement_areas: list[str] = []

        for dimension, summary in dimension_summaries.items():
            cleaned_summary = str(summary).strip()

            if not cleaned_summary:
                continue

            normalized = cleaned_summary.lower()

            if cls._is_explicit_improvement_signal(normalized):
                improvement_areas.append(
                    f"{dimension}: {cleaned_summary}"
                )

        return cls._deduplicate(improvement_areas)

    @staticmethod
    def _is_explicit_strength_signal(
        normalized: str,
    ) -> bool:
        """
        Detect clearly positive performance language.

        These signals are intentionally conservative. A word such
        as "clear" is not enough by itself because phrases such as
        "unclear reasoning" contain the same substring.
        """

        strength_signals = (
            "strong",
            "excellent",
            "effective",
            "well-supported",
            "well supported",
            "highly responsive",
            "demonstrated strong",
            "demonstrated excellent",
            "clear claim supported by reasoning",
            "maintained a consistent position",
            "maintained consistency",
            "improved across",
            "improved significantly",
        )

        return any(
            signal in normalized
            for signal in strength_signals
        )

    @staticmethod
    def _is_explicit_improvement_signal(
        normalized: str,
    ) -> bool:
        """
        Detect clearly negative or improvement-oriented language.

        "Varied" is treated as an improvement signal because the
        current performance-analysis pipeline uses it to indicate
        an area that was not stable across the debate.

        Generic words such as "consistent" or "consistently" are
        NOT automatically treated as weaknesses.
        """

        improvement_signals = (
            "declined",
            "decline",
            "varied",
            "weakness",
            "weak",
            "limited",
            "poor",
            "unclear",
            "unclear claim",
            "no explicit",
            "not identified",
            "not supported",
            "missing",
            "lacks",
            "lack of",
            "lacking",
            "insufficient",
            "needs improvement",
            "needs strengthening",
            "could improve",
            "could be improved",
            "should improve",
            "should be strengthened",
            "inconsistent",
            "identifiable weaknesses",
            "minimally responsive",
            "partially responsive",
        )

        return any(
            signal in normalized
            for signal in improvement_signals
        )

    @staticmethod
    def _deduplicate(
        items: list[str],
    ) -> list[str]:
        """
        Preserve insertion order while removing duplicates.
        """

        result: list[str] = []
        seen: set[str] = set()

        for item in items:
            normalized = item.strip().lower()

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(normalized)
            result.append(item.strip())

        return result

    @staticmethod
    def _build_overall_coaching_summary(
        strengths: list[str],
        improvement_areas: list[str],
        coaching_priorities: list[str],
    ) -> str:
        if (
            strengths
            and improvement_areas
            and coaching_priorities
        ):
            return (
                "Your debate shows several established "
                "strengths, while the identified improvement "
                "areas point to clear opportunities for your "
                "next round of growth."
            )

        if strengths and improvement_areas:
            return (
                "Your debate shows a mix of established "
                "strengths and areas that can be strengthened "
                "further."
            )

        if improvement_areas and coaching_priorities:
            return (
                "Focus on the identified improvement areas "
                "and apply the recommended coaching priorities "
                "in future debates."
            )

        if improvement_areas:
            return (
                "Your current performance highlights specific "
                "areas that can be strengthened in future "
                "debates."
            )

        if strengths:
            return (
                "Maintain the identified strengths while "
                "continuing to develop overall debate skills."
            )

        return (
            "Use the current debate performance as a "
            "baseline for future coaching."
        )