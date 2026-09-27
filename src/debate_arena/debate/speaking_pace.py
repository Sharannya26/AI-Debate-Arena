from enum import Enum


class SpeakingPace(str, Enum):
    """
    Represents the speaking-pace categories used by the
    communication analysis system.
    """

    SLOW = "slow"
    MODERATE = "moderate"
    FAST = "fast"