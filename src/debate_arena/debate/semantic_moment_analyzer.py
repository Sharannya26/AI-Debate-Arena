from debate_arena.debate.moment_analysis import MomentAnalysis
from debate_arena.debate.moment_prompts import (
    build_moment_analysis_prompt,
)
from debate_arena.debate.semantic_moment_analysis import (
    SemanticMomentAnalysis,
)


class SemanticMomentAnalyzer:
    """
    Uses the LLM client to semantically interpret
    deterministic strongest and weakest moment findings.

    The deterministic MomentAnalysis remains the source
    of truth for which moments were detected.
    """

    def __init__(self, llm_client=None) -> None:
        if llm_client is None:
            from debate_arena.llm.client import LLMClient

            llm_client = LLMClient()

        self.llm_client = llm_client

    def analyze(
        self,
        analysis: MomentAnalysis,
    ) -> SemanticMomentAnalysis:
        """
        Interpret deterministic moment findings using Gemini.
        """

        if analysis is None:
            raise ValueError(
                "Moment analysis cannot be None."
            )

        prompt = build_moment_analysis_prompt(
            analysis
        )

        data = self.llm_client.analyze_moment_analysis(
            prompt
        )

        return SemanticMomentAnalysis(
            strongest_interpretation=data.get(
                "strongest_interpretation",
                "",
            ),
            weakest_interpretation=data.get(
                "weakest_interpretation",
                "",
            ),
            key_insights=data.get(
                "key_insights",
                [],
            ),
        )