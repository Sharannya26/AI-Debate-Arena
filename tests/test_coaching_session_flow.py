from debate_arena.debate.coaching_profile import CoachingProfile
from debate_arena.debate.coaching_session_report import (
    CoachingSessionReport,
)
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)
from debate_arena.debate.actionable_coaching_recommendation import (
    ActionableCoachingRecommendation,
)
from debate_arena.debate.practice_exercise import (
    PracticeExercise,
)


def test_complete_coaching_session_report_flow():
    coaching_profile = CoachingProfile(
        strengths=["Clear argument structure"],
        improvement_areas=["Evidence usage"],
        coaching_priorities=["Use stronger evidence"],
        strongest_moments=["Strong opening argument"],
        weakest_moments=["Weak supporting evidence"],
        overall_coaching_summary=(
            "The user communicates clearly but should "
            "strengthen evidence usage."
        ),
    )

    improvement_priority = (
        PersonalizedImprovementPriority(
            priority="Strengthen evidence usage",
            reason=(
                "Several claims lacked concrete supporting evidence."
            ),
            focus_area="evidence usage",
            supporting_evidence=[
                "Round 2 contained unsupported claims."
            ],
        )
    )

    recommendation = ActionableCoachingRecommendation(
        recommendation="Support each major claim with evidence.",
        reason=(
            "Evidence will make the user's arguments more convincing."
        ),
        action=(
            "Include one fact, example, or statistic with each "
            "major claim."
        ),
        related_priority="Strengthen evidence usage",
    )

    exercise = PracticeExercise(
        exercise="Evidence Sprint",
        objective=(
            "Practice supporting claims with concrete evidence."
        ),
        instructions=(
            "Make three short claims and provide one piece "
            "of evidence for each."
        ),
        related_priority="Strengthen evidence usage",
    )

    report = CoachingSessionReport(
        coaching_profile=coaching_profile,
        improvement_priorities=[improvement_priority],
        recommendations=[recommendation],
        practice_exercises=[exercise],
        session_summary=(
            coaching_profile.overall_coaching_summary
        ),
    )

    assert report.coaching_profile is coaching_profile

    assert len(report.improvement_priorities) == 1
    assert (
        report.improvement_priorities[0]
        is improvement_priority
    )

    assert len(report.recommendations) == 1
    assert report.recommendations[0] is recommendation

    assert len(report.practice_exercises) == 1
    assert report.practice_exercises[0] is exercise

    assert report.session_summary == (
        "The user communicates clearly but should "
        "strengthen evidence usage."
    )


def test_coaching_session_report_preserves_complete_structure():
    coaching_profile = CoachingProfile(
        strengths=["Strong responsiveness"],
        improvement_areas=["Reasoning quality"],
        coaching_priorities=["Improve reasoning"],
        strongest_moments=["Direct rebuttal"],
        weakest_moments=["Unclear logical connection"],
        overall_coaching_summary="Improve logical reasoning.",
    )

    priority = PersonalizedImprovementPriority(
        priority="Improve reasoning",
        reason="Logical connections were sometimes unclear.",
        focus_area="reasoning quality",
        supporting_evidence=[
            "The conclusion was not always directly connected "
            "to the evidence."
        ],
    )

    recommendation = ActionableCoachingRecommendation(
        recommendation="Explain the link between evidence and conclusion.",
        reason="This will make reasoning easier to follow.",
        action=(
            "After giving evidence, explicitly explain how it "
            "supports the conclusion."
        ),
        related_priority="Improve reasoning",
    )

    exercise = PracticeExercise(
        exercise="Reasoning Chain",
        objective="Build clearer logical connections.",
        instructions=(
            "Give a claim, supporting evidence, and one sentence "
            "explaining the connection."
        ),
        related_priority="Improve reasoning",
    )

    report = CoachingSessionReport(
        coaching_profile=coaching_profile,
        improvement_priorities=[priority],
        recommendations=[recommendation],
        practice_exercises=[exercise],
        session_summary="Improve logical reasoning.",
    )

    assert report.coaching_profile.strengths == [
        "Strong responsiveness"
    ]

    assert report.coaching_profile.improvement_areas == [
        "Reasoning quality"
    ]

    assert report.improvement_priorities[0].focus_area == (
        "reasoning quality"
    )

    assert report.recommendations[0].related_priority == (
        "Improve reasoning"
    )

    assert report.practice_exercises[0].related_priority == (
        "Improve reasoning"
    )