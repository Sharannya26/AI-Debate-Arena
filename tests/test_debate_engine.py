import pytest
from unittest.mock import Mock

from debate_arena.debate.argument import Argument
from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState
from debate_arena.debate.argument_analyzer import ArgumentAnalysis
from debate_arena.debate.strategy import DebateStrategy
from debate_arena.debate.semantic_performance_analysis import (
    SemanticPerformanceAnalysis,
)


class FakeLLM:
    """Test double that avoids real Gemini API calls."""

    def analyze_debate(self, debate_data):
        return {
            "summary": "Test debate summary.",
            "strongest_argument": (
                "Social media provides educational opportunities."
            ),
            "weakest_argument": (
                "The AI response did not address the educational point."
            ),
            "strengths": [
                "Clear argument structure."
            ],
            "weaknesses": [
                "More evidence could be provided."
            ],
            "evidence_usage": (
                "Some evidence was used."
            ),
            "consistency": (
                "The position remained consistent."
            ),
            "responsiveness": (
                "The response addressed the previous argument."
            ),
            "recommendations": [
                "Provide stronger supporting evidence."
            ],
        }


class FakeArgumentAnalyzer:
    """Test double that avoids real Gemini API calls."""

    def analyze(
        self,
        argument: str,
    ) -> ArgumentAnalysis:
        return ArgumentAnalysis(
            claim=argument,
            reasoning="Test reasoning.",
            assumptions=[],
            evidence=[],
            weaknesses=[],
            argument_type="general",
        )


class FakePerformancePipeline:
    """Test double for the M9.8.8 performance pipeline."""

    def __init__(self):
        self.analyze_calls = []
        self.last_moment_analysis = None

        self.semantic_performance = SemanticPerformanceAnalysis(
            overall_interpretation="Overall performance was strong.",
            strengths_interpretation="Clear arguments.",
            weaknesses_interpretation=(
                "Some arguments needed more evidence."
            ),
            coaching_interpretation=(
                "Use stronger supporting evidence."
            ),
            key_insights=[
                "Arguments became clearer across rounds."
            ],
        )

        # M9.9.6 — Fake coaching session report.
        # This allows DebateEngine tests to verify that
        # the integrated coaching report is passed through.
        self.last_coaching_session_report = Mock(
            name="coaching_session_report"
        )

    def analyze(self, round_performances):
        self.analyze_calls.append(round_performances)
        return self.semantic_performance


def create_test_engine() -> DebateEngine:
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    return DebateEngine(
        state,
        llm=FakeLLM(),
        argument_analyzer=FakeArgumentAnalyzer(),
    )


def test_user_argument_changes_turn_to_ai():
    engine = create_test_engine()

    engine.submit_user_argument(
        "Social media provides educational opportunities."
    )

    assert len(engine.state.user_arguments) == 1

    argument = engine.state.user_arguments[0]

    assert isinstance(argument, Argument)
    assert argument.speaker == "user"
    assert argument.text == (
        "Social media provides educational opportunities."
    )
    assert argument.round == 1
    assert argument.turn == 1
    assert engine.is_ai_turn()
    assert not engine.is_user_turn()


def test_ai_argument_changes_turn_to_user():
    engine = create_test_engine()

    engine.submit_user_argument(
        "Social media provides educational opportunities."
    )

    engine.submit_ai_argument(
        "Those benefits do not eliminate its risks."
    )

    assert len(engine.state.ai_arguments) == 1

    argument = engine.state.ai_arguments[0]

    assert isinstance(argument, Argument)
    assert argument.speaker == "ai"
    assert argument.text == (
        "Those benefits do not eliminate its risks."
    )
    assert argument.round == 1
    assert argument.turn == 1
    assert engine.is_user_turn()
    assert not engine.is_ai_turn()


def test_empty_argument_is_rejected():
    engine = create_test_engine()

    with pytest.raises(ValueError):
        engine.submit_user_argument("   ")

    engine.submit_user_argument(
        "Valid user argument."
    )

    with pytest.raises(ValueError):
        engine.submit_ai_argument("")


def test_new_round_starts_with_user():
    engine = create_test_engine()

    engine.submit_user_argument(
        "First argument."
    )

    engine.submit_ai_argument(
        "First response."
    )

    engine.start_new_round()

    assert engine.state.current_round == 2
    assert engine.is_user_turn()


def test_arguments_are_rejected_after_debate_finishes():
    engine = create_test_engine()

    engine.state.current_round = (
        engine.state.max_rounds + 1
    )

    with pytest.raises(
        RuntimeError,
        match="Debate has finished",
    ):
        engine.submit_user_argument(
            "This argument should be rejected."
        )

    with pytest.raises(
        RuntimeError,
        match="Debate has finished",
    ):
        engine.submit_ai_argument(
            "This response should be rejected."
        )


