from debate_arena.debate.argument_analyzer import ArgumentAnalysis
from debate_arena.debate.strategy import DebateStrategy
from debate_arena.debate.strategy_prompts import (
    build_strategy_prompt,
)
from debate_arena.llm.client import LLMClient


class StrategySelector:
    """Selects a debate strategy using structured argument analysis."""

    def __init__(
        self,
        llm: LLMClient | None = None,
    ):
        self.llm = llm or LLMClient()

    def select(
        self,
        context: str,
        latest_argument: str,
        analysis: ArgumentAnalysis | None = None,
    ) -> DebateStrategy:
        """
        Select the most appropriate strategy for the latest argument.

        The structured argument analysis is supplied when available.
        """

        if not context.strip():
            raise ValueError(
                "Debate context cannot be empty."
            )

        if not latest_argument.strip():
            raise ValueError(
                "Latest argument cannot be empty."
            )

        analysis_data = None

        if analysis is not None:
            analysis_data = {
                "claim": analysis.claim,
                "reasoning": analysis.reasoning,
                "assumptions": analysis.assumptions,
                "evidence": analysis.evidence,
                "weaknesses": analysis.weaknesses,
                "argument_type": analysis.argument_type,
            }

        prompt = build_strategy_prompt(
            context=context,
            latest_argument=latest_argument,
            analysis=analysis_data,
        )

        response = self.llm.generate_response(
            prompt
        )

        strategy_value = response.strip().lower()

        try:
            return DebateStrategy(strategy_value)
        except ValueError as exc:
            raise RuntimeError(
                "LLM returned an invalid debate strategy: "
                f"{strategy_value!r}"
            ) from exc