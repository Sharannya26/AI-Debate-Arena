from debate_arena.debate.advanced_debate_analysis import (
    AdvancedDebateAnalysis,
)
from debate_arena.debate.advanced_debate_analyzer import (
    AdvancedDebateAnalyzer,
)
from debate_arena.debate.debate_performance import DebatePerformance
from debate_arena.debate.performance_summary import PerformanceSummary


class AdvancedAnalysisCoordinator:
    """
    Coordinates advanced semantic interpretation of debate performance.

    The coordinator keeps higher-level application code independent of
    prompt construction and LLM details.
    """

    def __init__(
        self,
        analyzer: AdvancedDebateAnalyzer | None = None,
    ) -> None:
        self.analyzer = analyzer or AdvancedDebateAnalyzer()
        self.last_analysis: AdvancedDebateAnalysis | None = None

    def analyze(
        self,
        performance: DebatePerformance,
        summary: PerformanceSummary,
    ) -> AdvancedDebateAnalysis:
        """
        Run advanced semantic analysis and store the latest result.
        """

        if performance is None:
            raise ValueError("Debate performance cannot be None.")

        if summary is None:
            raise ValueError("Performance summary cannot be None.")

        analysis = self.analyzer.analyze(
            performance,
            summary,
        )

        self.last_analysis = analysis

        return analysis