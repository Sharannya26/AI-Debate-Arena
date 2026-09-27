import math

from debate_arena.debate.speaking_pace import SpeakingPace
from debate_arena.debate.speaking_pace_metrics import (
    SpeakingPaceMetrics,
)


class SpeakingPaceAnalyzer:
    """
    Analyzes speaking pace using words-per-minute measurements.

    The classification is deterministic so that objective speech
    measurements are not delegated to an LLM.
    """

    SLOW_THRESHOLD = 100.0
    FAST_THRESHOLD = 160.0

    @staticmethod
    def _validate_wpm(words_per_minute: float) -> None:
        """
        Validate a WPM measurement before analysis.
        """
        if math.isnan(words_per_minute):
            raise ValueError(
                "Words per minute cannot be NaN."
            )

        if words_per_minute < 0:
            raise ValueError(
                "Words per minute cannot be negative."
            )

    def analyze(
        self,
        words_per_minute: float,
    ) -> SpeakingPaceMetrics:
        """
        Convert a WPM measurement into SpeakingPaceMetrics.
        """
        self._validate_wpm(words_per_minute)

        return SpeakingPaceMetrics(
            words_per_minute=words_per_minute,
        )

    @classmethod
    def classify(
        cls,
        words_per_minute: float,
    ) -> SpeakingPace:
        """
        Classify speaking pace using deterministic thresholds.

        Categories:
        - slow: below 100 WPM
        - moderate: 100-159.99 WPM
        - fast: 160+ WPM
        """
        cls._validate_wpm(words_per_minute)

        if words_per_minute < cls.SLOW_THRESHOLD:
            return SpeakingPace.SLOW

        if words_per_minute >= cls.FAST_THRESHOLD:
            return SpeakingPace.FAST

        return SpeakingPace.MODERATE