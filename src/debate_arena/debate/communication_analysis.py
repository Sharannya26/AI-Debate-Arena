from dataclasses import dataclass

from debate_arena.debate.communication_metrics import CommunicationMetrics
from debate_arena.debate.filler_metrics import FillerMetrics


@dataclass
class CommunicationAnalysis:
    """
    Structured communication analysis for one speech sample.

    This object combines objective communication measurements
    calculated by Python.

    Interpretation and qualitative feedback will be handled
    later by Gemini.
    """

    communication_metrics: CommunicationMetrics
    filler_metrics: FillerMetrics

    @property
    def word_count(self) -> int:
        """Return the total number of words spoken."""
        return self.communication_metrics.word_count

    @property
    def sentence_count(self) -> int:
        """Return the total number of sentences spoken."""
        return self.communication_metrics.sentence_count

    @property
    def duration(self) -> float:
        """Return the speech duration in seconds."""
        return self.communication_metrics.duration

    @property
    def words_per_minute(self) -> float:
        """Return the speaking rate in words per minute."""
        return self.communication_metrics.words_per_minute

    @property
    def speaking_pace(self):
        """Return the classified speaking pace."""
        return self.communication_metrics.speaking_pace

    @property
    def average_words_per_sentence(self) -> float:
        """Return the average sentence length."""
        return self.communication_metrics.average_words_per_sentence

    @property
    def total_filler_count(self) -> int:
        """Return the total number of detected filler words."""
        return self.filler_metrics.total_filler_count

    @property
    def filler_counts(self) -> dict[str, int]:
        """Return filler-word counts by filler."""
        return self.filler_metrics.filler_counts

    @property
    def filler_rate(self) -> float:
        """Return the proportion of words that were fillers."""
        return self.filler_metrics.filler_rate