import pytest

from debate_arena.debate.communication_feedback import CommunicationFeedback


def create_feedback() -> CommunicationFeedback:
    return CommunicationFeedback(
        clarity="The speaker communicates ideas clearly.",
        conciseness="Most ideas are expressed efficiently.",
        delivery="The delivery is energetic and understandable.",
        strengths=[
            "Clear main ideas",
            "Good engagement",
        ],
        weaknesses=[
            "Occasional filler words",
        ],
        recommendations=[
            "Reduce filler words",
            "Use deliberate pauses",
        ],
    )


def test_communication_feedback_stores_data():
    feedback = create_feedback()

    assert feedback.clarity == "The speaker communicates ideas clearly."
    assert feedback.conciseness == "Most ideas are expressed efficiently."
    assert feedback.delivery == "The delivery is energetic and understandable."


def test_communication_feedback_stores_lists():
    feedback = create_feedback()

    assert feedback.strengths == [
        "Clear main ideas",
        "Good engagement",
    ]

    assert feedback.weaknesses == [
        "Occasional filler words",
    ]

    assert feedback.recommendations == [
        "Reduce filler words",
        "Use deliberate pauses",
    ]


def test_communication_feedback_strips_list_items():
    feedback = CommunicationFeedback(
        clarity="Clear communication.",
        conciseness="Concise.",
        delivery="Good delivery.",
        strengths=[
            "  Clear ideas  ",
            "  Good structure ",
        ],
        weaknesses=[
            "  Too many fillers ",
        ],
        recommendations=[
            "  Slow down slightly ",
        ],
    )

    assert feedback.strengths == [
        "Clear ideas",
        "Good structure",
    ]

    assert feedback.weaknesses == [
        "Too many fillers",
    ]

    assert feedback.recommendations == [
        "Slow down slightly",
    ]


def test_communication_feedback_rejects_empty_clarity():
    with pytest.raises(
        ValueError,
        match="Clarity feedback cannot be empty",
    ):
        CommunicationFeedback(
            clarity="   ",
            conciseness="Concise.",
            delivery="Good delivery.",
            strengths=["Clear ideas"],
            weaknesses=["Fillers"],
            recommendations=["Pause more"],
        )


def test_communication_feedback_rejects_empty_conciseness():
    with pytest.raises(
        ValueError,
        match="Conciseness feedback cannot be empty",
    ):
        CommunicationFeedback(
            clarity="Clear.",
            conciseness="   ",
            delivery="Good delivery.",
            strengths=["Clear ideas"],
            weaknesses=["Fillers"],
            recommendations=["Pause more"],
        )


def test_communication_feedback_rejects_empty_delivery():
    with pytest.raises(
        ValueError,
        match="Delivery feedback cannot be empty",
    ):
        CommunicationFeedback(
            clarity="Clear.",
            conciseness="Concise.",
            delivery="   ",
            strengths=["Clear ideas"],
            weaknesses=["Fillers"],
            recommendations=["Pause more"],
        )


def test_communication_feedback_rejects_empty_strengths():
    with pytest.raises(
        ValueError,
        match="At least one communication strength is required",
    ):
        CommunicationFeedback(
            clarity="Clear.",
            conciseness="Concise.",
            delivery="Good.",
            strengths=[],
            weaknesses=["Fillers"],
            recommendations=["Pause more"],
        )


def test_communication_feedback_rejects_empty_weaknesses():
    with pytest.raises(
        ValueError,
        match="At least one communication weakness is required",
    ):
        CommunicationFeedback(
            clarity="Clear.",
            conciseness="Concise.",
            delivery="Good.",
            strengths=["Clear ideas"],
            weaknesses=[],
            recommendations=["Pause more"],
        )


def test_communication_feedback_rejects_empty_recommendations():
    with pytest.raises(
        ValueError,
        match="At least one communication recommendation is required",
    ):
        CommunicationFeedback(
            clarity="Clear.",
            conciseness="Concise.",
            delivery="Good.",
            strengths=["Clear ideas"],
            weaknesses=["Fillers"],
            recommendations=[],
        )