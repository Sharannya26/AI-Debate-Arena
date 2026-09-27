from debate_arena.debate.actionable_coaching_recommendation import (
    ActionableCoachingRecommendation,
)
from debate_arena.debate.coaching_session_report import (
    CoachingSessionReport,
)
from debate_arena.debate.coaching_profile import (
    CoachingProfile,
)
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)
from debate_arena.debate.practice_exercise import (
    PracticeExercise,
)

from debate_arena.frontend.coaching_view import (
    build_coaching_view_data,
)


def build_report() -> CoachingSessionReport:
    profile = CoachingProfile(
        strengths=["Clear reasoning"],
        improvement_areas=["Evidence usage"],
        coaching_priorities=["Use stronger evidence"],
        strongest_moments=["Round 1"],
        weakest_moments=["Round 2"],
        overall_coaching_summary=(
            "The user communicates clearly but should "
            "strengthen evidence usage."
        ),
    )

    priority = PersonalizedImprovementPriority(
        priority="Improve evidence usage",
        reason="Arguments need stronger support.",
        focus_area="Evidence usage",
        supporting_evidence=[
            "Several claims lacked concrete evidence."
        ],
    )

    recommendation = ActionableCoachingRecommendation(
        recommendation=(
            "Use one concrete example per claim."
        ),
        reason=(
            "Examples make arguments easier to support."
        ),
        action=(
            "Add a factual example before concluding."
        ),
        related_priority="Improve evidence usage",
    )

    exercise = PracticeExercise(
        exercise="Evidence Sprint",
        objective=(
            "Practice supporting claims with evidence."
        ),
        instructions=(
            "Make three claims and support each with "
            "one concrete example."
        ),
        related_priority="Improve evidence usage",
    )

    return CoachingSessionReport(
        coaching_profile=profile,
        improvement_priorities=[priority],
        recommendations=[recommendation],
        practice_exercises=[exercise],
        session_summary=(
            "Focused coaching session on evidence usage."
        ),
    )


def test_build_coaching_view_data():
    report = build_report()

    data = build_coaching_view_data(report)

    assert data["session_summary"] == (
        "Focused coaching session on evidence usage."
    )

    assert data["profile"]["strengths"] == [
        "Clear reasoning"
    ]

    assert data["profile"]["improvement_areas"] == [
        "Evidence usage"
    ]

    assert data["profile"]["coaching_priorities"] == [
        "Use stronger evidence"
    ]

    assert data["profile"]["strongest_moments"] == [
        "Round 1"
    ]

    assert data["profile"]["weakest_moments"] == [
        "Round 2"
    ]

    assert data["priorities"][0]["priority"] == (
        "Improve evidence usage"
    )

    assert data["priorities"][0]["focus_area"] == (
        "Evidence usage"
    )

    assert data["recommendations"][0][
        "recommendation"
    ] == "Use one concrete example per claim."

    assert data["practice_exercises"][0][
        "exercise"
    ] == "Evidence Sprint"


def test_build_coaching_view_data_rejects_none():
    try:
        build_coaching_view_data(None)
        assert False, (
            "Expected ValueError when report is None."
        )
    except ValueError as exc:
        assert str(exc) == (
            "Coaching session report cannot be None."
        )