def test_user_cannot_submit_during_ai_turn():
    engine = create_test_engine()

    engine.submit_user_argument(
        "First user argument."
    )

    assert engine.is_ai_turn()

    with pytest.raises(
        RuntimeError,
        match="It is not the user's turn",
    ):
        engine.submit_user_argument(
            "Second user argument."
        )


def test_ai_cannot_submit_during_user_turn():
    engine = create_test_engine()

    assert engine.is_user_turn()

    with pytest.raises(
        RuntimeError,
        match="It is not the AI's turn",
    ):
        engine.submit_ai_argument(
            "AI should not be able to speak yet."
        )


def test_cannot_start_new_round_before_ai_responds():
    engine = create_test_engine()

    engine.submit_user_argument(
        "Social media provides educational opportunities."
    )

    with pytest.raises(
        RuntimeError,
        match="Cannot start a new round before the AI has responded",
    ):
        engine.start_new_round()


def test_can_start_new_round_after_ai_responds():
    engine = create_test_engine()

    engine.submit_user_argument(
        "Social media provides educational opportunities."
    )

    engine.submit_ai_argument(
        "Those benefits do not eliminate its risks."
    )

    engine.start_new_round()

    assert engine.state.current_round == 2
    assert engine.state.current_turn == "user"


def test_cannot_start_new_round_after_debate_finishes():
    engine = create_test_engine()

    engine.state.current_round = (
        engine.state.max_rounds + 1
    )

    with pytest.raises(
        RuntimeError,
        match="Debate has finished",
    ):
        engine.start_new_round()


def test_submit_user_argument_analyzes_argument():
    analyzer = Mock()

    analyzer.analyze.return_value = ArgumentAnalysis(
        claim="Social media should not be banned.",
        reasoning="Students can use it for education.",
        assumptions=[
            "Students can use social media responsibly."
        ],
        evidence=[],
        weaknesses=[
            "The argument does not address misuse."
        ],
        argument_type="prescriptive",
    )

    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Social media should not be banned.",
        ai_position="Social media should be banned.",
    )

    engine = DebateEngine(
        state=state,
        llm=FakeLLM(),
        argument_analyzer=analyzer,
    )

    argument = (
        "Social media should not be banned because "
        "students can use it for education."
    )

    engine.submit_user_argument(argument)

    analyzer.analyze.assert_called_once_with(argument)

    assert engine.last_argument_analysis is not None

    assert (
        engine.last_argument_analysis.claim
        == "Social media should not be banned."
    )


def test_submit_user_argument_stores_analysis_for_latest_argument():
    analyzer = Mock()

    analyzer.analyze.side_effect = [
        ArgumentAnalysis(
            claim="First claim",
            argument_type="general",
        ),
        ArgumentAnalysis(
            claim="Second claim",
            argument_type="causal",
        ),
    ]

    state = DebateState(
        topic="Test topic",
        user_position="Position A",
        ai_position="Position B",
        max_rounds=3,
    )

    engine = DebateEngine(
        state=state,
        llm=FakeLLM(),
        argument_analyzer=analyzer,
    )

    engine.submit_user_argument(
        "First argument"
    )

    engine.submit_ai_argument(
        "First AI rebuttal"
    )

    engine.submit_user_argument(
        "Second argument"
    )

    assert (
        engine.last_argument_analysis.claim
        == "Second claim"
    )

    assert (
        engine.last_argument_analysis.argument_type
        == "causal"
    )


def test_generate_ai_rebuttal_uses_full_debate_context():
    llm = Mock()

    llm.generate_debate_response.return_value = Mock(
        rebuttal="The AI's context-aware rebuttal.",
        strategy=DebateStrategy.DIRECT_COUNTER,
    )

    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    engine = DebateEngine(
        state=state,
        llm=llm,
    )

    # Round 1
    engine.submit_user_argument(
        "Social media provides educational opportunities."
    )

    engine.submit_ai_argument(
        "Those benefits do not eliminate its risks."
    )

    # Start Round 2
    engine.start_new_round()

    # Round 2 user argument
    engine.submit_user_argument(
        "Students can learn responsible social media usage."
    )

    # Generate the AI rebuttal.
    engine.generate_ai_rebuttal()

    # The prompt sent to the LLM must contain
    # the complete debate context.
    prompt = llm.generate_debate_response.call_args[0][0]

    assert (
        "Social media provides educational opportunities."
        in prompt
    )

    assert (
        "Those benefits do not eliminate its risks."
        in prompt
    )

    assert (
        "Students can learn responsible social media usage."
        in prompt
    )

    assert "Round 1" in prompt
    assert "Round 2" in prompt


