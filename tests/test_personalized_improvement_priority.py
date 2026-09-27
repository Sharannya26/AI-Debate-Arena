import pytest

from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)


def test_personalized_improvement_priority_stores_values():
    priority = PersonalizedImprovementPriority(
        priority="Improve evidence usage",
        reason="Evidence usage needs improvement.",
        focus_area="Support claims with concrete evidence.",
        supporting_evidence=[
            "Evidence usage declined across rounds.",
            "Some claims lacked supporting examples.",
        ],
    )

    assert priority.priority == "Improve evidence usage"
    assert priority.reason == "Evidence usage needs improvement."
    assert priority.focus_area == (
        "Support claims with concrete evidence."
    )
    assert priority.supporting_evidence == [
        "Evidence usage declined across rounds.",
        "Some claims lacked supporting examples.",
    ]


def test_personalized_improvement_priority_strips_text():
    priority = PersonalizedImprovementPriority(
        priority="  Improve reasoning  ",
        reason="  Reasoning needs improvement.  ",
        focus_area="  Make logical connections clearer.  ",
        supporting_evidence=[
            "  Weak logical connection.  ",
            "",
            "   ",
        ],
    )

    assert priority.priority == "Improve reasoning"
    assert priority.reason == "Reasoning needs improvement."
    assert priority.focus_area == (
        "Make logical connections clearer."
    )
    assert priority.supporting_evidence == [
        "Weak logical connection.",
    ]


def test_personalized_improvement_priority_rejects_empty_priority():
    with pytest.raises(
        ValueError,
        match="Improvement priority cannot be empty.",
    ):
        PersonalizedImprovementPriority(
            priority="",
            reason="Needs improvement.",
            focus_area="Evidence.",
        )


def test_personalized_improvement_priority_rejects_empty_reason():
    with pytest.raises(
        ValueError,
        match="Improvement priority reason cannot be empty.",
    ):
        PersonalizedImprovementPriority(
            priority="Improve evidence usage",
            reason="",
            focus_area="Evidence.",
        )


def test_personalized_improvement_priority_rejects_empty_focus_area():
    with pytest.raises(
        ValueError,
        match="Improvement priority focus area cannot be empty.",
    ):
        PersonalizedImprovementPriority(
            priority="Improve evidence usage",
            reason="Needs improvement.",
            focus_area="",
        )