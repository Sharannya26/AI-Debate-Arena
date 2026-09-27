import pytest

from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis
from debate_arena.debate.cross_round_analysis_coordinator import (
    CrossRoundAnalysisCoordinator,
)
from debate_arena.debate.round_performance import RoundPerformance


class FakeDeterministicAnalyzer:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def analyze(self, round_performances):
        self.calls.append(round_performances)
        return self.result


class FakeSemanticAnalyzer:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def analyze(self, analysis):
        self.calls.append(analysis)
        return self.result


def make_rounds():
    return [
        RoundPerformance(
            round=1,
            argument_quality="Moderate",
            communication_quality="Moderate",
            evidence_usage="Limited",
            reasoning_quality="Moderate",
            responsiveness="Partially responsive",
        ),
        RoundPerformance(
            round=2,
            argument_quality="Strong",
            communication_quality="Strong",
            evidence_usage="Limited",
            reasoning_quality="Strong",
            responsiveness="Highly responsive",
        ),
    ]


def make_deterministic_analysis():
    return CrossRoundAnalysis(
        overall_trajectory="Performance improved across the debate.",
        improvement_patterns=[
            "Argument quality improved across the debate."
        ],
        decline_patterns=[],
        stable_patterns=[
            "Evidence usage remained stable across the debate."
        ],
        recurring_patterns=[],
        cross_dimension_patterns=[],
        key_insights=[],
    )


def make_semantic_analysis():
    return CrossRoundAnalysis(
        overall_trajectory="Later rounds showed stronger performance.",
        improvement_patterns=[
            "Argument quality became stronger."
        ],
        decline_patterns=[],
        stable_patterns=[
            "Evidence usage remained stable."
        ],
        recurring_patterns=[],
        cross_dimension_patterns=[
            "Argument quality improved while evidence usage remained limited."
        ],
        key_insights=[
            "The later round showed stronger argument quality."
        ],
    )


def make_coordinator():
    deterministic_result = make_deterministic_analysis()
    semantic_result = make_semantic_analysis()

    deterministic = FakeDeterministicAnalyzer(
        deterministic_result
    )

    semantic = FakeSemanticAnalyzer(
        semantic_result
    )

    coordinator = CrossRoundAnalysisCoordinator(
        deterministic_analyzer=deterministic,
        semantic_analyzer=semantic,
    )

    return coordinator, deterministic, semantic


def test_coordinator_rejects_none_round_performances():
    coordinator, _, _ = make_coordinator()

    with pytest.raises(ValueError):
        coordinator.analyze(None)


def test_coordinator_rejects_empty_round_performances():
    coordinator, _, _ = make_coordinator()

    with pytest.raises(ValueError):
        coordinator.analyze([])


def test_coordinator_calls_deterministic_analyzer():
    coordinator, deterministic, _ = make_coordinator()

    rounds = make_rounds()

    coordinator.analyze(rounds)

    assert len(deterministic.calls) == 1
    assert deterministic.calls[0] == rounds


def test_coordinator_passes_deterministic_result_to_semantic_analyzer():
    coordinator, _, semantic = make_coordinator()

    coordinator.analyze(make_rounds())

    assert len(semantic.calls) == 1
    assert semantic.calls[0] == make_deterministic_analysis()


def test_coordinator_returns_semantic_analysis():
    coordinator, _, _ = make_coordinator()

    result = coordinator.analyze(make_rounds())

    assert result == make_semantic_analysis()


def test_coordinator_stores_last_analysis():
    coordinator, _, _ = make_coordinator()

    result = coordinator.analyze(make_rounds())

    assert coordinator.last_analysis is result


def test_coordinator_runs_deterministic_before_semantic():
    events = []

    class OrderedDeterministicAnalyzer:
        def analyze(self, round_performances):
            events.append("deterministic")
            return make_deterministic_analysis()

    class OrderedSemanticAnalyzer:
        def analyze(self, analysis):
            events.append("semantic")
            return make_semantic_analysis()

    coordinator = CrossRoundAnalysisCoordinator(
        deterministic_analyzer=OrderedDeterministicAnalyzer(),
        semantic_analyzer=OrderedSemanticAnalyzer(),
    )

    coordinator.analyze(make_rounds())

    assert events == [
        "deterministic",
        "semantic",
    ]


def test_coordinator_propagates_deterministic_analyzer_errors():
    class FailingDeterministicAnalyzer:
        def analyze(self, round_performances):
            raise RuntimeError("Deterministic analysis failed.")

    coordinator = CrossRoundAnalysisCoordinator(
        deterministic_analyzer=FailingDeterministicAnalyzer(),
        semantic_analyzer=FakeSemanticAnalyzer(
            make_semantic_analysis()
        ),
    )

    with pytest.raises(RuntimeError, match="Deterministic analysis failed."):
        coordinator.analyze(make_rounds())


def test_coordinator_propagates_semantic_analyzer_errors():
    class FailingSemanticAnalyzer:
        def analyze(self, analysis):
            raise RuntimeError("Semantic analysis failed.")

    coordinator = CrossRoundAnalysisCoordinator(
        deterministic_analyzer=FakeDeterministicAnalyzer(
            make_deterministic_analysis()
        ),
        semantic_analyzer=FailingSemanticAnalyzer(),
    )

    with pytest.raises(RuntimeError, match="Semantic analysis failed."):
        coordinator.analyze(make_rounds())