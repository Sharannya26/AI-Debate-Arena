from debate_arena.debate.advanced_analysis_coordinator import (
    AdvancedAnalysisCoordinator,
)
from debate_arena.debate.advanced_debate_analysis import (
    AdvancedDebateAnalysis,
)
from debate_arena.debate.debate_performance import DebatePerformance
from debate_arena.debate.performance_summary import PerformanceSummary


class FakeAnalyzer:
    def __init__(self):
        self.received_performance = None
        self.received_summary = None

    def analyze(self, performance, summary):
        self.received_performance = performance
        self.received_summary = summary

        return AdvancedDebateAnalysis(
            overall_interpretation=(
                "The user's performance showed clear development."
            ),
            cross_dimension_patterns=[
                "Reasoning and responsiveness worked together."
            ],
            round_patterns=[
                "Reasoning improved across rounds."
            ],
            strengths_interpretation=(
                "The user developed clear logical responses."
            ),
            weaknesses_interpretation=(
                "Some claims lacked supporting evidence."
            ),
            coaching_interpretation=(
                "Support major claims with concrete evidence."
            ),
            key_insights=[
                "Reasoning was a recurring strength."
            ],
        )


def create_performance():
    return DebatePerformance(
        argument_quality="Argument quality was clear.",
        communication_quality="Communication remained clear.",
        responsiveness="Responsiveness was strong.",
        consistency="Mostly consistent.",
        evidence_usage="Evidence usage was limited.",
        reasoning_quality="Reasoning was clear.",
    )


def create_summary():
    return PerformanceSummary(
        overall_summary="Performance was generally clear."
    )


def test_coordinator_returns_analysis():
    analyzer = FakeAnalyzer()
    coordinator = AdvancedAnalysisCoordinator(
        analyzer=analyzer
    )

    analysis = coordinator.analyze(
        create_performance(),
        create_summary(),
    )

    assert isinstance(
        analysis,
        AdvancedDebateAnalysis,
    )

    assert (
        analysis.overall_interpretation
        == "The user's performance showed clear development."
    )


def test_coordinator_passes_performance_to_analyzer():
    analyzer = FakeAnalyzer()
    coordinator = AdvancedAnalysisCoordinator(
        analyzer=analyzer
    )

    performance = create_performance()
    summary = create_summary()

    coordinator.analyze(
        performance,
        summary,
    )

    assert analyzer.received_performance is performance


def test_coordinator_passes_summary_to_analyzer():
    analyzer = FakeAnalyzer()
    coordinator = AdvancedAnalysisCoordinator(
        analyzer=analyzer
    )

    performance = create_performance()
    summary = create_summary()

    coordinator.analyze(
        performance,
        summary,
    )

    assert analyzer.received_summary is summary


def test_coordinator_stores_last_analysis():
    analyzer = FakeAnalyzer()
    coordinator = AdvancedAnalysisCoordinator(
        analyzer=analyzer
    )

    analysis = coordinator.analyze(
        create_performance(),
        create_summary(),
    )

    assert coordinator.last_analysis is analysis


def test_coordinator_rejects_none_performance():
    analyzer = FakeAnalyzer()
    coordinator = AdvancedAnalysisCoordinator(
        analyzer=analyzer
    )

    try:
        coordinator.analyze(
            None,
            create_summary(),
        )
    except ValueError as exc:
        assert str(exc) == "Debate performance cannot be None."
    else:
        raise AssertionError("Expected ValueError.")


def test_coordinator_rejects_none_summary():
    analyzer = FakeAnalyzer()
    coordinator = AdvancedAnalysisCoordinator(
        analyzer=analyzer
    )

    try:
        coordinator.analyze(
            create_performance(),
            None,
        )
    except ValueError as exc:
        assert str(exc) == "Performance summary cannot be None."
    else:
        raise AssertionError("Expected ValueError.")