from debate_arena.debate.argument_analyzer import (
    ArgumentAnalysis,
    ArgumentAnalyzer,
)
from debate_arena.debate.argument import Argument
from debate_arena.debate.communication_analyzer import (
    CommunicationAnalyzer,
)
from debate_arena.debate.responsiveness_analyzer import (
    ResponsivenessAnalyzer,
)
from debate_arena.debate.round_performance import RoundPerformance
from debate_arena.debate.speech_sample import SpeechSample


class RoundPerformanceAnalyzer:
    """
    Combines argument, communication, and responsiveness analysis
    into a round-level performance assessment.

    Responsiveness requires a previous AI argument. Therefore,
    responsiveness remains None when analyzing the first round.
    """

    def __init__(
        self,
        argument_analyzer: ArgumentAnalyzer | None = None,
        communication_analyzer: CommunicationAnalyzer | None = None,
        responsiveness_analyzer: ResponsivenessAnalyzer | None = None,
    ) -> None:
        self.argument_analyzer = (
            argument_analyzer or ArgumentAnalyzer()
        )

        self.communication_analyzer = (
            communication_analyzer or CommunicationAnalyzer()
        )

        self.responsiveness_analyzer = (
            responsiveness_analyzer or ResponsivenessAnalyzer()
        )

    def analyze(
        self,
        sample: SpeechSample,
        previous_ai_argument: Argument | None = None,
    ) -> RoundPerformance:
        """
        Analyze one user's debate speech.

        Args:
            sample:
                The user's speech sample.

            previous_ai_argument:
                The AI argument immediately preceding the user's
                response. This is optional because Round 1 has no
                previous AI argument.
        """

        if sample is None:
            raise ValueError("Speech sample cannot be None.")

        argument_analysis = self.argument_analyzer.analyze(
            sample.text
        )

        communication_metrics = self.communication_analyzer.analyze(
            sample
        )

        responsiveness = None

        if previous_ai_argument is not None:
            user_argument = Argument(
                speaker="user",
                text=sample.text,
                round=sample.round,
                turn=sample.turn,
            )

            responsiveness = (
                self.responsiveness_analyzer.analyze(
                    previous_ai_argument,
                    user_argument,
                ).responsiveness
            )

        return RoundPerformance(
            round=sample.round,
            argument_quality=self._argument_quality(
                argument_analysis
            ),
            communication_quality=self._communication_quality(
                communication_metrics
            ),
            evidence_usage=self._evidence_usage(
                argument_analysis
            ),
            reasoning_quality=self._reasoning_quality(
                argument_analysis
            ),
            responsiveness=responsiveness,
        )

    @staticmethod
    def _argument_quality(
        analysis: ArgumentAnalysis,
    ) -> str:
        if analysis.weaknesses:
            return "Argument contains identifiable weaknesses."

        if analysis.claim and analysis.reasoning:
            return (
                "Argument contains a clear claim "
                "supported by reasoning."
            )

        if analysis.claim:
            return "Argument contains a clear claim."

        return (
            "Argument structure could not be clearly established."
        )

    @staticmethod
    def _communication_quality(metrics) -> str:
        pace = metrics.speaking_pace.value

        if pace == "moderate":
            return "Speech was delivered at a moderate pace."

        if pace == "fast":
            return "Speech was delivered at a fast pace."

        return "Speech was delivered at a slow pace."

    @staticmethod
    def _evidence_usage(
        analysis: ArgumentAnalysis,
    ) -> str:
        if analysis.evidence:
            return (
                f"The argument used {len(analysis.evidence)} "
                "identified piece(s) of evidence."
            )

        return "No explicit evidence was identified."

    @staticmethod
    def _reasoning_quality(
        analysis: ArgumentAnalysis,
    ) -> str:
        if analysis.reasoning:
            return "Reasoning was identified in the argument."

        return "No explicit reasoning structure was identified."