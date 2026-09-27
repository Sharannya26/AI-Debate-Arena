from dataclasses import dataclass

from debate_arena.debate.speaking_pace import SpeakingPace


@dataclass
class CommunicationMetrics:
    """
    Objective communication metrics calculated from a speech sample.

    These metrics are intentionally deterministic and are calculated
    by Python rather than by the LLM.
    """

    word_count: int
    sentence_count: int
    duration: float
    words_per_minute: float
    average_words_per_sentence: float
    speaking_pace: SpeakingPace

    def __post_init__(self) -> None:
        if self.word_count < 0:
            raise ValueError(
                "Word count cannot be negative."
            )

        if self.sentence_count < 0:
            raise ValueError(
                "Sentence count cannot be negative."
            )

        if self.duration < 0:
            raise ValueError(
                "Duration cannot be negative."
            )

        if self.words_per_minute < 0:
            raise ValueError(
                "Words per minute cannot be negative."
            )

        if self.average_words_per_sentence < 0:
            raise ValueError(
                "Average words per sentence cannot be negative."
            )