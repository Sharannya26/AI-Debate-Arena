from debate_arena.debate.performance_summary import (
    PerformanceSummary,
)
from debate_arena.debate.semantic_performance_analysis import (
    SemanticPerformanceAnalysis,
)
from debate_arena.debate.semantic_performance_prompts import (
    build_semantic_performance_prompt,
)
from debate_arena.llm.client import LLMClient


class SemanticPerformanceAnalyzer:
    """
    Uses an LLM to semantically interpret a deterministic
    PerformanceSummary.

    The analyzer itself does not calculate debate metrics.
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
    ) -> None:
        self.llm_client = (
            llm_client or LLMClient()
        )

    def analyze(
        self,
        summary: PerformanceSummary,
    ) -> SemanticPerformanceAnalysis:
        if summary is None:
            raise ValueError(
                "Performance summary cannot be None."
            )

        prompt = build_semantic_performance_prompt(
            summary
        )

        data = (
            self.llm_client
            .analyze_semantic_performance(prompt)
        )

        return SemanticPerformanceAnalysis(
            overall_interpretation=data.get(
                "overall_interpretation",
                "Unable to determine overall interpretation.",
            ),
            strengths_interpretation=data.get(
                "strengths_interpretation",
                "",
            ),
            weaknesses_interpretation=data.get(
                "weaknesses_interpretation",
                "",
            ),
            coaching_interpretation=data.get(
                "coaching_interpretation",
                "",
            ),
            key_insights=data.get(
                "key_insights",
                [],
            ),
        )