from debate_arena.debate.moment_analysis import MomentAnalysis
from debate_arena.debate.moment_analysis_coordinator import (
    MomentAnalysisCoordinator,
)
from debate_arena.debate.semantic_moment_analysis import (
    SemanticMomentAnalysis,
)


class FakeSemanticMomentAnalyzer:
    def __init__(self):
        self.calls = []

        self.result = SemanticMomentAnalysis(
            strongest_interpretation=(
                "The strongest moments showed clear "
                "argument structure."
            ),
            weakest_interpretation=(
                "The weakest moments showed limited "
                "evidence support."
            ),
            key_insights=[
                "Argument structure became clearer later."
            ],
        )

    def analyze(self, analysis):
        self.calls.append(analysis)
        return self.result


def create_moment_analysis():
    return MomentAnalysis(
        strongest_moments=[
            "Round 2: Strong argument quality — Strong argument."
        ],
        weakest_moments=[
            "Round 1: Weak evidence usage — Limited evidence."
        ],
    )


def test_coordinator_returns_semantic_analysis():
    fake_analyzer = FakeSemanticMomentAnalyzer()

    coordinator = MomentAnalysisCoordinator(
        semantic_analyzer=fake_analyzer
    )

    result = coordinator.analyze(
        create_moment_analysis()
    )

    assert isinstance(
        result,
        SemanticMomentAnalysis,
    )


def test_coordinator_calls_semantic_analyzer():
    fake_analyzer = FakeSemanticMomentAnalyzer()

    coordinator = MomentAnalysisCoordinator(
        semantic_analyzer=fake_analyzer
    )

    analysis = create_moment_analysis()

    coordinator.analyze(analysis)

    assert len(fake_analyzer.calls) == 1
    assert fake_analyzer.calls[0] is analysis


def test_coordinator_stores_last_analysis():
    fake_analyzer = FakeSemanticMomentAnalyzer()

    coordinator = MomentAnalysisCoordinator(
        semantic_analyzer=fake_analyzer
    )

    result = coordinator.analyze(
        create_moment_analysis()
    )

    assert coordinator.last_analysis is result


def test_coordinator_returns_analyzer_result():
    fake_analyzer = FakeSemanticMomentAnalyzer()

    coordinator = MomentAnalysisCoordinator(
        semantic_analyzer=fake_analyzer
    )

    result = coordinator.analyze(
        create_moment_analysis()
    )

    assert (
        result.strongest_interpretation
        == (
            "The strongest moments showed clear "
            "argument structure."
        )
    )


def test_coordinator_rejects_none():
    fake_analyzer = FakeSemanticMomentAnalyzer()

    coordinator = MomentAnalysisCoordinator(
        semantic_analyzer=fake_analyzer
    )

    try:
        coordinator.analyze(None)
    except ValueError as error:
        assert str(error) == (
            "Moment analysis cannot be None."
        )
    else:
        raise AssertionError(
            "Expected ValueError."
        )


def test_coordinator_can_analyze_multiple_times():
    fake_analyzer = FakeSemanticMomentAnalyzer()

    coordinator = MomentAnalysisCoordinator(
        semantic_analyzer=fake_analyzer
    )

    first = coordinator.analyze(
        create_moment_analysis()
    )

    second = coordinator.analyze(
        create_moment_analysis()
    )

    assert len(fake_analyzer.calls) == 2
    assert coordinator.last_analysis is second
    assert first is second