import pytest

from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)
from debate_arena.debate.practice_exercise import (
    PracticeExercise,
)
from debate_arena.debate.practice_exercise_analyzer import (
    PracticeExerciseAnalyzer,
)


def make_priority(
    focus_area: str,
    priority: str = "Improve the target skill",
) -> PersonalizedImprovementPriority:
    return PersonalizedImprovementPriority(
        priority=priority,
        reason="This area needs improvement.",
        focus_area=focus_area,
        supporting_evidence=[
            "Performance varied across rounds."
        ],
    )


def test_analyzer_creates_evidence_usage_exercise():
    analyzer = PracticeExerciseAnalyzer()

    priority = make_priority(
        focus_area="Improve evidence usage",
        priority="Improve evidence usage",
    )

    exercises = analyzer.analyze([priority])

    assert len(exercises) == 1
    assert isinstance(exercises[0], PracticeExercise)
    assert (
        exercises[0].objective
        == "Improve evidence usage."
    )
    assert (
        exercises[0].related_priority
        == "Improve evidence usage"
    )


def test_analyzer_creates_argument_quality_exercise():
    analyzer = PracticeExerciseAnalyzer()

    priority = make_priority(
        focus_area="Improve argument quality",
        priority="Improve argument quality",
    )

    exercises = analyzer.analyze([priority])

    assert len(exercises) == 1
    assert (
        exercises[0].objective
        == "Improve argument quality."
    )


def test_analyzer_creates_communication_quality_exercise():
    analyzer = PracticeExerciseAnalyzer()

    priority = make_priority(
        focus_area="Improve communication quality",
        priority="Improve communication quality",
    )

    exercises = analyzer.analyze([priority])

    assert len(exercises) == 1
    assert (
        exercises[0].objective
        == "Improve communication quality."
    )


def test_analyzer_creates_reasoning_quality_exercise():
    analyzer = PracticeExerciseAnalyzer()

    priority = make_priority(
        focus_area="Improve reasoning quality",
        priority="Improve reasoning quality",
    )

    exercises = analyzer.analyze([priority])

    assert len(exercises) == 1
    assert (
        exercises[0].objective
        == "Improve reasoning quality."
    )


def test_analyzer_creates_responsiveness_exercise():
    analyzer = PracticeExerciseAnalyzer()

    priority = make_priority(
        focus_area="Improve responsiveness",
        priority="Improve responsiveness",
    )

    exercises = analyzer.analyze([priority])

    assert len(exercises) == 1
    assert (
        exercises[0].objective
        == "Improve responsiveness."
    )


def test_analyzer_handles_unknown_focus_area():
    analyzer = PracticeExerciseAnalyzer()

    priority = make_priority(
        focus_area="Improve confidence",
        priority="Improve confidence",
    )

    exercises = analyzer.analyze([priority])

    assert len(exercises) == 1
    assert (
        exercises[0].exercise
        == "Improve confidence"
    )
    assert (
        exercises[0].objective
        == "This area needs improvement."
    )
    assert (
        exercises[0].related_priority
        == "Improve confidence"
    )


def test_analyzer_returns_empty_list_for_no_priorities():
    analyzer = PracticeExerciseAnalyzer()

    exercises = analyzer.analyze([])

    assert exercises == []


def test_analyzer_rejects_none_priorities():
    analyzer = PracticeExerciseAnalyzer()

    with pytest.raises(
        ValueError,
        match="Improvement priorities cannot be None.",
    ):
        analyzer.analyze(None)


def test_analyzer_rejects_none_priority_item():
    analyzer = PracticeExerciseAnalyzer()

    with pytest.raises(
        ValueError,
        match="Improvement priorities cannot contain None.",
    ):
        analyzer.analyze([None])