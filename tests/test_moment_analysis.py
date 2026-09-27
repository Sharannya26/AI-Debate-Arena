import pytest

from debate_arena.debate.moment_analysis import MomentAnalysis


def test_moment_analysis_accepts_valid_data():
    analysis = MomentAnalysis(
        strongest_moments=[
            "Round 2 showed strong reasoning."
        ],
        weakest_moments=[
            "Round 1 lacked supporting evidence."
        ],
        key_insights=[
            "Reasoning became clearer in later rounds."
        ],
    )

    assert analysis.strongest_moments == [
        "Round 2 showed strong reasoning."
    ]

    assert analysis.weakest_moments == [
        "Round 1 lacked supporting evidence."
    ]

    assert analysis.key_insights == [
        "Reasoning became clearer in later rounds."
    ]


def test_moment_analysis_defaults_to_empty_lists():
    analysis = MomentAnalysis()

    assert analysis.strongest_moments == []
    assert analysis.weakest_moments == []
    assert analysis.key_insights == []


def test_moment_analysis_strips_whitespace():
    analysis = MomentAnalysis(
        strongest_moments=[
            "  Strong reasoning in round 2.  "
        ],
        weakest_moments=[
            "  Limited evidence in round 1.  "
        ],
        key_insights=[
            "  Later reasoning was clearer.  "
        ],
    )

    assert analysis.strongest_moments == [
        "Strong reasoning in round 2."
    ]

    assert analysis.weakest_moments == [
        "Limited evidence in round 1."
    ]

    assert analysis.key_insights == [
        "Later reasoning was clearer."
    ]


def test_moment_analysis_filters_empty_strongest_moments():
    analysis = MomentAnalysis(
        strongest_moments=[
            "",
            "   ",
            "Strong reasoning.",
        ]
    )

    assert analysis.strongest_moments == [
        "Strong reasoning."
    ]


def test_moment_analysis_filters_empty_weakest_moments():
    analysis = MomentAnalysis(
        weakest_moments=[
            "",
            "   ",
            "Limited evidence.",
        ]
    )

    assert analysis.weakest_moments == [
        "Limited evidence."
    ]


def test_moment_analysis_filters_empty_key_insights():
    analysis = MomentAnalysis(
        key_insights=[
            "",
            "   ",
            "Reasoning improved.",
        ]
    )

    assert analysis.key_insights == [
        "Reasoning improved."
    ]


def test_moment_analysis_handles_mixed_valid_and_empty_values():
    analysis = MomentAnalysis(
        strongest_moments=[
            "Strong argument.",
            "",
            "   ",
            "Clear response.",
        ],
        weakest_moments=[
            "",
            "Weak evidence.",
            "   ",
        ],
        key_insights=[
            "Useful insight.",
            "",
            "   ",
        ],
    )

    assert analysis.strongest_moments == [
        "Strong argument.",
        "Clear response.",
    ]

    assert analysis.weakest_moments == [
        "Weak evidence."
    ]

    assert analysis.key_insights == [
        "Useful insight."
    ]


def test_moment_analysis_does_not_require_any_moment():
    analysis = MomentAnalysis(
        strongest_moments=[],
        weakest_moments=[],
        key_insights=[],
    )

    assert analysis.strongest_moments == []
    assert analysis.weakest_moments == []
    assert analysis.key_insights == []