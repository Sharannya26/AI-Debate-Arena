from dataclasses import dataclass


@dataclass
class Argument:
    """Represents a single argument made during a debate."""

    speaker: str
    text: str
    round: int
    turn: int