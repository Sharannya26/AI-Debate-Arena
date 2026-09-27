from debate_arena.debate.coaching_profile import CoachingProfile
from debate_arena.debate.coaching_profile_analyzer import (
    CoachingProfileAnalyzer,
)
from debate_arena.debate.performance_summary import (
    PerformanceSummary,
)


def test_analyzer_builds_coaching_profile():
    summary = PerformanceSummary(
        overall_summary="Performance improved.",
        dimension_summaries={
            "argument quality": (
                "Argument quality improved across rounds."
            ),
            "communication quality": (
                "Communication quality improved across rounds."
            ),
        },
        strongest_moments=[
            "Strong rebuttal in round 2."
        ],
        weakest_moments=[
            "Weak evidence in round 1."
        ],
        coaching_priorities=[
            "Use stronger evidence."
        ],
    )

    analyzer = CoachingProfileAnalyzer()

    profile = analyzer.analyze(summary)

    assert isinstance(profile, CoachingProfile)

    assert profile.strengths == [
        (
            "argument quality: "
            "Argument quality improved across rounds."
        ),
        (
            "communication quality: "
            "Communication quality improved across rounds."
        ),
    ]

    assert profile.improvement_areas == []

    assert profile.coaching_priorities == [
        "Use stronger evidence."
    ]

    assert profile.strongest_moments == [
        "Strong rebuttal in round 2."
    ]

    assert profile.weakest_moments == [
        "Weak evidence in round 1."
    ]

    assert profile.overall_coaching_summary == (
        "Maintain the identified strengths while "
        "continuing to develop overall debate skills."
    )


def test_analyzer_identifies_improvement_areas():
    summary = PerformanceSummary(
        overall_summary="Performance varied.",
        dimension_summaries={
            "evidence usage": (
                "Evidence usage declined across rounds."
            ),
            "responsiveness": (
                "Responsiveness varied across the debate."
            ),
        },
        coaching_priorities=[
            "Use stronger evidence."
        ],
    )

    analyzer = CoachingProfileAnalyzer()

    profile = analyzer.analyze(summary)

    assert profile.strengths == []

    assert profile.improvement_areas == [
        (
            "evidence usage: "
            "Evidence usage declined across rounds."
        ),
        (
            "responsiveness: "
            "Responsiveness varied across the debate."
        ),
    ]

    assert profile.overall_coaching_summary == (
        "Focus on the identified improvement areas "
        "and apply the recommended coaching priorities "
        "in future debates."
    )


def test_analyzer_handles_empty_summary_data():
    summary = PerformanceSummary(
        overall_summary="Baseline established.",
    )

    analyzer = CoachingProfileAnalyzer()

    profile = analyzer.analyze(summary)

    assert profile.strengths == []
    assert profile.improvement_areas == []
    assert profile.coaching_priorities == []
    assert profile.strongest_moments == []
    assert profile.weakest_moments == []
    assert profile.overall_coaching_summary == (
        "Use the current debate performance as a "
        "baseline for future coaching."
    )


def test_analyzer_rejects_none():
    analyzer = CoachingProfileAnalyzer()

    try:
        analyzer.analyze(None)
        assert False
    except ValueError as exc:
        assert str(exc) == (
            "Performance summary cannot be None."
        )