def test_generate_debate_report_includes_semantic_performance():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    pipeline = FakePerformancePipeline()

    engine = DebateEngine(
        state=state,
        llm=FakeLLM(),
        argument_analyzer=FakeArgumentAnalyzer(),
        performance_pipeline=pipeline,
    )

    engine.submit_user_argument(
        "Social media provides educational opportunities."
    )

    engine.submit_ai_argument(
        "Those benefits do not eliminate its risks."
    )

    engine.state.current_round = (
        engine.state.max_rounds + 1
    )

    engine.round_performances = [
        Mock(round=1),
    ]

    report = engine.generate_debate_report()

    assert report.semantic_performance is (
        pipeline.semantic_performance
    )

    assert len(pipeline.analyze_calls) == 1

    assert pipeline.analyze_calls[0] == (
        engine.round_performances
    )


def test_generate_debate_report_includes_semantic_moments():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    pipeline = FakePerformancePipeline()

    pipeline.last_moment_analysis = Mock(
        strongest_moments=[
            "Strong opening argument"
        ],
        weakest_moments=[
            "Weak evidence"
        ],
    )

    engine = DebateEngine(
        state=state,
        llm=FakeLLM(),
        argument_analyzer=FakeArgumentAnalyzer(),
        performance_pipeline=pipeline,
    )

    engine.submit_user_argument(
        "Social media provides educational opportunities."
    )

    engine.submit_ai_argument(
        "Those benefits do not eliminate its risks."
    )

    engine.state.current_round = (
        engine.state.max_rounds + 1
    )

    engine.round_performances = [
        Mock(round=1),
    ]

    report = engine.generate_debate_report()

    assert report.semantic_moments is (
        pipeline.last_moment_analysis
    )


def test_generate_debate_report_caches_integrated_report():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    pipeline = FakePerformancePipeline()

    engine = DebateEngine(
        state=state,
        llm=FakeLLM(),
        argument_analyzer=FakeArgumentAnalyzer(),
        performance_pipeline=pipeline,
    )

    engine.submit_user_argument(
        "Social media provides educational opportunities."
    )

    engine.submit_ai_argument(
        "Those benefits do not eliminate its risks."
    )

    engine.state.current_round = (
        engine.state.max_rounds + 1
    )

    engine.round_performances = [
        Mock(round=1),
    ]

    first_report = engine.generate_debate_report()
    second_report = engine.generate_debate_report()

    assert first_report is second_report
    assert len(pipeline.analyze_calls) == 1


def test_generate_debate_report_includes_coaching_session_report():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    pipeline = FakePerformancePipeline()

    engine = DebateEngine(
        state=state,
        llm=FakeLLM(),
        argument_analyzer=FakeArgumentAnalyzer(),
        performance_pipeline=pipeline,
    )

    engine.submit_user_argument(
        "Social media provides educational opportunities."
    )

    engine.submit_ai_argument(
        "Those benefits do not eliminate its risks."
    )

    engine.state.current_round = (
        engine.state.max_rounds + 1
    )

    engine.round_performances = [
        Mock(round=1),
    ]

    report = engine.generate_debate_report()

    assert report.coaching_session_report is (
        pipeline.last_coaching_session_report
    )

    assert (
        engine.last_coaching_session_report
        is report.coaching_session_report
    )


def test_generate_debate_report_caches_coaching_session_report():
    state = DebateState(
        topic="Should social media be banned for teenagers?",
        user_position="Against",
        ai_position="For",
    )

    pipeline = FakePerformancePipeline()

    engine = DebateEngine(
        state=state,
        llm=FakeLLM(),
        argument_analyzer=FakeArgumentAnalyzer(),
        performance_pipeline=pipeline,
    )

    engine.submit_user_argument(
        "Social media provides educational opportunities."
    )

    engine.submit_ai_argument(
        "Those benefits do not eliminate its risks."
    )

    engine.state.current_round = (
        engine.state.max_rounds + 1
    )

    engine.round_performances = [
        Mock(round=1),
    ]

    first_report = engine.generate_debate_report()

    first_coaching_report = (
        first_report.coaching_session_report
    )

    second_report = engine.generate_debate_report()

    second_coaching_report = (
        second_report.coaching_session_report
    )

    assert first_coaching_report is not None
    assert second_coaching_report is not None

    assert (
        first_coaching_report
        is second_coaching_report
    )

    assert (
        engine.last_coaching_session_report
        is second_coaching_report
    )