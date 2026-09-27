from debate_arena.debate.argument import Argument
from debate_arena.debate.evidence_reasoning_analyzer import (
    EvidenceReasoningAnalyzer,
)
from debate_arena.debate.evidence_reasoning_insight import (
    EvidenceReasoningInsight,
)
from debate_arena.debate.semantic_evidence_reasoning_analyzer import (
    SemanticEvidenceReasoningAnalyzer,
)


class EvidenceReasoningCoordinator:
    """
    Combines deterministic evidence/reasoning metrics
    with semantic LLM interpretation.
    """

    def __init__(
        self,
        deterministic_analyzer: EvidenceReasoningAnalyzer | None = None,
        semantic_analyzer: (
            SemanticEvidenceReasoningAnalyzer | None
        ) = None,
    ) -> None:
        self.deterministic_analyzer = (
            deterministic_analyzer
            or EvidenceReasoningAnalyzer()
        )

        self.semantic_analyzer = (
            semantic_analyzer
            or SemanticEvidenceReasoningAnalyzer()
        )

        self.last_insight: EvidenceReasoningInsight | None = None

    def analyze(
        self,
        user_arguments: list[Argument],
    ) -> EvidenceReasoningInsight:
        if user_arguments is None:
            raise ValueError(
                "User arguments cannot be None."
            )

        if not user_arguments:
            raise ValueError(
                "At least one user argument is required."
            )

        deterministic_analysis = (
            self.deterministic_analyzer.analyze(
                user_arguments
            )
        )

        metrics = (
            self.deterministic_analyzer.last_metrics
        )

        if metrics is None:
            raise RuntimeError(
                "Deterministic analyzer did not produce metrics."
            )

        semantic_analysis = (
            self.semantic_analyzer.analyze(
                user_arguments
            )
        )

        coaching_points = (
            self._build_coaching_points(
                metrics.evidence_coverage,
                metrics.reasoning_coverage,
                semantic_analysis,
            )
        )

        insight = EvidenceReasoningInsight(
            metrics=metrics,
            analysis=semantic_analysis,
            evidence_coverage=metrics.evidence_coverage,
            reasoning_coverage=metrics.reasoning_coverage,
            evidence_strength=semantic_analysis.evidence_quality,
            reasoning_strength=semantic_analysis.reasoning_quality,
            coaching_points=coaching_points,
        )

        self.last_insight = insight

        return insight

    @staticmethod
    def _build_coaching_points(
        evidence_coverage: float,
        reasoning_coverage: float,
        analysis,
    ) -> list[str]:
        coaching_points: list[str] = []

        if evidence_coverage < 0.50:
            coaching_points.append(
                "Support more major claims with concrete "
                "evidence, examples, or data."
            )

        if reasoning_coverage < 0.50:
            coaching_points.append(
                "Make the logical connection between claims "
                "and conclusions more explicit."
            )

        if analysis.missing_evidence:
            coaching_points.append(
                "Review claims identified as lacking "
                "supporting evidence."
            )

        if analysis.reasoning_gaps:
            coaching_points.append(
                "Strengthen the reasoning gaps identified "
                "across the debate rounds."
            )

        if not coaching_points:
            coaching_points.append(
                "Continue supporting claims with evidence "
                "and clearly connecting your reasoning."
            )

        return coaching_points