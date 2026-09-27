from debate_arena.debate.argument import Argument
from debate_arena.debate.argument_analyzer import (
    ArgumentAnalysis,
)
from debate_arena.debate.debate_analyzer import (
    DebateAnalysis,
)
from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState


class FakeArgumentAnalyzer:
    """Fake analyzer for DebateEngine integration tests."""

    def analyze(self, argument: str) -> ArgumentAnalysis:
        return ArgumentAnalysis(
            claim=argument,
            reasoning="Test reasoning.",
        )


class FakeDebateAnalyzer:
    """Fake full-debate analyzer."""

    def __init__(self):
        self.received_state = None

    def analyze(
        self,
        state: DebateState,
    ) -> DebateAnalysis:
        self.received_state = state

        return DebateAnalysis(
            summary="The user maintained a clear position.",
            strongest_argument=(
                "Students can learn responsible usage."
            ),
            weakest_argument=(
                "Social media has educational benefits."
            ),
            strengths=[
                "Clear position",
                "Consistent reasoning",
            ],
            weaknesses=[
                "Limited evidence",
            ],
            evidence_usage=(
                "The user used limited concrete evidence."
            ),
            consistency=(
                "The user's position remained consistent."
            ),
            responsiveness=(
                "The user responded to opposing arguments."
            ),
            recommendations=[
                "Use more concrete evidence."
            ],
        )


def create_finished_state() -> DebateState:
    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    for round_number in range(1, 4):
        state.add_user_argument(
            Argument(
                speaker="user",
                text=(
                    f"User argument for round "
                    f"{round_number}."
                ),
                round=round_number,
                turn=round_number,
            )
        )

        state.add_ai_argument(
            Argument(
                speaker="ai",
                text=(
                    f"AI argument for round "
                    f"{round_number}."
                ),
                round=round_number,
                turn=round_number,
            )
        )

    return state


def test_engine_generates_final_debate_report():
    state = create_finished_state()

    debate_analyzer = FakeDebateAnalyzer()

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=debate_analyzer,
    )

    report = engine.generate_debate_report()

    assert report.topic == (
        "Should social media be banned for students?"
    )

    assert report.user_position == "Against"
    assert report.ai_position == "For"

    assert report.rounds_completed == 3

    assert report.summary == (
        "The user maintained a clear position."
    )

    assert report.strongest_argument == (
        "Students can learn responsible usage."
    )

    assert report.weakest_argument == (
        "Social media has educational benefits."
    )

    assert report.strengths == [
        "Clear position",
        "Consistent reasoning",
    ]

    assert report.weaknesses == [
        "Limited evidence",
    ]

    assert report.recommendations == [
        "Use more concrete evidence."
    ]


def test_engine_stores_last_debate_analysis_and_report():
    state = create_finished_state()

    debate_analyzer = FakeDebateAnalyzer()

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=debate_analyzer,
    )

    report = engine.generate_debate_report()

    assert engine.get_last_debate_analysis() is not None

    assert (
        engine.get_last_debate_analysis().summary
        == "The user maintained a clear position."
    )

    assert engine.get_last_debate_report() is report


def test_engine_passes_current_state_to_debate_analyzer():
    state = create_finished_state()

    debate_analyzer = FakeDebateAnalyzer()

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=debate_analyzer,
    )

    engine.generate_debate_report()

    assert debate_analyzer.received_state is state


def test_engine_rejects_report_before_debate_finishes():
    state = DebateState(
        topic="Test topic",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=FakeDebateAnalyzer(),
    )

    try:
        engine.generate_debate_report()
    except RuntimeError as exc:
        assert (
            "Cannot generate a debate report before "
            "the debate has finished."
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected RuntimeError before debate completion."
        )