from dataclasses import dataclass, field

from debate_arena.llm.client import LLMClient


@dataclass
class ArgumentAnalysis:
    """Structured analysis of a debate argument."""

    claim: str
    reasoning: str = ""
    assumptions: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    argument_type: str = "general"


class ArgumentAnalyzer:
    """
    Analyzes debate arguments using Gemini.

    The analyzer focuses only on understanding the argument.
    It does NOT generate the rebuttal.
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
    ):
        self.llm_client = llm_client or LLMClient()

    def analyze(
        self,
        argument: str,
    ) -> ArgumentAnalysis:
        if not argument or not argument.strip():
            raise ValueError(
                "Argument cannot be empty."
            )

        cleaned_argument = argument.strip()

        data = self.llm_client.analyze_argument(
            cleaned_argument
        )

        return ArgumentAnalysis(
            claim=data.get(
                "claim",
                cleaned_argument,
            ),
            reasoning=data.get(
                "reasoning",
                "",
            ),
            assumptions=data.get(
                "assumptions",
                [],
            ),
            evidence=data.get(
                "evidence",
                [],
            ),
            weaknesses=data.get(
                "weaknesses",
                [],
            ),
            argument_type=data.get(
                "argument_type",
                "general",
            ),
        )