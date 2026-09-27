from debate_arena.debate.debate_performance import (
    DebatePerformance,
)
from debate_arena.debate.performance_summary import (
    PerformanceSummary,
)


class PerformanceSummaryAnalyzer:
    """
    Creates a deterministic high-level summary from an
    already-computed DebatePerformance object.

    This class does not call Gemini.
    """

    def analyze(
        self,
        performance: DebatePerformance,
        dimension_summaries: dict[str, str] | None = None,
    ) -> PerformanceSummary:
        if performance is None:
            raise ValueError(
                "Performance cannot be None."
            )

        if dimension_summaries is None:
            dimension_summaries = {}

        cleaned_dimensions = {
            key.strip(): value.strip()
            for key, value in dimension_summaries.items()
            if key
            and key.strip()
            and value
            and value.strip()
        }

        overall_summary = self._build_overall_summary(
            performance,
            cleaned_dimensions,
        )

        return PerformanceSummary(
            overall_summary=overall_summary,
            dimension_summaries=cleaned_dimensions,
            strongest_moments=list(
                performance.strongest_moments
            ),
            weakest_moments=list(
                performance.weakest_moments
            ),
            coaching_priorities=list(
                performance.coaching_priorities
            ),
        )

    def _build_overall_summary(
        self,
        performance: DebatePerformance,
        dimension_summaries: dict[str, str],
    ) -> str:
        if dimension_summaries:
            summaries = list(
                dimension_summaries.values()
            )

            improved = sum(
                "improved" in summary.lower()
                for summary in summaries
            )

            declined = sum(
                "declined" in summary.lower()
                for summary in summaries
            )

            varied = sum(
                "varied" in summary.lower()
                for summary in summaries
            )

            if improved > declined and improved > varied:
                return (
                    "Performance improved across "
                    "multiple debate dimensions."
                )

            if declined > improved and declined > varied:
                return (
                    "Performance declined across "
                    "multiple debate dimensions."
                )

            if varied > 0:
                return (
                    "Performance varied across "
                    "the debate."
                )

        if performance.strongest_moments:
            if performance.weakest_moments:
                return (
                    "The debate showed a mix of "
                    "performance strengths and areas "
                    "for improvement."
                )

            return (
                "The debate demonstrated several "
                "notable strengths."
            )

        if performance.weakest_moments:
            return (
                "The debate identified several "
                "areas for improvement."
            )

        return (
            "The debate performance data provides "
            "a baseline for further analysis."
        )