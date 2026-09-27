from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis
from debate_arena.debate.round_performance import RoundPerformance


class CrossRoundAnalyzer:
    """
    Deterministic analyzer for identifying performance patterns across rounds.

    This analyzer compares already-computed qualitative performance labels.
    It does not use an LLM and does not calculate numerical performance scores.
    """

    QUALITY_LEVELS = {
        "very weak": 0,
        "weak": 1,
        "limited": 2,
        "moderate": 3,
        "partial": 3,
        "partially responsive": 3,
        "mostly consistent": 3,
        "strong": 4,
        "highly responsive": 5,
        "highly consistent": 5,
        "excellent": 5,
    }

    DIMENSIONS = (
        "argument_quality",
        "communication_quality",
        "evidence_usage",
        "reasoning_quality",
        "responsiveness",
    )

    DIMENSION_LABELS = {
        "argument_quality": "Argument quality",
        "communication_quality": "Communication quality",
        "evidence_usage": "Evidence usage",
        "reasoning_quality": "Reasoning quality",
        "responsiveness": "Responsiveness",
    }

    def analyze(
        self,
        round_performances: list[RoundPerformance],
    ) -> CrossRoundAnalysis:
        """
        Analyze performance changes across debate rounds.

        Raises:
            ValueError: If round_performances is None or empty.
        """
        if round_performances is None:
            raise ValueError("Round performances cannot be None.")

        if not round_performances:
            raise ValueError("At least one round performance is required.")

        ordered_rounds = sorted(
            round_performances,
            key=lambda performance: performance.round,
        )

        improvement_patterns: list[str] = []
        decline_patterns: list[str] = []
        stable_patterns: list[str] = []
        recurring_patterns: list[str] = []

        for dimension in self.DIMENSIONS:
            values = [
                self._get_dimension_value(performance, dimension)
                for performance in ordered_rounds
            ]

            scores = [
                self._quality_score(value)
                for value in values
            ]

            label = self.DIMENSION_LABELS[dimension]

            if len(values) >= 2:
                if scores[-1] > scores[0]:
                    improvement_patterns.append(
                        f"{label} improved across the debate."
                    )
                elif scores[-1] < scores[0]:
                    decline_patterns.append(
                        f"{label} declined across the debate."
                    )
                else:
                    stable_patterns.append(
                        f"{label} remained stable across the debate."
                    )

            if len(values) >= 2 and len(set(values)) == 1:
                recurring_patterns.append(
                    f"{label} remained consistently {values[0]} across the rounds."
                )

        overall_trajectory = self._determine_overall_trajectory(
            improvement_patterns=improvement_patterns,
            decline_patterns=decline_patterns,
            stable_patterns=stable_patterns,
        )

        return CrossRoundAnalysis(
            overall_trajectory=overall_trajectory,
            improvement_patterns=improvement_patterns,
            decline_patterns=decline_patterns,
            stable_patterns=stable_patterns,
            recurring_patterns=recurring_patterns,
        )

    def _get_dimension_value(
        self,
        performance: RoundPerformance,
        dimension: str,
    ) -> str:
        value = getattr(performance, dimension)

        if value is None:
            return ""

        return str(value).strip()

    def _quality_score(self, value: str) -> int:
        normalized = value.strip().lower()

        if normalized in self.QUALITY_LEVELS:
            return self.QUALITY_LEVELS[normalized]

        return self._fallback_quality_score(normalized)

    def _fallback_quality_score(self, value: str) -> int:
        """
        Provide a deterministic fallback for qualitative labels that are not
        explicitly listed in QUALITY_LEVELS.

        The fallback uses descriptive keywords rather than numerical scoring
        exposed to the user.
        """
        if any(
            keyword in value
            for keyword in (
                "excellent",
                "highly",
                "strong",
                "clear",
                "good",
            )
        ):
            return 4

        if any(
            keyword in value
            for keyword in (
                "moderate",
                "mostly",
                "partial",
                "adequate",
            )
        ):
            return 3

        if any(
            keyword in value
            for keyword in (
                "limited",
                "weak",
                "poor",
            )
        ):
            return 1

        if any(
            keyword in value
            for keyword in (
                "none",
                "not",
            )
        ):
            return 0

        return 3

    def _determine_overall_trajectory(
        self,
        improvement_patterns: list[str],
        decline_patterns: list[str],
        stable_patterns: list[str],
    ) -> str:
        improvement_count = len(improvement_patterns)
        decline_count = len(decline_patterns)

        if improvement_count > decline_count:
            return "Performance improved across the debate."

        if decline_count > improvement_count:
            return "Performance declined across the debate."

        if improvement_count > 0 and decline_count > 0:
            return "Performance showed mixed changes across the debate."

        if stable_patterns:
            return "Performance remained broadly stable across the debate."

        return "Performance trajectory could not be determined from the available data."