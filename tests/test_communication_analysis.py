import pytest

from debate_arena.debate.communication_analysis import CommunicationAnalysis
from debate_arena.debate.communication_metrics import CommunicationMetrics
from debate_arena.debate.filler_metrics import FillerMetrics
from debate_arena.debate.speaking_pace import SpeakingPace


def create_communication_metrics() -> CommunicationMetrics:
    return CommunicationMetrics(
        word_count=20,
        sentence_count=2,
        duration=10.0,
        words_per_minute=120.0,
        average_words_per_sentence=10.0,
        speaking_pace=SpeakingPace.MODERATE,
    )


def create_filler_metrics() -> FillerMetrics:
    return FillerMetrics(
        total_filler_count=3,
        filler_counts={
            "um": 2,
            "like": 1,
        },
        total_word_count=20,
        filler_rate=3 / 20,
    )


def create_analysis() -> CommunicationAnalysis:
    return CommunicationAnalysis(
        communication_metrics=create_communication_metrics(),
        filler_metrics=create_filler_metrics(),
    )


def test_communication_analysis_stores_metrics():
    analysis = create_analysis()

    assert analysis.communication_metrics.word_count == 20
    assert analysis.filler_metrics.total_filler_count == 3


def test_word_count_property():
    analysis = create_analysis()

    assert analysis.word_count == 20


def test_sentence_count_property():
    analysis = create_analysis()

    assert analysis.sentence_count == 2


def test_duration_property():
    analysis = create_analysis()

    assert analysis.duration == 10.0


def test_words_per_minute_property():
    analysis = create_analysis()

    assert analysis.words_per_minute == 120.0


def test_speaking_pace_property():
    analysis = create_analysis()

    assert analysis.speaking_pace == SpeakingPace.MODERATE


def test_average_words_per_sentence_property():
    analysis = create_analysis()

    assert analysis.average_words_per_sentence == 10.0


def test_total_filler_count_property():
    analysis = create_analysis()

    assert analysis.total_filler_count == 3


def test_filler_counts_property():
    analysis = create_analysis()

    assert analysis.filler_counts == {
        "um": 2,
        "like": 1,
    }


def test_filler_rate_property():
    analysis = create_analysis()

    assert analysis.filler_rate == pytest.approx(0.15)