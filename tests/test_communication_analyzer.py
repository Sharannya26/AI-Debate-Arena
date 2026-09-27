import pytest

from debate_arena.debate.communication_analyzer import CommunicationAnalyzer
from debate_arena.debate.speech_sample import SpeechSample


def create_sample(text: str, duration: float = 10.0) -> SpeechSample:
    return SpeechSample(
        text=text,
        duration=duration,
        round=1,
        turn=1,
    )


def test_analyzer_counts_words():
    sample = create_sample(
        "Social media can help students."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.word_count == 5


def test_analyzer_counts_sentences():
    sample = create_sample(
        "Social media can help students. "
        "It can also help them learn."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 2


def test_analyzer_preserves_duration():
    sample = create_sample(
        "Students can use technology for learning.",
        duration=12.5,
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.duration == 12.5


def test_analyzer_calculates_words_per_minute():
    sample = create_sample(
        "one two three four five",
        duration=10.0,
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.words_per_minute == 30.0


def test_analyzer_calculates_average_words_per_sentence():
    sample = create_sample(
        "Social media helps students. "
        "It provides educational resources."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 2
    assert metrics.word_count == 8
    assert metrics.average_words_per_sentence == 4.0


def test_analyzer_handles_question_and_exclamation_sentences():
    sample = create_sample(
        "Can students learn online? Yes! They can."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 3


def test_analyzer_handles_zero_duration():
    sample = create_sample(
        "Students can learn online.",
        duration=0.0,
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.words_per_minute == 0.0


def test_analyzer_rejects_none_sample():
    analyzer = CommunicationAnalyzer()

    with pytest.raises(
        ValueError,
        match="Speech sample cannot be None",
    ):
        analyzer.analyze(None)


def test_analyzer_handles_exclamation_mark():
    sample = create_sample(
        "This is important!"
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 1


def test_analyzer_handles_question_mark():
    sample = create_sample(
        "Should students use social media?"
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 1


def test_analyzer_handles_multiple_punctuation_marks():
    sample = create_sample(
        "Really?! This is useful."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 2


def test_analyzer_handles_ellipsis():
    sample = create_sample(
        "I think... this is useful."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.sentence_count == 2


def test_analyzer_handles_punctuation_attached_to_words():
    sample = create_sample(
        "Well, I think this is useful."
    )

    analyzer = CommunicationAnalyzer()

    metrics = analyzer.analyze(sample)

    assert metrics.word_count == 6
    assert metrics.sentence_count == 1