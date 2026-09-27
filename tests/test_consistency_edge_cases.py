import pytest

from debate_arena.debate.argument import Argument
from debate_arena.debate.consistency_analyzer import (
    ConsistencyAnalyzer,
)


def create_user_argument(
    text: str,
    round_number: int,
) -> Argument:
    return Argument(
        speaker="user",
        text=text,
        round=round_number,
        turn=1,
    )


def test_consistency_ignores_capitalization_and_punctuation():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "Social media helps students learn!",
            1,
        ),
        create_user_argument(
            "SOCIAL MEDIA helps students learn.",
            2,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert result.consistency == "Highly consistent."
    assert len(result.consistent_points) == 1
    assert len(result.inconsistent_points) == 0


def test_consistency_detects_repeated_ideas_across_three_rounds():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "Students should have access to online education.",
            1,
        ),
        create_user_argument(
            "Online education gives students more opportunities.",
            2,
        ),
        create_user_argument(
            "Students benefit from online learning opportunities.",
            3,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert result.consistency == "Highly consistent."
    assert len(result.consistent_points) == 2
    assert len(result.inconsistent_points) == 0


def test_consistency_handles_short_arguments():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "Education matters.",
            1,
        ),
        create_user_argument(
            "Education matters.",
            2,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert result.consistency == "Highly consistent."
    assert len(result.consistent_points) == 1
    assert len(result.inconsistent_points) == 0


def test_consistency_handles_arguments_with_no_keywords():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "The the and and.",
            1,
        ),
        create_user_argument(
            "A an the.",
            2,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert (
        result.consistency
        == "No consistent keywords identified."
    )

    assert len(result.consistent_points) == 0
    assert len(result.inconsistent_points) == 1


def test_consistency_detects_mixed_rounds():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "Students need access to education.",
            1,
        ),
        create_user_argument(
            "Education gives students opportunities.",
            2,
        ),
        create_user_argument(
            "Public transport reduces traffic.",
            3,
        ),
        create_user_argument(
            "Public transport reduces pollution.",
            4,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert result.consistency == "Mostly consistent."

    assert len(result.consistent_points) == 2
    assert len(result.inconsistent_points) == 1


def test_consistency_preserves_round_numbers_in_findings():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "Students need education.",
            1,
        ),
        create_user_argument(
            "Students deserve education.",
            3,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert len(result.consistent_points) == 1

    assert (
        "Round 1 and Round 3"
        in result.consistent_points[0]
    )