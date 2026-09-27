import re

from debate_arena.debate.communication_metrics import CommunicationMetrics
from debate_arena.debate.speaking_pace_analyzer import (
    SpeakingPaceAnalyzer,
)
from debate_arena.debate.speech_sample import SpeechSample


class CommunicationAnalyzer:
    """
    Calculates objective communication metrics from a SpeechSample.

    This class deliberately uses deterministic Python calculations.
    Interpretation of these metrics will be handled later by Gemini.
    """

    def __init__(
        self,
        speaking_pace_analyzer: SpeakingPaceAnalyzer | None = None,
    ) -> None:
        self.speaking_pace_analyzer = (
            speaking_pace_analyzer
            or SpeakingPaceAnalyzer()
        )

    def analyze(self, sample: SpeechSample) -> CommunicationMetrics:
        if sample is None:
            raise ValueError("Speech sample cannot be None.")

        text = sample.text.strip()

        word_count = self._count_words(text)
        sentence_count = self._count_sentences(text)

        words_per_minute = self._calculate_words_per_minute(
            word_count=word_count,
            duration=sample.duration,
        )

        average_words_per_sentence = (
            word_count / sentence_count
            if sentence_count > 0
            else 0.0
        )

        speaking_pace = self.speaking_pace_analyzer.classify(
            words_per_minute
        )

        return CommunicationMetrics(
            word_count=word_count,
            sentence_count=sentence_count,
            duration=sample.duration,
            words_per_minute=words_per_minute,
            average_words_per_sentence=average_words_per_sentence,
            speaking_pace=speaking_pace,
        )

    @staticmethod
    def _count_words(text: str) -> int:
        """
        Count words using whitespace-separated tokens.

        Punctuation attached to words does not create additional words.
        """
        if not text:
            return 0

        return len(text.split())

    @staticmethod
    def _count_sentences(text: str) -> int:
        """
        Count sentences using common sentence-ending punctuation.

        '.', '?' and '!' are treated as sentence boundaries.
        """
        if not text:
            return 0

        sentences = re.findall(
            r"[^.!?]+(?:[.!?]+|$)",
            text,
        )

        return len(
            [
                sentence
                for sentence in sentences
                if sentence.strip()
            ]
        )

    @staticmethod
    def _calculate_words_per_minute(
        word_count: int,
        duration: float,
    ) -> float:
        """
        Calculate speaking rate in words per minute.
        """
        if duration <= 0:
            return 0.0

        return (word_count / duration) * 60.0