from debate_arena.debate.argument import Argument
from debate_arena.debate.debate_performance import DebatePerformance
from debate_arena.debate.round_performance import RoundPerformance


class DebatePerformanceAnalyzer:
    """
    Aggregates previously computed debate analyses into
    one structured DebatePerformance object.

    This class is intentionally deterministic. It does not
    call Gemini directly.
    """

    def analyze(
        self,
        round_performances: list[RoundPerformance],
        argument_quality: str,
        communication_quality: str,
        responsiveness: str,
        consistency: str,
        evidence_usage: str,
        reasoning_quality: str,
        strongest_moments: list[str] | None = None,
        weakest_moments: list[str] | None = None,
        coaching_priorities: list[str] | None = None,
    ) -> DebatePerformance:
        if round_performances is None:
            raise ValueError(
                "Round performances cannot be None."
            )

        if argument_quality is None:
            raise ValueError(
                "Argument quality cannot be None."
            )

        if communication_quality is None:
            raise ValueError(
                "Communication quality cannot be None."
            )

        if responsiveness is None:
            raise ValueError(
                "Responsiveness cannot be None."
            )

        if consistency is None:
            raise ValueError(
                "Consistency cannot be None."
            )

        if evidence_usage is None:
            raise ValueError(
                "Evidence usage cannot be None."
            )

        if reasoning_quality is None:
            raise ValueError(
                "Reasoning quality cannot be None."
            )

        for performance in round_performances:
            if performance is None:
                raise ValueError(
                    "Round performances cannot contain None."
                )

        performance = DebatePerformance(
            round_performances=round_performances,
            argument_quality=argument_quality,
            communication_quality=communication_quality,
            responsiveness=responsiveness,
            consistency=consistency,
            evidence_usage=evidence_usage,
            reasoning_quality=reasoning_quality,
            strongest_moments=(
                strongest_moments
                if strongest_moments is not None
                else []
            ),
            weakest_moments=(
                weakest_moments
                if weakest_moments is not None
                else []
            ),
            coaching_priorities=(
                coaching_priorities
                if coaching_priorities is not None
                else []
            ),
        )

        return performance