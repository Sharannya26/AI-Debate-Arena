import pytest

from debate_arena.debate.argument import Argument
from debate_arena.debate.responsiveness_analyzer import (
    ResponsivenessAnalyzer,
)


def make_ai_argument(text: str) -> Argument:
    return Argument(
        speaker="ai",
        text=text,
        round=1,
        turn=1,
    )


def make_user_argument(text: str) -> Argument:
    return Argument(
        speaker="user",
        text=text,
        round=1,
        turn=2,
    )


def test_highly_responsive_argument():
    analyzer = ResponsivenessAnalyzer()

    ai_argument = make_ai_argument(
        "Public transport is unreliable and expensive."
    )

    user_argument = make_user_argument(
        "Public transport is unreliable and expensive, "
        "but better scheduling can solve the problem."
    )

    result = analyzer.analyze(
        ai_argument,
        user_argument,
    )

    assert result.responsiveness == "Highly responsive."
    assert "public" in result.addressed_points
    assert "transport" in result.addressed_points


def test_partially_responsive_argument():
    analyzer = ResponsivenessAnalyzer()

    ai_argument = make_ai_argument(
        "Public transport is unreliable, expensive, slow, "
        "crowded, and inconvenient."
    )

    user_argument = make_user_argument(
        "Public transport can become more affordable "
        "with government subsidies."
    )

    result = analyzer.analyze(
        ai_argument,
        user_argument,
    )

    assert result.responsiveness == "Partially responsive."

def test_minimally_responsive_argument():
    analyzer = ResponsivenessAnalyzer()

    ai_argument = make_ai_argument(
        "Public transport is unreliable, expensive, slow, "
        "crowded, and inconvenient."
    )

    user_argument = make_user_argument(
        "Public services can be improved through better planning."
    )

    result = analyzer.analyze(
        ai_argument,
        user_argument,
    )

    assert result.responsiveness == "Minimally responsive."


def test_not_directly_responsive_argument():
    analyzer = ResponsivenessAnalyzer()

    ai_argument = make_ai_argument(
        "Public transport is unreliable and expensive."
    )

    user_argument = make_user_argument(
        "Private vehicles provide greater personal convenience."
    )

    result = analyzer.analyze(
        ai_argument,
        user_argument,
    )

    assert result.responsiveness == "Not directly responsive."


def test_identifies_addressed_and_ignored_points():
    analyzer = ResponsivenessAnalyzer()

    ai_argument = make_ai_argument(
        "Public transport is unreliable and expensive."
    )

    user_argument = make_user_argument(
        "Public transport is expensive, but subsidies can reduce costs."
    )

    result = analyzer.analyze(
        ai_argument,
        user_argument,
    )

    assert "public" in result.addressed_points
    assert "transport" in result.addressed_points
    assert "expensive" in result.addressed_points

    assert "unreliable" in result.ignored_points


def test_stop_words_are_removed():
    analyzer = ResponsivenessAnalyzer()

    keywords = analyzer._extract_keywords(
        "The public transport system is very expensive."
    )

    assert "the" not in keywords
    assert "is" not in keywords
    assert "very" in keywords
    assert "public" in keywords
    assert "transport" in keywords
    assert "expensive" in keywords


def test_rejects_none_ai_argument():
    analyzer = ResponsivenessAnalyzer()

    user_argument = make_user_argument(
        "Public transport should be improved."
    )

    with pytest.raises(
        ValueError,
        match="Previous AI argument cannot be None.",
    ):
        analyzer.analyze(
            None,
            user_argument,
        )


def test_rejects_none_user_argument():
    analyzer = ResponsivenessAnalyzer()

    ai_argument = make_ai_argument(
        "Public transport should be improved."
    )

    with pytest.raises(
        ValueError,
        match="User argument cannot be None.",
    ):
        analyzer.analyze(
            ai_argument,
            None,
        )


def test_rejects_non_ai_previous_argument():
    analyzer = ResponsivenessAnalyzer()

    previous_argument = make_user_argument(
        "Public transport should be improved."
    )

    user_argument = make_user_argument(
        "Better buses would help."
    )

    with pytest.raises(
        ValueError,
        match="Previous argument must be from the AI.",
    ):
        analyzer.analyze(
            previous_argument,
            user_argument,
        )


def test_rejects_non_user_current_argument():
    analyzer = ResponsivenessAnalyzer()

    ai_argument = make_ai_argument(
        "Public transport should be improved."
    )

    current_argument = make_ai_argument(
        "Better buses would help."
    )

    with pytest.raises(
        ValueError,
        match="User argument must be from the user.",
    ):
        analyzer.analyze(
            ai_argument,
            current_argument,
        )


def test_handles_argument_with_no_keywords():
    analyzer = ResponsivenessAnalyzer()

    ai_argument = make_ai_argument(
        "The."
    )

    user_argument = make_user_argument(
        "And."
    )

    result = analyzer.analyze(
        ai_argument,
        user_argument,
    )

    assert result.responsiveness == (
        "Unable to determine responsiveness."
    )