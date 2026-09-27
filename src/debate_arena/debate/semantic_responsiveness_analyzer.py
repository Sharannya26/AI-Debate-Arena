from debate_arena.debate.argument import Argument
from debate_arena.debate.responsiveness_analysis import (
    ResponsivenessAnalysis,
)
from debate_arena.debate.responsiveness_prompts import (
    build_responsiveness_prompt,
)
from debate_arena.llm.client import LLMClient


class SemanticResponsivenessAnalyzer:
    """
    Uses Gemini to determine how semantically responsive
    a user's argument is to the AI's previous argument.

    This analyzer focuses on semantic relationships rather
    than exact keyword overlap.
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
        previous_ai_argument: Argument,
        user_argument: Argument,
    ) -> ResponsivenessAnalysis:
        """
        Analyze semantic responsiveness between an AI
        argument and the user's response.
        """

        if previous_ai_argument is None:
            raise ValueError(
                "Previous AI argument cannot be None."
            )

        if user_argument is None:
            raise ValueError(
                "User argument cannot be None."
            )

        if previous_ai_argument.speaker != "ai":
            raise ValueError(
                "Previous argument must be from the AI."
            )

        if user_argument.speaker != "user":
            raise ValueError(
                "User argument must be from the user."
            )

        prompt = build_responsiveness_prompt(
            previous_ai_argument=previous_ai_argument.text,
            user_argument=user_argument.text,
        )

        data = self.llm_client.analyze_responsiveness(
            prompt
        )

        return ResponsivenessAnalysis(
            responsiveness=data.get(
                "responsiveness",
                "Unable to determine responsiveness.",
            ),
            addressed_points=data.get(
                "addressed_points",
                [],
            ),
            ignored_points=data.get(
                "ignored_points",
                [],
            ),
        )