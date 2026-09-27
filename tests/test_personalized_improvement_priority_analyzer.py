import pytest

from debate_arena.debate.coaching_profile import CoachingProfile
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)
from debate_arena.debate.personalized_improvement_priority_analyzer import (
    PersonalizedImprovementPriorityAnalyzer,
)


def test_analyzer_builds_personalized_priority():
    analyzer = (
        PersonalizedImprovementPriorityAnalyzer()
    )

    profile = CoachingProfile(
        strengths=[],
        improvement_areas=[
            "evidence usage: Evidence usage declined across rounds."
        ],
        coaching_priorities=[
            "evidence usage: Support major claims with concrete evidence."
        ],
        strongest_moments=[],
        weakest_moments=[
            "Unsupported claim in Round 1."
        ],
        overall_coaching_summary="Focus on evidence usage.",
    )

    result = analyzer.analyze(profile)

    assert len(result) == 1
    assert isinstance(
        result[0],
        PersonalizedImprovementPriority,
    )
    assert result[0].priority == (
        "Improve evidence usage"
    )
    assert "Evidence usage declined" in (
        result[0].reason
    )
    assert result[0].focus_area == (
        "evidence usage: Support major claims with concrete evidence."
    )
    assert (
        "Unsupported claim in Round 1."
        in result[0].supporting_evidence
    )


def test_analyzer_uses_improvement_area_without_matching_priority():
    analyzer = (
        PersonalizedImprovementPriorityAnalyzer()
    )

    profile = CoachingProfile(
        improvement_areas=[
            "reasoning quality: Logical connections varied across rounds."
        ],
        coaching_priorities=[],
        weakest_moments=[
            "Conclusion was not clearly connected to the claim."
        ],
    )

    result = analyzer.analyze(profile)

    assert len(result) == 1
    assert result[0].priority == (
        "Improve reasoning quality"
    )
    assert result[0].reason == (
        "Logical connections varied across rounds."
    )
    assert result[0].focus_area == (
        "Strengthen reasoning quality during future debates."
    )


def test_analyzer_includes_weakest_moments_as_supporting_evidence():
    analyzer = (
        PersonalizedImprovementPriorityAnalyzer()
    )

    profile = CoachingProfile(
        improvement_areas=[
            "communication quality: Communication varied across rounds."
        ],
        coaching_priorities=[],
        weakest_moments=[
            "Long and unclear response in Round 1.",
            "Main point was difficult to identify.",
        ],
    )

    result = analyzer.analyze(profile)

    assert len(result) == 1
    assert result[0].supporting_evidence == [
        "Communication varied across rounds.",
        "Long and unclear response in Round 1.",
        "Main point was difficult to identify.",
    ]


def test_analyzer_returns_empty_list_when_no_improvement_areas():
    analyzer = (
        PersonalizedImprovementPriorityAnalyzer()
    )

    profile = CoachingProfile(
        strengths=["Clear reasoning."],
        improvement_areas=[],
        coaching_priorities=[
            "Continue maintaining strong reasoning."
        ],
    )

    result = analyzer.analyze(profile)

    assert result == []


def test_analyzer_rejects_none_profile():
    analyzer = (
        PersonalizedImprovementPriorityAnalyzer()
    )

    with pytest.raises(
        ValueError,
        match="Coaching profile cannot be None.",
    ):
        analyzer.analyze(None)