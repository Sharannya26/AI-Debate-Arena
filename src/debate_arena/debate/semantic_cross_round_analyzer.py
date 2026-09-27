from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis
from debate_arena.debate.cross_round_prompts import (
    build_cross_round_analysis_prompt,
)
from debate_arena.llm.client import LLMClient


class SemanticCrossRoundAnalyzer:
    """
    Semantic analyzer for cross-round debate-performance findings.

    The deterministic CrossRoundAnalyzer identifies the observable
    performance patterns. This class asks the LLM to interpret those
    findings without recalculating metrics or inventing observations.
    """

    REQUIRED_FIELDS = (
        "overall_interpretation",
        "improvement_interpretation",
        "decline_interpretation",
        "stability_interpretation",
        "recurring_interpretation",
        "cross_dimension_interpretation",
        "key_insights",
    )

    def __init__(
        self,
        llm_client=None,
        prompt_builder=None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.prompt_builder = (
            prompt_builder or build_cross_round_analysis_prompt
        )
        self.last_analysis: CrossRoundAnalysis | None = None

    def analyze(
        self,
        analysis: CrossRoundAnalysis,
    ) -> CrossRoundAnalysis:
        """
        Interpret deterministic cross-round findings semantically.

        Raises:
            ValueError: If analysis is None.
            RuntimeError: If the prompt or LLM response is invalid.
        """
        if analysis is None:
            raise ValueError("Cross-round analysis cannot be None.")

        prompt = self.prompt_builder(analysis)

        if not prompt or not prompt.strip():
            raise RuntimeError(
                "Cross-round analysis prompt cannot be empty."
            )

        data = self.llm_client.analyze_cross_round_performance(prompt)

        if not isinstance(data, dict):
            raise RuntimeError(
                "Cross-round analysis response must be a dictionary."
            )

        missing_fields = [
            field
            for field in self.REQUIRED_FIELDS
            if field not in data
        ]

        if missing_fields:
            raise RuntimeError(
                "Cross-round analysis response is missing fields: "
                + ", ".join(missing_fields)
            )

        result = CrossRoundAnalysis(
            overall_trajectory=data["overall_interpretation"],
            improvement_patterns=[
                data["improvement_interpretation"]
            ],
            decline_patterns=[
                data["decline_interpretation"]
            ],
            stable_patterns=[
                data["stability_interpretation"]
            ],
            recurring_patterns=[
                data["recurring_interpretation"]
            ],
            cross_dimension_patterns=[
                data["cross_dimension_interpretation"]
            ],
            key_insights=data["key_insights"],
        )

        self.last_analysis = result

        return result