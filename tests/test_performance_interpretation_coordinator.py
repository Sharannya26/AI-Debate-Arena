from debate_arena.debate.performance_interpretation_coordinator import (
    PerformanceInterpretationCoordinator,
)
from debate_arena.debate.performance_summary import (
    PerformanceSummary,
)
from debate_arena.debate.semantic_performance_analysis import (
    SemanticPerformanceAnalysis,
)


class FakeSemanticAnalyzer:
    def __init__(self):
        self.received_summary = None

    def analyze(
        self,
        summary: PerformanceSummary,
    ) -> SemanticPerformanceAnalysis:
        self.received_summary = summary

        return SemanticPerformanceAnalysis(
            overall_interpretation=(
                "The user's performance became "
                "more structured."
            ),
            strengths_interpretation=(
                "Reasoning remained strong."
            ),
            weaknesses_interpretation=(
                "Evidence usage needs improvement."
            ),
            coaching_interpretation=(
                "Support claims with evidence."
            ),
            key_insights=[
                "Reasoning remained consistent.",
            ],
        )


def create_summary():
    return PerformanceSummary(
        overall_summary="Performance improved.",
        dimension_summaries={
            "reasoning quality":
                "Reasoning quality remained consistent.",
            "evidence usage":
                "Evidence usage varied across the debate.",
        },
        strongest_moments=[
            "Round 2: Strong reasoning."
        ],
        weakest_moments=[
            "Round 3: Weak evidence usage."
        ],
        coaching_priorities=[
            "Support major claims with evidence."
        ],
    )


def test_coordinator_returns_semantic_analysis():
    fake_analyzer = FakeSemanticAnalyzer()

    coordinator = PerformanceInterpretationCoordinator(
        semantic_analyzer=fake_analyzer
    )

    result = coordinator.analyze(
        create_summary()
    )

    assert isinstance(
        result,
        SemanticPerformanceAnalysis,
    )

    assert (
        result.overall_interpretation
        == "The user's performance became "
        "more structured."
    )


def test_coordinator_passes_summary_to_analyzer():
    fake_analyzer = FakeSemanticAnalyzer()

    coordinator = PerformanceInterpretationCoordinator(
        semantic_analyzer=fake_analyzer
    )

    summary = create_summary()

    coordinator.analyze(summary)

    assert fake_analyzer.received_summary is summary


def test_coordinator_stores_last_analysis():
    fake_analyzer = FakeSemanticAnalyzer()

    coordinator = PerformanceInterpretationCoordinator(
        semantic_analyzer=fake_analyzer
    )

    result = coordinator.analyze(
        create_summary()
    )

    assert coordinator.last_analysis is result


def test_coordinator_rejects_none_summary():
    fake_analyzer = FakeSemanticAnalyzer()

    coordinator = PerformanceInterpretationCoordinator(
        semantic_analyzer=fake_analyzer
    )

    try:
        coordinator.analyze(None)
    except ValueError as error:
        assert str(error) == (
            "Performance summary cannot be None."
        )
    else:
        raise AssertionError(
            "Expected ValueError."
        )