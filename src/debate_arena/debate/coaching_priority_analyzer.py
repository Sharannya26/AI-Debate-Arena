from debate_arena.debate.round_performance import RoundPerformance


class CoachingPriorityAnalyzer:
    """
    Converts identified weaknesses into actionable coaching
    priorities.

    This analyzer is deterministic and does not call Gemini.
    """

    PRIORITY_MESSAGES = {
        "argument quality": (
            "Strengthen the structure and clarity of your "
            "arguments so each claim is supported by a clear "
            "reason or example."
        ),
        "communication quality": (
            "Improve the clarity and delivery of your ideas "
            "by expressing each point in a concise and "
            "structured way."
        ),
        "evidence usage": (
            "Support major claims with concrete examples, "
            "statistics, research, or other relevant evidence."
        ),
        "reasoning quality": (
            "Make the logical connection between your claims "
            "and conclusions more explicit."
        ),
        "responsiveness": (
            "Address the opponent's main point directly "
            "before introducing your rebuttal."
        ),
    }

    def analyze(
        self,
        round_performances: list[RoundPerformance],
    ) -> list[str]:
        if round_performances is None:
            raise ValueError(
                "Round performances cannot be None."
            )

        for performance in round_performances:
            if performance is None:
                raise ValueError(
                    "Round performances cannot contain None."
                )

        priorities: list[str] = []

        for performance in round_performances:
            self._check_dimension(
                priorities,
                "argument quality",
                performance.argument_quality,
            )

            self._check_dimension(
                priorities,
                "communication quality",
                performance.communication_quality,
            )

            self._check_dimension(
                priorities,
                "evidence usage",
                performance.evidence_usage,
            )

            self._check_dimension(
                priorities,
                "reasoning quality",
                performance.reasoning_quality,
            )

            if performance.responsiveness is not None:
                self._check_dimension(
                    priorities,
                    "responsiveness",
                    performance.responsiveness,
                )

        return self._deduplicate(priorities)

    def _check_dimension(
        self,
        priorities: list[str],
        dimension: str,
        value: str,
    ) -> None:
        if not value or not value.strip():
            return

        normalized = value.strip().lower()

        if self._is_weak(normalized):
            priorities.append(
                self.PRIORITY_MESSAGES[dimension]
            )

    @staticmethod
    def _is_weak(value: str) -> bool:
        weak_terms = (
            "weak",
            "limited",
            "poor",
            "none",
            "not responsive",
            "no consistent",
        )

        return any(
            term in value
            for term in weak_terms
        )

    @staticmethod
    def _deduplicate(
        priorities: list[str],
    ) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []

        for priority in priorities:
            if priority not in seen:
                seen.add(priority)
                result.append(priority)

        return result