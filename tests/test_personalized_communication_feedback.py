import pytest

from debate_arena.debate.communication_improvement_target import (
    CommunicationImprovementTarget,
)
from debate_arena.debate.personalized_communication_feedback import (
    PersonalizedCommunicationFeedback,
)


def test_personalized_feedback_creation() -> None:
    feedback = PersonalizedCommunicationFeedback(
        primary_focus=(
            CommunicationImprovementTarget.FILLER_WORDS
        ),
        improvement_goal="Reduce filler-word usage.",
        action_plan=[
            "Pause before answering.",
            "Replace filler words with silence.",
        ],
    )

    assert feedback.primary_focus == (
        CommunicationImprovementTarget.FILLER_WORDS
    )

    assert feedback.improvement_goal == (
        "Reduce filler-word usage."
    )

    assert feedback.action_plan == [
        "Pause before answering.",
        "Replace filler words with silence.",
    ]


def test_personalized_feedback_strips_whitespace() -> None:
    feedback = PersonalizedCommunicationFeedback(
        primary_focus=(
            CommunicationImprovementTarget.FILLER_WORDS
        ),
        improvement_goal="  Reduce filler words.  ",
        action_plan=[
            "  Pause before answering.  ",
            " ",
            "Replace filler words with silence.",
        ],
    )

    assert feedback.primary_focus == (
        CommunicationImprovementTarget.FILLER_WORDS
    )

    assert feedback.improvement_goal == (
        "Reduce filler words."
    )

    assert feedback.action_plan == [
        "Pause before answering.",
        "Replace filler words with silence.",
    ]


def test_rejects_invalid_primary_focus() -> None:
    with pytest.raises(
        ValueError,
        match="Primary communication focus must be",
    ):
        PersonalizedCommunicationFeedback(
            primary_focus="filler_words",
            improvement_goal="Reduce filler words.",
            action_plan=[
                "Pause before answering.",
            ],
        )


def test_rejects_empty_improvement_goal() -> None:
    with pytest.raises(
        ValueError,
        match="Communication improvement goal cannot be empty",
    ):
        PersonalizedCommunicationFeedback(
            primary_focus=(
                CommunicationImprovementTarget.FILLER_WORDS
            ),
            improvement_goal="   ",
            action_plan=[
                "Pause before answering.",
            ],
        )


def test_rejects_empty_action_plan() -> None:
    with pytest.raises(
        ValueError,
        match="At least one communication action is required",
    ):
        PersonalizedCommunicationFeedback(
            primary_focus=(
                CommunicationImprovementTarget.FILLER_WORDS
            ),
            improvement_goal="Reduce filler words.",
            action_plan=[],
        )


def test_rejects_action_plan_containing_only_whitespace() -> None:
    with pytest.raises(
        ValueError,
        match="At least one communication action is required",
    ):
        PersonalizedCommunicationFeedback(
            primary_focus=(
                CommunicationImprovementTarget.FILLER_WORDS
            ),
            improvement_goal="Reduce filler words.",
            action_plan=[
                " ",
                "   ",
            ],
        )


def test_all_improvement_targets_are_supported() -> None:
    for target in CommunicationImprovementTarget:
        feedback = PersonalizedCommunicationFeedback(
            primary_focus=target,
            improvement_goal="Improve communication.",
            action_plan=[
                "Practice this communication skill.",
            ],
        )

        assert feedback.primary_focus == target