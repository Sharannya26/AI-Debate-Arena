from debate_arena.debate.moment_analysis import MomentAnalysis
from debate_arena.debate.round_performance import RoundPerformance


class MomentAnalyzer:
    """
    Identifies notable strongest and weakest moments from
    already-computed round performance data.

    This analyzer is deterministic and does not call Gemini.

    Strong moments are identified from positive performance
    evidence already produced by RoundPerformanceAnalyzer.

    Weak moments are identified from explicit negative
    performance evidence.
    """

    def analyze(
        self,
        round_performances: list[RoundPerformance],
    ) -> tuple[list[str], list[str]]:
        """
        Preserve the original M9.5 interface.

        Returns:
            A tuple containing:
            (strongest_moments, weakest_moments)
        """
        analysis = self.analyze_structured(round_performances)

        return (
            analysis.strongest_moments,
            analysis.weakest_moments,
        )

    def analyze_structured(
        self,
        round_performances: list[RoundPerformance],
    ) -> MomentAnalysis:
        """
        Perform deterministic moment analysis and return
        the structured M9.8 MomentAnalysis model.
        """
        if round_performances is None:
            raise ValueError(
                "Round performances cannot be None."
            )

        for performance in round_performances:
            if performance is None:
                raise ValueError(
                    "Round performances cannot contain None."
                )

        if not round_performances:
            return MomentAnalysis()

        strongest_moments: list[str] = []
        weakest_moments: list[str] = []

        for performance in round_performances:
            self._collect_dimension_moment(
                strongest_moments,
                weakest_moments,
                performance.round,
                "argument quality",
                performance.argument_quality,
            )

            self._collect_dimension_moment(
                strongest_moments,
                weakest_moments,
                performance.round,
                "communication quality",
                performance.communication_quality,
            )

            self._collect_dimension_moment(
                strongest_moments,
                weakest_moments,
                performance.round,
                "evidence usage",
                performance.evidence_usage,
            )

            self._collect_dimension_moment(
                strongest_moments,
                weakest_moments,
                performance.round,
                "reasoning quality",
                performance.reasoning_quality,
            )

            if performance.responsiveness is not None:
                self._collect_dimension_moment(
                    strongest_moments,
                    weakest_moments,
                    performance.round,
                    "responsiveness",
                    performance.responsiveness,
                )

        return MomentAnalysis(
            strongest_moments=strongest_moments,
            weakest_moments=weakest_moments,
        )

    def _collect_dimension_moment(
        self,
        strongest_moments: list[str],
        weakest_moments: list[str],
        round_number: int,
        dimension: str,
        value: str,
    ) -> None:
        if not value or not value.strip():
            return

        cleaned_value = value.strip()
        normalized = cleaned_value.lower()

        if self._is_strong(normalized):
            strongest_moments.append(
                f"Round {round_number}: "
                f"Strong {dimension} — {cleaned_value}"
            )

        if self._is_weak(normalized):
            weakest_moments.append(
                f"Round {round_number}: "
                f"Weak {dimension} — {cleaned_value}"
            )

    @staticmethod
    def _is_strong(value: str) -> bool:
        """
        Identify explicit positive performance evidence.

        These signals correspond to positive descriptions
        already produced by the deterministic round-performance
        analyzers.
        """
        strong_terms = (
            # General positive performance
            "strong",
            "excellent",
            "effective",
            "highly responsive",
            "highly consistent",
            "clear and strong",

            # Argument quality
            "clear claim supported by reasoning",
            "clear claim",

            # Communication quality
            "moderate pace",

            # Evidence usage
            "used ",
            "identified piece(s) of evidence",

            # Reasoning quality
            "reasoning was identified",

            # Responsiveness
            "highly responsive",
        )

        return any(
            term in value
            for term in strong_terms
        )

    @staticmethod
    def _is_weak(value: str) -> bool:
        """
        Identify explicit negative performance evidence.
        """
        weak_terms = (
            "weak",
            "limited",
            "poor",
            "none",
            "not responsive",
            "no consistent",
            "could not be clearly established",
            "no explicit",
        )

        return any(
            term in value
            for term in weak_terms
        )