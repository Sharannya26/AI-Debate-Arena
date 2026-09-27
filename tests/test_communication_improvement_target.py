from debate_arena.debate.communication_improvement_target import (
    CommunicationImprovementTarget,
)


def test_filler_words_target() -> None:
    assert (
        CommunicationImprovementTarget.FILLER_WORDS.value
        == "filler_words"
    )


def test_speaking_pace_target() -> None:
    assert (
        CommunicationImprovementTarget.SPEAKING_PACE.value
        == "speaking_pace"
    )


def test_sentence_length_target() -> None:
    assert (
        CommunicationImprovementTarget.SENTENCE_LENGTH.value
        == "sentence_length"
    )


def test_argument_delivery_target() -> None:
    assert (
        CommunicationImprovementTarget.ARGUMENT_DELIVERY.value
        == "argument_delivery"
    )


def test_overall_clarity_target() -> None:
    assert (
        CommunicationImprovementTarget.OVERALL_CLARITY.value
        == "overall_clarity"
    )


def test_target_is_string_compatible() -> None:
    target = CommunicationImprovementTarget.FILLER_WORDS

    assert isinstance(target, str)
    assert target == "filler_words"


def test_target_from_string() -> None:
    target = CommunicationImprovementTarget(
        "speaking_pace"
    )

    assert target == (
        CommunicationImprovementTarget.SPEAKING_PACE
    )