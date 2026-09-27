import pytest

from debate_arena.debate.actionable_coaching_recommendation import (
    ActionableCoachingRecommendation,
)


def test_actionable_coaching_recommendation_stores_values():
    recommendation = ActionableCoachingRecommendation(
        recommendation=(
            "Support major claims with concrete evidence."
        ),
        reason=(
            "Evidence usage was identified as an "
            "improvement priority."
        ),
        action=(
            "Prepare one example or statistic "
            "for each major claim."
        ),
        related_priority="Improve evidence usage",
    )

    assert recommendation.recommendation == (
        "Support major claims with concrete evidence."
    )
    assert recommendation.reason == (
        "Evidence usage was identified as an "
        "improvement priority."
    )
    assert recommendation.action == (
        "Prepare one example or statistic "
        "for each major claim."
    )
    assert recommendation.related_priority == (
        "Improve evidence usage"
    )


def test_actionable_coaching_recommendation_strips_text():
    recommendation = ActionableCoachingRecommendation(
        recommendation=(
            "  Improve evidence usage.  "
        ),
        reason=(
            "  Evidence needs improvement.  "
        ),
        action=(
            "  Prepare supporting examples.  "
        ),
        related_priority=(
            "  Improve evidence usage  "
        ),
    )

    assert recommendation.recommendation == (
        "Improve evidence usage."
    )
    assert recommendation.reason == (
        "Evidence needs improvement."
    )
    assert recommendation.action == (
        "Prepare supporting examples."
    )
    assert recommendation.related_priority == (
        "Improve evidence usage"
    )


def test_recommendation_rejects_empty_recommendation():
    with pytest.raises(
        ValueError,
        match="Coaching recommendation cannot be empty.",
    ):
        ActionableCoachingRecommendation(
            recommendation="",
            reason="Needs improvement.",
            action="Practice.",
            related_priority="Improve evidence usage",
        )


def test_recommendation_rejects_empty_reason():
    with pytest.raises(
        ValueError,
        match="Coaching recommendation reason cannot be empty.",
    ):
        ActionableCoachingRecommendation(
            recommendation="Improve evidence usage.",
            reason="",
            action="Practice.",
            related_priority="Improve evidence usage",
        )


def test_recommendation_rejects_empty_action():
    with pytest.raises(
        ValueError,
        match="Coaching recommendation action cannot be empty.",
    ):
        ActionableCoachingRecommendation(
            recommendation="Improve evidence usage.",
            reason="Needs improvement.",
            action="",
            related_priority="Improve evidence usage",
        )


def test_recommendation_rejects_empty_related_priority():
    with pytest.raises(
        ValueError,
        match="Related priority cannot be empty.",
    ):
        ActionableCoachingRecommendation(
            recommendation="Improve evidence usage.",
            reason="Needs improvement.",
            action="Practice.",
            related_priority="",
        )