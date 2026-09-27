from debate_arena.debate.argument import Argument
from debate_arena.debate.state import DebateState


class DebateHistoryExtractor:
    """Converts debate state history into report-ready data."""

    def extract(self, state: DebateState) -> list[dict]:
        """Extract the complete debate history."""

        if state is None:
            raise ValueError("Debate state cannot be None.")

        history = []

        for argument in state.get_history():
            history.append(
                {
                    "speaker": argument.speaker,
                    "text": argument.text,
                    "round": argument.round,
                    "turn": argument.turn,
                }
            )

        return history