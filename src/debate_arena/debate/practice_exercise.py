from dataclasses import dataclass


@dataclass
class PracticeExercise:
    """
    Represents one structured practice exercise
    designed to improve a specific debate skill.

    This model stores coaching exercise information.
    It does not perform analysis and does not call Gemini.
    """

    exercise: str
    objective: str
    instructions: str
    related_priority: str

    def __post_init__(self) -> None:
        self.exercise = self.exercise.strip()
        self.objective = self.objective.strip()
        self.instructions = self.instructions.strip()
        self.related_priority = (
            self.related_priority.strip()
        )

        if not self.exercise:
            raise ValueError(
                "Practice exercise cannot be empty."
            )

        if not self.objective:
            raise ValueError(
                "Practice exercise objective cannot be empty."
            )

        if not self.instructions:
            raise ValueError(
                "Practice exercise instructions cannot be empty."
            )

        if not self.related_priority:
            raise ValueError(
                "Related priority cannot be empty."
            )