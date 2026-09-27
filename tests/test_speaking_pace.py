from debate_arena.debate.speaking_pace import SpeakingPace


def test_speaking_pace_contains_slow():
    assert SpeakingPace.SLOW.value == "slow"


def test_speaking_pace_contains_moderate():
    assert SpeakingPace.MODERATE.value == "moderate"


def test_speaking_pace_contains_fast():
    assert SpeakingPace.FAST.value == "fast"


def test_speaking_pace_is_string_compatible():
    assert SpeakingPace.FAST == "fast"