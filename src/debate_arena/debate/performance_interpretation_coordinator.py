from debate_arena.debate.performance_summary import PerformanceSummary
from debate_arena.debate.semantic_performance_analysis import (
    SemanticPerformanceAnalysis,
)
from debate_arena.debate.semantic_performance_analyzer import (
    SemanticPerformanceAnalyzer,
)


class PerformanceInterpretationCoordinator:
    """
    Coordinates deterministic performance summarization with
    semantic LLM-based interpretation.

    The deterministic summary is produced first. The semantic
    analyzer then interprets that summary without recalculating
    the underlying debate metrics.
    """

    def __init__(
        self,
        semantic_analyzer: SemanticPerformanceAnalyzer | None = None,
    ) -> None:
        self.semantic_analyzer = (
            semantic_analyzer
            or SemanticPerformanceAnalyzer()
        )
        self.last_analysis: (
            SemanticPerformanceAnalysis | None
        ) = None

    def analyze(
        self,
        summary: PerformanceSummary,
    ) -> SemanticPerformanceAnalysis:
        if summary is None:
            raise ValueError(
                "Performance summary cannot be None."
            )

        analysis = self.semantic_analyzer.analyze(
            summary
        )

        self.last_analysis = analysis
        return analysis