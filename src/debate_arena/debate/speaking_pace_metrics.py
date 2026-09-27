from dataclasses import dataclass


@dataclass
class SpeakingPaceMetrics:
    """
    Stores objective speaking-pace measurements.

    Speaking pace is measured in words per minute (WPM).
    """

    words_per_minute: float

    def __post_init__(self) -> None:
        if self.words_per_minute < 0:
            raise ValueError(
                "Words per minute cannot be negative."
            )