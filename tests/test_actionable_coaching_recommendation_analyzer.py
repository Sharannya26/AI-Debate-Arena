from debate_arena.debate.actionable_coaching_recommendation import (
    ActionableCoachingRecommendation,
)
from debate_arena.debate.actionable_coaching_recommendation_analyzer import (
    ActionableCoachingRecommendationAnalyzer,
)
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)


def test_analyzer_builds_evidence_recommendation():
    analyzer = (
        ActionableCoachingRecommendationAnalyzer()
    )

    priority = PersonalizedImprovementPriority(
        priority="Improve evidence usage",
        reason=(
            "Evidence usage declined across the debate."
        ),
        focus_area=(
            "Support major claims with concrete evidence."
        ),
    )

    recommendations = analyzer.analyze([priority])

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert isinstance(
        recommendation,
        ActionableCoachingRecommendation,
    )

    assert recommendation.related_priority == (
        "Improve evidence usage"
    )

    assert "evidence" in (
        recommendation.recommendation.lower()
    )

    assert recommendation.action


def test_analyzer_builds_responsiveness_recommendation():
    analyzer = (
        ActionableCoachingRecommendationAnalyzer()
    )

    priority = PersonalizedImprovementPriority(
        priority="Improve responsiveness",
        reason=(
            "Responsiveness varied across the debate."
        ),
        focus_area=(
            "Address the opponent's main point directly."
        ),
    )

    recommendations = analyzer.analyze([priority])

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation.related_priority == (
        "Improve responsiveness"
    )

    assert "opponent" in (
        recommendation.recommendation.lower()
    )

    assert recommendation.action


def test_analyzer_handles_multiple_priorities():
    analyzer = (
        ActionableCoachingRecommendationAnalyzer()
    )

    priorities = [
        PersonalizedImprovementPriority(
            priority="Improve evidence usage",
            reason="Evidence usage declined.",
            focus_area="Strengthen evidence usage.",
        ),
        PersonalizedImprovementPriority(
            priority="Improve reasoning quality",
            reason="Reasoning quality declined.",
            focus_area="Strengthen reasoning quality.",
        ),
    ]

    recommendations = analyzer.analyze(priorities)

    assert len(recommendations) == 2

    assert (
        recommendations[0].related_priority
        == "Improve evidence usage"
    )

    assert (
        recommendations[1].related_priority
        == "Improve reasoning quality"
    )


def test_analyzer_handles_unknown_dimension():
    analyzer = (
        ActionableCoachingRecommendationAnalyzer()
    )

    priority = PersonalizedImprovementPriority(
        priority="Improve debate preparation",
        reason=(
            "Preparation should be improved."
        ),
        focus_area="Improve debate preparation.",
    )

    recommendations = analyzer.analyze([priority])

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation.related_priority == (
        "Improve debate preparation"
    )

    assert recommendation.recommendation == (
        "Improve debate preparation"
    )

    assert recommendation.action


def test_analyzer_rejects_none_priorities():
    analyzer = (
        ActionableCoachingRecommendationAnalyzer()
    )

    try:
        analyzer.analyze(None)
        assert False
    except ValueError as exc:
        assert str(exc) == (
            "Improvement priorities cannot be None."
        )


def test_analyzer_rejects_none_priority_item():
    analyzer = (
        ActionableCoachingRecommendationAnalyzer()
    )

    try:
        analyzer.analyze([None])
        assert False
    except ValueError as exc:
        assert str(exc) == (
            "Improvement priorities cannot contain None."
        )