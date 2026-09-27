from debate_arena.debate.moment_analysis import MomentAnalysis

from debate_arena.debate.semantic_moment_analysis import (
    SemanticMomentAnalysis,
)

from debate_arena.debate.semantic_moment_analyzer import (
    SemanticMomentAnalyzer,
)


class MomentAnalysisCoordinator:
    """
    Coordinates deterministic moment findings with the
    semantic interpretation layer.

    The deterministic MomentAnalysis identifies the moments.
    The SemanticMomentAnalyzer interprets those moments.
    """

    def __init__(
        self,
        semantic_analyzer: SemanticMomentAnalyzer | None = None,
        llm_client=None,
    ) -> None:
        self.semantic_analyzer = (
            semantic_analyzer
            or SemanticMomentAnalyzer(
                llm_client=llm_client
            )
        )

        self.last_analysis: SemanticMomentAnalysis | None = None

    def analyze(
        self,
        analysis: MomentAnalysis,
    ) -> SemanticMomentAnalysis:
        """
        Run semantic interpretation for the supplied
        deterministic moment analysis.
        """

        if analysis is None:
            raise ValueError(
                "Moment analysis cannot be None."
            )

        result = self.semantic_analyzer.analyze(
            analysis
        )

        self.last_analysis = result

        return result