import pytest

from debate_arena.debate.communication_analyzer import (
    CommunicationAnalyzer,
)
from debate_arena.debate.speaking_pace import SpeakingPace
from debate_arena.debate.speech_sample import SpeechSample


def create_sample(
    text: str,
    duration: float = 10.0,
) -> SpeechSample:
    return SpeechSample(
        text=text,
        duration=duration,
        round=1,
        turn=1,
    )


def test_analyzer_counts_words():
    sample = create_sample(
        "This is a simple test."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.word_count == 5


def test_analyzer_counts_sentences():
    sample = create_sample(
        "This is one sentence. This is another sentence."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 2


def test_analyzer_preserves_duration():
    sample = create_sample(
        "This is a test.",
        duration=5.0,
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.duration == 5.0


def test_analyzer_calculates_wpm():
    sample = create_sample(
        "One two three four five.",
        duration=10.0,
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.words_per_minute == pytest.approx(30.0)


def test_analyzer_calculates_average_words_per_sentence():
    sample = create_sample(
        "One two three. Four five six.",
        duration=10.0,
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.average_words_per_sentence == pytest.approx(3.0)


def test_analyzer_handles_question_and_exclamation():
    sample = create_sample(
        "Are you ready? Yes, I am!"
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 2


def test_analyzer_handles_zero_duration():
    sample = create_sample(
        "This is a test.",
        duration=0.0,
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.words_per_minute == 0.0
    assert metrics.speaking_pace == SpeakingPace.SLOW


def test_analyzer_rejects_none_sample():
    analyzer = CommunicationAnalyzer()

    with pytest.raises(
        ValueError,
        match="Speech sample cannot be None",
    ):
        analyzer.analyze(None)


def test_analyzer_handles_exclamation_mark():
    sample = create_sample(
        "This is great!"
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 1


def test_analyzer_handles_question_mark():
    sample = create_sample(
        "Is this working?"
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 1


def test_analyzer_handles_multiple_punctuation_marks():
    sample = create_sample(
        "Really?! Yes!! Absolutely!!!"
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 3


def test_analyzer_handles_ellipsis():
    sample = create_sample(
        "Well... I think this works."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 2


def test_analyzer_handles_punctuation_attached_to_words():
    sample = create_sample(
        "Hello, world! This works."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.word_count == 4
    assert metrics.sentence_count == 2


def test_analyzer_classifies_slow_speaking_pace():
    sample = create_sample(
        "One two three four five.",
        duration=5.0,
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.words_per_minute == pytest.approx(60.0)
    assert metrics.speaking_pace == SpeakingPace.SLOW


def test_analyzer_classifies_moderate_speaking_pace():
    sample = create_sample(
        "One two three four five six seven eight nine ten.",
        duration=5.0,
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.words_per_minute == pytest.approx(120.0)
    assert metrics.speaking_pace == SpeakingPace.MODERATE


def test_analyzer_classifies_fast_speaking_pace():
    sample = create_sample(
        "One two three four five six seven eight nine ten.",
        duration=3.0,
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.words_per_minute == pytest.approx(200.0)
    assert metrics.speaking_pace == SpeakingPace.FAST