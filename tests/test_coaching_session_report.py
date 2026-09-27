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


def build_profile() -> CoachingProfile:
    return CoachingProfile(
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


def build_priority() -> PersonalizedImprovementPriority:
    return PersonalizedImprovementPriority(
        priority="Improve evidence usage",
        reason="Arguments need stronger support.",
        focus_area="Evidence usage",
        supporting_evidence=[
            "Several claims lacked concrete evidence."
        ],
    )


def build_recommendation() -> ActionableCoachingRecommendation:
    return ActionableCoachingRecommendation(
        recommendation="Use one concrete example per claim.",
        reason="Examples make arguments easier to support.",
        action="Add a factual example before concluding.",
        related_priority="Improve evidence usage",
    )


def build_exercise() -> PracticeExercise:
    return PracticeExercise(
        exercise="Evidence Sprint",
        objective="Practice supporting claims with evidence.",
        instructions=(
            "Make three claims and support each with "
            "one concrete example."
        ),
        related_priority="Improve evidence usage",
    )


def test_coaching_session_report_stores_complete_session():
    profile = build_profile()
    priority = build_priority()
    recommendation = build_recommendation()
    exercise = build_exercise()

    report = CoachingSessionReport(
        coaching_profile=profile,
        improvement_priorities=[priority],
        recommendations=[recommendation],
        practice_exercises=[exercise],
        session_summary=(
            "Focused coaching session on evidence usage."
        ),
    )

    assert report.coaching_profile is profile
    assert report.improvement_priorities == [priority]
    assert report.recommendations == [recommendation]
    assert report.practice_exercises == [exercise]
    assert (
        report.session_summary
        == "Focused coaching session on evidence usage."
    )


def test_coaching_session_report_strips_session_summary():
    report = CoachingSessionReport(
        coaching_profile=build_profile(),
        session_summary=(
            "  Evidence usage needs improvement.  "
        ),
    )

    assert (
        report.session_summary
        == "Evidence usage needs improvement."
    )


def test_coaching_session_report_filters_none_items():
    priority = build_priority()
    recommendation = build_recommendation()
    exercise = build_exercise()

    report = CoachingSessionReport(
        coaching_profile=build_profile(),
        improvement_priorities=[
            priority,
            None,
        ],
        recommendations=[
            recommendation,
            None,
        ],
        practice_exercises=[
            exercise,
            None,
        ],
    )

    assert report.improvement_priorities == [priority]
    assert report.recommendations == [recommendation]
    assert report.practice_exercises == [exercise]


def test_coaching_session_report_requires_profile():
    try:
        CoachingSessionReport(
            coaching_profile=None,
        )
        assert False, (
            "Expected ValueError when coaching profile is None."
        )
    except ValueError as exc:
        assert str(exc) == (
            "Coaching profile cannot be None."
        )