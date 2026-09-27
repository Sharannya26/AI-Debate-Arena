from dataclasses import dataclass, field

from debate_arena.debate.history_extractor import DebateHistoryExtractor
from debate_arena.debate.state import DebateState
from debate_arena.llm.client import LLMClient


@dataclass
class DebateAnalysis:
    """Structured analysis of the user's performance across the debate."""

    summary: str
    strongest_argument: str = ""
    weakest_argument: str = ""
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    evidence_usage: str = ""
    consistency: str = ""
    responsiveness: str = ""
    recommendations: list[str] = field(default_factory=list)


class DebateAnalyzer:
    """Analyzes the user's complete debate performance."""

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        history_extractor: DebateHistoryExtractor | None = None,
    ):
        self.llm_client = llm_client or LLMClient()
        self.history_extractor = (
            history_extractor or DebateHistoryExtractor()
        )

    def analyze(self, state: DebateState) -> DebateAnalysis:
        """Analyze the complete debate."""

        if state is None:
            raise ValueError("Debate state cannot be None.")

        history = self.history_extractor.extract(state)

        if not history:
            raise ValueError(
                "Cannot analyze a debate with no history."
            )

        debate_data = {
            "topic": state.topic,
            "user_position": state.user_position,
            "ai_position": state.ai_position,
            "history": history,
        }

        data = self.llm_client.analyze_debate(
            debate_data
        )

        return DebateAnalysis(
            summary=data.get("summary", ""),
            strongest_argument=data.get(
                "strongest_argument",
                "",
            ),
            weakest_argument=data.get(
                "weakest_argument",
                "",
            ),
            strengths=data.get(
                "strengths",
                [],
            ),
            weaknesses=data.get(
                "weaknesses",
                [],
            ),
            evidence_usage=data.get(
                "evidence_usage",
                "",
            ),
            consistency=data.get(
                "consistency",
                "",
            ),
            responsiveness=data.get(
                "responsiveness",
                "",
            ),
            recommendations=data.get(
                "recommendations",
                [],
            ),
        )