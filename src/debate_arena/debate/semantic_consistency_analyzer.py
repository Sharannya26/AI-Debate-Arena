from debate_arena.debate.argument import Argument
from debate_arena.debate.consistency_analysis import (
    ConsistencyAnalysis,
)
from debate_arena.debate.consistency_prompts import (
    build_consistency_prompt,
)
from debate_arena.llm.client import LLMClient


class SemanticConsistencyAnalyzer:
    """
    Performs semantic consistency analysis using Gemini.

    Unlike the deterministic ConsistencyAnalyzer, this analyzer
    can recognize paraphrases and semantic contradictions even
    when the exact keywords differ.
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()

    def analyze(
        self,
        user_arguments: list[Argument],
    ) -> ConsistencyAnalysis:
        if user_arguments is None:
            raise ValueError(
                "User arguments cannot be None."
            )

        if len(user_arguments) < 2:
            raise ValueError(
                "At least two user arguments are required."
            )

        for argument in user_arguments:
            if argument is None:
                raise ValueError(
                    "User arguments cannot contain None."
                )

            if argument.speaker != "user":
                raise ValueError(
                    "All arguments must be from the user."
                )

        prompt = build_consistency_prompt(
            [
                argument.text
                for argument in user_arguments
            ]
        )

        data = self.llm_client.analyze_consistency(
            prompt
        )

        return ConsistencyAnalysis(
            consistency=data.get(
                "consistency",
                "Unable to determine consistency.",
            ),
            consistent_points=data.get(
                "consistent_points",
                [],
            ),
            inconsistent_points=data.get(
                "inconsistent_points",
                [],
            ),
        )