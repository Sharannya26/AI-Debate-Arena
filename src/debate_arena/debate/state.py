from dataclasses import dataclass, field

from debate_arena.debate.argument import Argument


@dataclass
class DebateState:
    """Stores the current state of an AI Debate Arena session."""

    topic: str
    user_position: str
    ai_position: str

    current_round: int = 1
    current_turn: str = "user"
    max_rounds: int = 3

    user_arguments: list[Argument] = field(default_factory=list)
    ai_arguments: list[Argument] = field(default_factory=list)
    history: list[Argument] = field(default_factory=list)

    def add_user_argument(self, argument: Argument) -> None:
        """Store a user argument."""

        self.user_arguments.append(argument)
        self.history.append(argument)

    def add_ai_argument(self, argument: Argument) -> None:
        """Store an AI argument."""

        self.ai_arguments.append(argument)
        self.history.append(argument)

    def advance_round(self) -> None:
        """Move the debate to the next round."""

        self.current_round += 1

    def switch_turn(self) -> None:
        """Switch between the user's and AI's turn."""

        if self.current_turn == "user":
            self.current_turn = "ai"
        else:
            self.current_turn = "user"

    def is_finished(self) -> bool:
        """
        Return True only when all configured rounds
        have been completed by BOTH sides.
        """

        completed_rounds = min(
            len(self.user_arguments),
            len(self.ai_arguments),
        )

        return (
            self.current_round > self.max_rounds
            or completed_rounds >= self.max_rounds
        )

    def get_history(self) -> list[Argument]:
        """Return a copy of the debate history."""

        return list(self.history)

    def get_context(self) -> str:
        """Build the complete debate context for the LLM."""

        lines = [
            f"Topic: {self.topic}",
            f"User position: {self.user_position}",
            f"AI position: {self.ai_position}",
            "",
            "Debate history:",
        ]

        for argument in self.history:
            speaker = (
                "User"
                if argument.speaker == "user"
                else "AI"
            )

            lines.append(
                f"Round {argument.round} - "
                f"{speaker}: {argument.text}"
            )

        return "\n".join(lines)