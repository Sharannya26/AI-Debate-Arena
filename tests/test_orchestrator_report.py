import pytest

from debate_arena.debate.argument import Argument
from debate_arena.debate.debate_analyzer import DebateAnalysis
from debate_arena.debate.debate_report import DebateReport
from debate_arena.debate.engine import DebateEngine
from debate_arena.voice.orchestrator import DebateOrchestrator
from debate_arena.debate.state import DebateState


class FakeArgumentAnalyzer:
    """Fake argument analyzer for orchestrator tests."""

    def analyze(self, argument: str):
        from debate_arena.debate.argument_analyzer import (
            ArgumentAnalysis,
        )

        return ArgumentAnalysis(
            claim=argument,
            reasoning="Test reasoning.",
        )


class FakeDebateAnalyzer:
    """Fake debate analyzer for orchestrator tests."""

    def analyze(
        self,
        state: DebateState,
    ) -> DebateAnalysis:
        return DebateAnalysis(
            summary="Test summary.",
            strongest_argument="Strongest argument.",
            weakest_argument="Weakest argument.",
            strengths=["Clear reasoning."],
            weaknesses=["Limited evidence."],
            evidence_usage="Some evidence was used.",
            consistency="Position remained consistent.",
            responsiveness="Arguments were addressed.",
            recommendations=[
                "Use more concrete evidence."
            ],
        )


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


def create_orchestrator() -> DebateOrchestrator:
    """Create an orchestrator with fake analysis dependencies."""

    state = create_finished_state()

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=FakeDebateAnalyzer(),
    )

    return DebateOrchestrator(engine)


def test_orchestrator_returns_final_debate_report():
    orchestrator = create_orchestrator()

    report = orchestrator.get_debate_report()

    assert isinstance(report, DebateReport)


def test_orchestrator_exposes_report_content():
    orchestrator = create_orchestrator()

    report = orchestrator.get_debate_report()

    assert report.summary == "Test summary."
    assert report.strongest_argument == (
        "Strongest argument."
    )
    assert report.weakest_argument == (
        "Weakest argument."
    )

    assert report.strengths == [
        "Clear reasoning."
    ]

    assert report.weaknesses == [
        "Limited evidence."
    ]

    assert report.recommendations == [
        "Use more concrete evidence."
    ]


def test_orchestrator_rejects_report_before_debate_finishes():
    state = DebateState(
        topic="Test topic",
        user_position="For",
        ai_position="Against",
        max_rounds=3,
    )

    engine = DebateEngine(
        state=state,
        argument_analyzer=FakeArgumentAnalyzer(),
        debate_analyzer=FakeDebateAnalyzer(),
    )

    orchestrator = DebateOrchestrator(engine)

    with pytest.raises(
        RuntimeError,
        match="Cannot get the debate report before",
    ):
        orchestrator.get_debate_report()


def test_orchestrator_returns_same_cached_report():
    orchestrator = create_orchestrator()

    first_report = orchestrator.get_debate_report()
    second_report = orchestrator.get_debate_report()

    assert first_report is second_report