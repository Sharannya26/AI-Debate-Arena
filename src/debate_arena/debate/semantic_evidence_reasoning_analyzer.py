from debate_arena.debate.argument import Argument
from debate_arena.debate.evidence_analysis import (
    EvidenceAnalysis,
)
from debate_arena.debate.evidence_reasoning_prompts import (
    build_evidence_reasoning_prompt,
)
from debate_arena.llm.client import LLMClient


class SemanticEvidenceReasoningAnalyzer:
    """
    Performs semantic evidence and reasoning analysis
    using an LLM.

    The deterministic analyzer remains responsible for
    objective keyword-based metrics.
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()

    def analyze(
        self,
        user_arguments: list[Argument],
    ) -> EvidenceAnalysis:
        if user_arguments is None:
            raise ValueError(
                "User arguments cannot be None."
            )

        if not user_arguments:
            raise ValueError(
                "At least one user argument is required."
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

        prompt = build_evidence_reasoning_prompt(
            [argument.text for argument in user_arguments]
        )

        data = self.llm_client.analyze_evidence_reasoning(
            prompt
        )

        return EvidenceAnalysis(
            evidence_quality=data.get(
                "evidence_quality",
                "Unable to determine evidence quality.",
            ),
            reasoning_quality=data.get(
                "reasoning_quality",
                "Unable to determine reasoning quality.",
            ),
            evidence_points=data.get(
                "evidence_points",
                [],
            ),
            missing_evidence=data.get(
                "missing_evidence",
                [],
            ),
            reasoning_points=data.get(
                "reasoning_points",
                [],
            ),
            reasoning_gaps=data.get(
                "reasoning_gaps",
                [],
            ),
        )