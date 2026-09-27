from debate_arena.debate.communication_analysis import (
    CommunicationAnalysis,
)
from debate_arena.debate.communication_feedback import (
    CommunicationFeedback,
)
from debate_arena.debate.communication_prompts import (
    build_communication_analysis_prompt,
)
from debate_arena.llm.client import LLMClient


class CommunicationGeminiAnalyzer:
    """
    Uses Gemini to interpret objective communication measurements.

    Python calculates the objective measurements.
    Gemini interprets those measurements and produces qualitative
    communication feedback.
    """

    def __init__(
        self,
        llm: LLMClient | None = None,
    ) -> None:
        self.llm = llm or LLMClient()

    def analyze(
        self,
        analysis: CommunicationAnalysis,
    ) -> CommunicationFeedback:
        """
        Analyze communication performance using Gemini.

        Python provides the objective measurements.
        Gemini interprets those measurements.
        The response is converted into CommunicationFeedback.
        """

        if analysis is None:
            raise ValueError(
                "Communication analysis cannot be None."
            )

        analysis_data = self._build_analysis_data(
            analysis
        )

        prompt = build_communication_analysis_prompt(
            analysis_data
        )

        response = self.llm.analyze_communication(
            prompt
        )

        if not isinstance(response, dict):
            raise ValueError(
                "Gemini communication analysis must be a dictionary."
            )

        return self._build_feedback(
            response
        )

    @staticmethod
    def _build_analysis_data(
        analysis: CommunicationAnalysis,
    ) -> dict:
        """
        Convert CommunicationAnalysis into the dictionary
        expected by the communication-analysis prompt.
        """

        return {
            "word_count": analysis.word_count,
            "sentence_count": analysis.sentence_count,
            "duration": analysis.duration,
            "words_per_minute": analysis.words_per_minute,
            "speaking_pace": analysis.speaking_pace.value,
            "average_words_per_sentence": (
                analysis.average_words_per_sentence
            ),
            "total_filler_count": (
                analysis.total_filler_count
            ),
            "filler_counts": analysis.filler_counts,
            "filler_rate": analysis.filler_rate,
        }

    @staticmethod
    def _build_feedback(
        response: dict,
    ) -> CommunicationFeedback:
        """
        Convert Gemini's structured response into
        CommunicationFeedback.
        """

        required_fields = (
            "clarity",
            "conciseness",
            "delivery",
            "strengths",
            "weaknesses",
            "recommendations",
        )

        missing_fields = [
            field
            for field in required_fields
            if field not in response
        ]

        if missing_fields:
            raise ValueError(
                "Gemini communication analysis is missing "
                f"required fields: {missing_fields}"
            )

        return CommunicationFeedback(
            clarity=response["clarity"],
            conciseness=response["conciseness"],
            delivery=response["delivery"],
            strengths=response["strengths"],
            weaknesses=response["weaknesses"],
            recommendations=response["recommendations"],
        )