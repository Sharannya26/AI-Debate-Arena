import pytest

from debate_arena.debate.communication_metrics import CommunicationMetrics
from debate_arena.debate.speaking_pace import SpeakingPace


def create_metrics() -> CommunicationMetrics:
    return CommunicationMetrics(
        word_count=20,
        sentence_count=2,
        duration=10.0,
        words_per_minute=120.0,
        average_words_per_sentence=10.0,
        speaking_pace=SpeakingPace.MODERATE,
    )


def test_communication_metrics_stores_data():
    metrics = create_metrics()

    assert metrics.word_count == 20
    assert metrics.sentence_count == 2
    assert metrics.duration == 10.0
    assert metrics.words_per_minute == 120.0
    assert metrics.average_words_per_sentence == 10.0
    assert metrics.speaking_pace == SpeakingPace.MODERATE


def test_communication_metrics_rejects_negative_word_count():
    with pytest.raises(
        ValueError,
        match="Word count cannot be negative",
    ):
        CommunicationMetrics(
            word_count=-1,
            sentence_count=2,
            duration=10.0,
            words_per_minute=120.0,
            average_words_per_sentence=10.0,
            speaking_pace=SpeakingPace.MODERATE,
        )


def test_communication_metrics_rejects_negative_sentence_count():
    with pytest.raises(
        ValueError,
        match="Sentence count cannot be negative",
    ):
        CommunicationMetrics(
            word_count=20,
            sentence_count=-1,
            duration=10.0,
            words_per_minute=120.0,
            average_words_per_sentence=10.0,
            speaking_pace=SpeakingPace.MODERATE,
        )


def test_communication_metrics_rejects_negative_duration():
    with pytest.raises(
        ValueError,
        match="Duration cannot be negative",
    ):
        CommunicationMetrics(
            word_count=20,
            sentence_count=2,
            duration=-1.0,
            words_per_minute=120.0,
            average_words_per_sentence=10.0,
            speaking_pace=SpeakingPace.MODERATE,
        )


def test_communication_metrics_rejects_negative_wpm():
    with pytest.raises(
        ValueError,
        match="Words per minute cannot be negative",
    ):
        CommunicationMetrics(
            word_count=20,
            sentence_count=2,
            duration=10.0,
            words_per_minute=-1.0,
            average_words_per_sentence=10.0,
            speaking_pace=SpeakingPace.MODERATE,
        )


def test_communication_metrics_rejects_negative_average_sentence_length():
    with pytest.raises(
        ValueError,
        match="Average words per sentence cannot be negative",
    ):
        CommunicationMetrics(
            word_count=20,
            sentence_count=2,
            duration=10.0,
            words_per_minute=120.0,
            average_words_per_sentence=-1.0,
            speaking_pace=SpeakingPace.MODERATE,
        )