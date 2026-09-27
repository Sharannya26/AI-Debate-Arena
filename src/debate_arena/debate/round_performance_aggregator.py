from debate_arena.debate.round_performance import RoundPerformance


class RoundPerformanceAggregator:
    """
    Organizes round-level debate performance and provides
    simple deterministic comparisons across rounds.

    This class does not call Gemini.
    """

    def aggregate(
        self,
        round_performances: list[RoundPerformance],
    ) -> list[RoundPerformance]:
        if round_performances is None:
            raise ValueError(
                "Round performances cannot be None."
            )

        for performance in round_performances:
            if performance is None:
                raise ValueError(
                    "Round performances cannot contain None."
                )

        return sorted(
            round_performances,
            key=lambda performance: performance.round,
        )

    def strongest_round(
        self,
        round_performances: list[RoundPerformance],
    ) -> RoundPerformance | None:
        ordered = self.aggregate(round_performances)

        if not ordered:
            return None

        return ordered[-1]

    def weakest_round(
        self,
        round_performances: list[RoundPerformance],
    ) -> RoundPerformance | None:
        ordered = self.aggregate(round_performances)

        if not ordered:
            return None

        return ordered[0]

    def dimension_values(
        self,
        round_performances: list[RoundPerformance],
        dimension: str,
    ) -> list[str]:
        ordered = self.aggregate(round_performances)

        valid_dimensions = {
            "argument_quality",
            "communication_quality",
            "evidence_usage",
            "reasoning_quality",
            "responsiveness",
        }

        if dimension not in valid_dimensions:
            raise ValueError(
                f"Unsupported performance dimension: {dimension}"
            )

        return [
            getattr(performance, dimension)
            for performance in ordered
        ]