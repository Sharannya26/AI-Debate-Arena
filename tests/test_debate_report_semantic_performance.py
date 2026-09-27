from debate_arena.debate.debate_report import DebateReport
from debate_arena.debate.semantic_performance_analysis import (
    SemanticPerformanceAnalysis,
)


def create_report():
    return DebateReport(
        topic="Should AI be used in education?",
        user_position="Support",
        ai_position="Oppose",
        rounds_completed=3,
        summary="The debate was completed.",
    )


def test_report_can_store_semantic_performance():
    analysis = SemanticPerformanceAnalysis(
        overall_interpretation=(
            "The user's performance became "
            "more structured."
        ),
        strengths_interpretation=(
            "Reasoning remained strong."
        ),
        weaknesses_interpretation=(
            "Evidence usage needs improvement."
        ),
        coaching_interpretation=(
            "Support claims with evidence."
        ),
        key_insights=[
            "Reasoning remained consistent.",
        ],
    )

    report = create_report()

    report.semantic_performance = analysis

    assert report.semantic_performance is analysis


def test_report_semantic_performance_defaults_to_none():
    report = create_report()

    assert report.semantic_performance is None


def test_existing_report_fields_remain_unchanged():
    report = create_report()

    assert report.topic == (
        "Should AI be used in education?"
    )

    assert report.user_position == "Support"

    assert report.ai_position == "Oppose"

    assert report.rounds_completed == 3

    assert report.summary == (
        "The debate was completed."
    )