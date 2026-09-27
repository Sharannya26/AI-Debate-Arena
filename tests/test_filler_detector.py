import pytest

from debate_arena.debate.filler_detector import FillerWordDetector
from debate_arena.debate.speech_sample import SpeechSample


def create_sample(text: str) -> SpeechSample:
    return SpeechSample(
        text=text,
        duration=10.0,
        round=1,
        turn=1,
    )


def test_detector_detects_single_filler():
    sample = create_sample(
        "Um, I think social media is useful."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 1
    assert metrics.filler_counts == {
        "um": 1,
    }


def test_detector_detects_multiple_fillers():
    sample = create_sample(
        "Um, I think, like, social media is useful, uh."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 3
    assert metrics.filler_counts == {
        "um": 1,
        "like": 1,
        "uh": 1,
    }


def test_detector_counts_repeated_fillers():
    sample = create_sample(
        "Um, um, I think, like, like, this is useful."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 4
    assert metrics.filler_counts == {
        "um": 2,
        "like": 2,
    }


def test_detector_is_case_insensitive():
    sample = create_sample(
        "UM, I think this is, LIKE, useful."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 2
    assert metrics.filler_counts == {
        "um": 1,
        "like": 1,
    }


def test_detector_does_not_match_partial_words():
    sample = create_sample(
        "The umbrella is useful and unlike other options."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 0
    assert metrics.filler_counts == {}


def test_detector_detects_multi_word_filler():
    sample = create_sample(
        "You know, students can benefit from technology."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 1
    assert metrics.filler_counts == {
        "you know": 1,
    }


def test_detector_handles_no_fillers():
    sample = create_sample(
        "Students can use technology to improve learning."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 0
    assert metrics.filler_counts == {}


def test_detector_rejects_none_sample():
    detector = FillerWordDetector()

    with pytest.raises(
        ValueError,
        match="Speech sample cannot be None",
    ):
        detector.analyze(None)


def test_detector_handles_punctuation():
    sample = create_sample(
        "Um! I think, uh... this is useful, like?"
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 3
    assert metrics.filler_counts == {
        "um": 1,
        "uh": 1,
        "like": 1,
    }


def test_detector_handles_multiple_word_phrase_repetitions():
    sample = create_sample(
        "You know, I think, you know, this is useful."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 2
    assert metrics.filler_counts == {
        "you know": 2,
    }


def test_detector_supports_custom_filler_vocabulary():
    sample = create_sample(
        "Well, perhaps this is useful, maybe."
    )

    detector = FillerWordDetector(
        fillers=("well", "perhaps", "maybe"),
    )

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 3
    assert metrics.filler_counts == {
        "well": 1,
        "perhaps": 1,
        "maybe": 1,
    }


def test_detector_ignores_default_fillers_when_custom_vocabulary_is_used():
    sample = create_sample(
        "Um, well, I think this is useful."
    )

    detector = FillerWordDetector(
        fillers=("well",),
    )

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 1
    assert metrics.filler_counts == {
        "well": 1,
    }


def test_detector_calculates_total_word_count():
    sample = create_sample(
        "Um, I think this is useful."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_word_count == 6


def test_detector_calculates_filler_rate():
    sample = create_sample(
        "Um, I think this is useful."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 1
    assert metrics.total_word_count == 6
    assert metrics.filler_rate == pytest.approx(1 / 6)

def test_detector_handles_punctuation_only_text():
    sample = create_sample(
        "..."
    )

    detector = FillerWordDetector()

    metrics = detector.analyze(sample)

    assert metrics.total_filler_count == 0
    assert metrics.total_word_count == 1
    assert metrics.filler_rate == 0.0