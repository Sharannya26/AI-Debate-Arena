from dataclasses import dataclass


@dataclass
class SpeechSample:
    """
    Represents one finalized piece of the user's spoken response.

    A SpeechSample is the foundation for M8 communication analysis.
    It stores the raw transcript together with the debate context
    needed to analyze the speaker's communication later.
    """

    text: str
    duration: float
    round: int
    turn: int

    def __post_init__(self) -> None:
        if not self.text or not self.text.strip():
            raise ValueError("Speech text cannot be empty.")

        if self.duration < 0:
            raise ValueError("Speech duration cannot be negative.")

        if self.round < 1:
            raise ValueError("Round must be at least 1.")

        if self.turn < 1:
            raise ValueError("Turn must be at least 1.")

        self.text = self.text.strip()