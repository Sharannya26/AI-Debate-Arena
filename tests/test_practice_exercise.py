import pytest

from debate_arena.debate.practice_exercise import (
    PracticeExercise,
)


def test_practice_exercise_stores_values():
    exercise = PracticeExercise(
        exercise="Build a claim with supporting evidence.",
        objective="Improve evidence usage.",
        instructions=(
            "State one claim and support it with "
            "one concrete example within 30 seconds."
        ),
        related_priority="Improve evidence usage",
    )

    assert (
        exercise.exercise
        == "Build a claim with supporting evidence."
    )

    assert (
        exercise.objective
        == "Improve evidence usage."
    )

    assert (
        exercise.instructions
        == (
            "State one claim and support it with "
            "one concrete example within 30 seconds."
        )
    )

    assert (
        exercise.related_priority
        == "Improve evidence usage"
    )


def test_practice_exercise_strips_whitespace():
    exercise = PracticeExercise(
        exercise="  Practice evidence.  ",
        objective="  Improve evidence usage.  ",
        instructions="  Give one example.  ",
        related_priority="  Improve evidence usage  ",
    )

    assert exercise.exercise == "Practice evidence."
    assert exercise.objective == "Improve evidence usage."
    assert exercise.instructions == "Give one example."
    assert exercise.related_priority == "Improve evidence usage"


@pytest.mark.parametrize(
    "field,value,error_message",
    [
        (
            "exercise",
            "",
            "Practice exercise cannot be empty.",
        ),
        (
            "objective",
            "",
            "Practice exercise objective cannot be empty.",
        ),
        (
            "instructions",
            "",
            "Practice exercise instructions cannot be empty.",
        ),
        (
            "related_priority",
            "",
            "Related priority cannot be empty.",
        ),
    ],
)
def test_practice_exercise_rejects_empty_fields(
    field,
    value,
    error_message,
):
    values = {
        "exercise": "Practice exercise.",
        "objective": "Improve a skill.",
        "instructions": "Follow the instructions.",
        "related_priority": "Improve communication quality",
    }

    values[field] = value

    with pytest.raises(
        ValueError,
        match=error_message,
    ):
        PracticeExercise(**values)


def test_practice_exercise_is_dataclass():
    exercise = PracticeExercise(
        exercise="Practice rebuttal.",
        objective="Improve responsiveness.",
        instructions="Respond directly to the opponent.",
        related_priority="Improve responsiveness",
    )

    assert hasattr(exercise, "__dataclass_fields__")