from debate_arena.debate.advanced_debate_analysis import (
    AdvancedDebateAnalysis,
)
from debate_arena.debate.advanced_debate_prompts import (
    build_advanced_debate_analysis_prompt,
)
from debate_arena.debate.debate_performance import DebatePerformance
from debate_arena.debate.performance_summary import PerformanceSummary
from debate_arena.llm.client import LLMClient


class AdvancedDebateAnalyzer:
    """
    Performs advanced semantic interpretation of an already-computed
    debate performance.

    Deterministic metrics are calculated elsewhere. This analyzer only
    asks the LLM to interpret the supplied performance information.
    """

    REQUIRED_FIELDS = (
        "overall_interpretation",
        "cross_dimension_patterns",
        "round_patterns",
        "strengths_interpretation",
        "weaknesses_interpretation",
        "coaching_interpretation",
        "key_insights",
    )

    def __init__(
        self,
        llm_client=None,
        prompt_builder=None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.prompt_builder = (
            prompt_builder or build_advanced_debate_analysis_prompt
        )

        self.last_analysis: AdvancedDebateAnalysis | None = None

    def analyze(
        self,
        performance: DebatePerformance,
        summary: PerformanceSummary,
    ) -> AdvancedDebateAnalysis:
        """
        Interpret the supplied debate performance and summary.
        """

        if performance is None:
            raise ValueError("Debate performance cannot be None.")

        if summary is None:
            raise ValueError("Performance summary cannot be None.")

        prompt = self.prompt_builder(
            performance,
            summary,
        )

        if not prompt or not prompt.strip():
            raise RuntimeError(
                "Advanced debate analysis prompt cannot be empty."
            )

        data = self.llm_client.analyze_advanced_debate_performance(
            prompt
        )

        if not isinstance(data, dict):
            raise RuntimeError(
                "Advanced debate analysis response must be a dictionary."
            )

        missing_fields = [
            field
            for field in self.REQUIRED_FIELDS
            if field not in data
        ]

        if missing_fields:
            raise RuntimeError(
                "Advanced debate analysis response is missing fields: "
                + ", ".join(missing_fields)
            )

        analysis = AdvancedDebateAnalysis(
            overall_interpretation=data["overall_interpretation"],
            cross_dimension_patterns=data[
                "cross_dimension_patterns"
            ],
            round_patterns=data["round_patterns"],
            strengths_interpretation=data[
                "strengths_interpretation"
            ],
            weaknesses_interpretation=data[
                "weaknesses_interpretation"
            ],
            coaching_interpretation=data[
                "coaching_interpretation"
            ],
            key_insights=data["key_insights"],
        )

        self.last_analysis = analysis

        return analysis