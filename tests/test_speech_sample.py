import pytest

from debate_arena.debate.speech_sample import SpeechSample


def test_speech_sample_stores_data():
    sample = SpeechSample(
        text="  Social media can be harmful.  ",
        duration=12.5,
        round=1,
        turn=1,
    )

    assert sample.text == "Social media can be harmful."
    assert sample.duration == 12.5
    assert sample.round == 1
    assert sample.turn == 1


def test_speech_sample_rejects_empty_text():
    with pytest.raises(ValueError, match="Speech text cannot be empty"):
        SpeechSample(
            text="   ",
            duration=10.0,
            round=1,
            turn=1,
        )


def test_speech_sample_rejects_negative_duration():
    with pytest.raises(
        ValueError,
        match="Speech duration cannot be negative",
    ):
        SpeechSample(
            text="This is an argument.",
            duration=-1.0,
            round=1,
            turn=1,
        )


def test_speech_sample_rejects_invalid_round():
    with pytest.raises(ValueError, match="Round must be at least 1"):
        SpeechSample(
            text="This is an argument.",
            duration=10.0,
            round=0,
            turn=1,
        )


def test_speech_sample_rejects_invalid_turn():
    with pytest.raises(ValueError, match="Turn must be at least 1"):
        SpeechSample(
            text="This is an argument.",
            duration=10.0,
            round=1,
            turn=0,
        )