from collections.abc import Callable

from debate_arena.debate.engine import DebateEngine


class DebateListener:
    """Connects AssemblyAI transcripts to the DebateEngine."""

    def __init__(
        self,
        engine: DebateEngine,
        on_transcript: Callable[[str], None] | None = None,
    ):
        self.engine = engine
        self.on_transcript = on_transcript

    def handle_transcript(self, transcript: str) -> None:
        """Send a completed user transcript to the debate engine."""

        transcript = transcript.strip()

        if not transcript:
            return

        if self.on_transcript:
            self.on_transcript(transcript)

        self.engine.submit_user_argument(transcript)