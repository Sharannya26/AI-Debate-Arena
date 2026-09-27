from debate_arena.debate.coaching_session_report import (
    CoachingSessionReport,
)


def build_coaching_view_data(
    report: CoachingSessionReport,
) -> dict:
    """
    Convert a CoachingSessionReport into frontend-ready data.

    This function only prepares presentation data.
    It does not perform analysis, call Gemini, or modify
    the coaching report.
    """

    if report is None:
        raise ValueError(
            "Coaching session report cannot be None."
        )

    profile = report.coaching_profile

    return {
        "session_summary": report.session_summary,
        "profile": {
            "strengths": list(profile.strengths),
            "improvement_areas": list(
                profile.improvement_areas
            ),
            "coaching_priorities": list(
                profile.coaching_priorities
            ),
            "strongest_moments": list(
                profile.strongest_moments
            ),
            "weakest_moments": list(
                profile.weakest_moments
            ),
            "overall_coaching_summary": (
                profile.overall_coaching_summary
            ),
        },
        "priorities": [
            {
                "priority": item.priority,
                "reason": item.reason,
                "focus_area": item.focus_area,
                "supporting_evidence": list(
                    item.supporting_evidence
                ),
            }
            for item in report.improvement_priorities
        ],
        "recommendations": [
            {
                "recommendation": item.recommendation,
                "reason": item.reason,
                "action": item.action,
                "related_priority": item.related_priority,
            }
            for item in report.recommendations
        ],
        "practice_exercises": [
            {
                "exercise": item.exercise,
                "objective": item.objective,
                "instructions": item.instructions,
                "related_priority": item.related_priority,
            }
            for item in report.practice_exercises
        ],
    }