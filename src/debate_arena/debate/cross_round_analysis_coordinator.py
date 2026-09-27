from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis

from debate_arena.debate.cross_round_analyzer import CrossRoundAnalyzer

from debate_arena.debate.round_performance import RoundPerformance

from debate_arena.debate.semantic_cross_round_analyzer import (
    SemanticCrossRoundAnalyzer,
)


class CrossRoundAnalysisCoordinator:
    """
    Coordinates deterministic and semantic cross-round analysis.

    The deterministic analyzer identifies observable changes and patterns.
    The semantic analyzer interprets those findings.
    """

    def __init__(
        self,
        deterministic_analyzer=None,
        semantic_analyzer=None,
        llm_client=None,
    ) -> None:
        self.deterministic_analyzer = (
            deterministic_analyzer or CrossRoundAnalyzer()
        )

        self.semantic_analyzer = (
            semantic_analyzer
            or SemanticCrossRoundAnalyzer(
                llm_client=llm_client
            )
        )

        self.last_analysis: CrossRoundAnalysis | None = None

    def analyze(
        self,
        round_performances: list[RoundPerformance],
    ) -> CrossRoundAnalysis:
        """
        Run deterministic and semantic cross-round analysis.

        Raises:
            ValueError: If round performances are None or empty.
        """

        if round_performances is None:
            raise ValueError(
                "Round performances cannot be None."
            )

        if not round_performances:
            raise ValueError(
                "At least one round performance is required."
            )

        deterministic_analysis = (
            self.deterministic_analyzer.analyze(
                round_performances
            )
        )

        semantic_analysis = self.semantic_analyzer.analyze(
            deterministic_analysis
        )

        self.last_analysis = semantic_analysis

        return semantic_analysis