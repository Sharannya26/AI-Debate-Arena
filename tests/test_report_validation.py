from debate_arena.debate.argument import Argument
from debate_arena.debate.debate_analyzer import DebateAnalysis
from debate_arena.debate.debate_report import DebateReport
from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState


class FakeArgumentAnalyzer:
    """Fake argument analyzer for validation tests."""

    def analyze(self, argument: str):
        from debate_arena.debate.argument_analyzer import (
            ArgumentAnalysis,
        )

        return ArgumentAnalysis(
            claim=argument,
            reasoning="Test reasoning.",
        )


class FakeDebateAnalyzer:
    """Fake full-debate analyzer."""

    def __init__(
        self,
        analysis: DebateAnalysis | None = None,
    ):
        self.analysis = analysis or DebateAnalysis(
            summary="Test debate summary.",
            strongest_argument="Strong argument.",
            weakest_argument="Weak argument.",
            strengths=["Clear reasoning."],
            weaknesses=["Limited evidence."],
            evidence_usage="Limited evidence was used.",
            consistency="The position remained consistent.",
            responsiveness="The opposing arguments were addressed.",
            recommendations=["Use more concrete evidence."],
        )

    def analyze(self, state: DebateState) -> DebateAnalysis:
        return self.analysis


def create_finished_state() -> DebateState:
    """Create a completed three-round debate."""

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
                text=f"User argument {round_number}.",
                round=round_number,
                turn=round_number,
            )
        )

        state.add_ai_argument(
            Argument(
                speaker="ai",
                text=f"AI argument {round_number}.",
                round=round_number,
                turn=round_number,
            )
        )

    return state


def test_report_contains_all_analysis_sections():
    state = create_finished_state()

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=FakeDebateAnalyzer(),
    )

    report = engine.generate_debate_report()

    assert isinstance(report, DebateReport)

    assert report.summary
    assert report.strongest_argument
    assert report.weakest_argument

    assert isinstance(report.strengths, list)
    assert isinstance(report.weaknesses, list)
    assert isinstance(report.recommendations, list)

    assert report.evidence_usage
    assert report.consistency
    assert report.responsiveness


def test_report_metadata_matches_debate_state():
    state = create_finished_state()

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=FakeDebateAnalyzer(),
    )

    report = engine.generate_debate_report()

    assert report.topic == state.topic
    assert report.user_position == state.user_position
    assert report.ai_position == state.ai_position

    assert report.rounds_completed == 3


def test_report_lists_are_independent_from_analysis():
    analysis = DebateAnalysis(
        summary="Summary.",
        strengths=["Original strength."],
        weaknesses=["Original weakness."],
        recommendations=["Original recommendation."],
    )

    state = create_finished_state()

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=FakeDebateAnalyzer(
            analysis=analysis,
        ),
    )

    report = engine.generate_debate_report()

    report.strengths.append(
        "New report-only strength."
    )

    report.weaknesses.append(
        "New report-only weakness."
    )

    report.recommendations.append(
        "New report-only recommendation."
    )

    assert analysis.strengths == [
        "Original strength."
    ]

    assert analysis.weaknesses == [
        "Original weakness."
    ]

    assert analysis.recommendations == [
        "Original recommendation."
    ]


def test_report_is_stored_as_last_report():
    state = create_finished_state()

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=FakeDebateAnalyzer(),
    )

    report = engine.generate_debate_report()

    assert engine.get_last_debate_report() is report


def test_report_generation_does_not_modify_debate_history():
    state = create_finished_state()

    history_before = list(state.history)

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=FakeDebateAnalyzer(),
    )

    engine.generate_debate_report()

    assert state.history == history_before
    assert len(state.history) == 6


def test_report_generation_does_not_modify_round_count():
    state = create_finished_state()

    round_before = state.current_round

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=FakeDebateAnalyzer(),
    )

    engine.generate_debate_report()

    assert state.current_round == round_before