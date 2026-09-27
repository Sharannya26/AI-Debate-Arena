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


def test_consistency_analyzer_requires_arguments():
    analyzer = ConsistencyAnalyzer()

    result = analyzer.analyze([])

    assert (
        result.consistency
        == "Not enough arguments to determine consistency."
    )


def test_consistency_analyzer_detects_shared_keywords():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "Students can use social media for education.",
            1,
        ),
        create_user_argument(
            "Social media can help students learn.",
            2,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert result.consistency == "Highly consistent."
    assert len(result.consistent_points) == 1
    assert len(result.inconsistent_points) == 0


def test_consistency_analyzer_detects_missing_keyword_overlap():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "Students can use social media for education.",
            1,
        ),
        create_user_argument(
            "Public transportation reduces traffic congestion.",
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


def test_non_user_argument_is_rejected():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "Students can use social media for education.",
            1,
        ),
        Argument(
            speaker="ai",
            text="Social media has risks.",
            round=2,
            turn=1,
        ),
    ]

    with pytest.raises(
        ValueError,
        match="All arguments must be from the user",
    ):
        analyzer.analyze(arguments)


def test_none_argument_is_rejected():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "Students can use social media for education.",
            1,
        ),
        None,
    ]

    with pytest.raises(
        ValueError,
        match="User arguments cannot contain None",
    ):
        analyzer.analyze(arguments)


def test_two_consistent_comparisons_are_mostly_consistent():
    analyzer = ConsistencyAnalyzer()

    arguments = [
        create_user_argument(
            "Students should learn online.",
            1,
        ),
        create_user_argument(
            "Online learning helps students.",
            2,
        ),
        create_user_argument(
            "Public transport reduces pollution.",
            3,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert result.consistency == "Mostly consistent."
    assert len(result.consistent_points) == 1
    assert len(result.inconsistent_points) == 1