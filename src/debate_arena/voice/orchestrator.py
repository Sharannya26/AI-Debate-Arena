from debate_arena.debate.debate_report import DebateReport
from debate_arena.debate.engine import DebateEngine


class DebateOrchestrator:
    """Coordinates transcript handling, debate processing, and reporting."""

    def __init__(self, engine: DebateEngine):
        self.engine = engine

    def handle_final_transcript(
        self,
        transcript: str,
    ) -> None:
        """Process a finalized user transcript through the debate engine."""

        if not transcript or not transcript.strip():
            return

        transcript = transcript.strip()

        print("\n" + "-" * 60)
        print("👤 USER ARGUMENT")
        print("-" * 60)
        print(transcript)

        self.engine.submit_user_argument(transcript)

        rebuttal = self.engine.generate_and_submit_ai_rebuttal()

        print("\n" + "-" * 60)
        print("🤖 AI REBUTTAL")
        print("-" * 60)
        print(rebuttal)

        if self.engine.tts is not None:
            self.engine.tts.speak_stream(rebuttal)

        if not self.engine.state.is_finished():
            self.engine.complete_round()

    def get_debate_report(self) -> DebateReport:
        """
        Return the final debate report.

        The debate must be finished before a report can be generated.
        """

        if not self.engine.is_finished():
            raise RuntimeError(
                "Cannot get the debate report before "
                "the debate has finished."
            )

        return self.engine.generate_debate_report()