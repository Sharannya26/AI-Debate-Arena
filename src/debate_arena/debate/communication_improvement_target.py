from enum import Enum


class CommunicationImprovementTarget(str, Enum):
    """
    Represents the communication areas that can become
    personalized improvement targets.

    These targets are used by the coaching system to identify
    the main communication skill that the speaker should improve.
    """

    FILLER_WORDS = "filler_words"
    SPEAKING_PACE = "speaking_pace"
    SENTENCE_LENGTH = "sentence_length"
    ARGUMENT_DELIVERY = "argument_delivery"
    OVERALL_CLARITY = "overall_clarity"