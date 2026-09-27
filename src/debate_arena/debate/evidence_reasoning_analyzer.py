import re

from debate_arena.debate.argument import Argument
from debate_arena.debate.evidence_analysis import (
    EvidenceAnalysis,
)
from debate_arena.debate.evidence_reasoning_metrics import (
    EvidenceReasoningMetrics,
)


class EvidenceReasoningAnalyzer:
    """
    Performs deterministic analysis of evidence and reasoning
    across the user's debate arguments.

    This analyzer provides both:

    1. Qualitative findings through EvidenceAnalysis.
    2. Objective measurements through EvidenceReasoningMetrics.

    Deeper semantic interpretation can be handled by Gemini later.
    """

    EVIDENCE_PATTERNS = (
        r"\b\d+(?:\.\d+)?%?\b",
        r"\baccording to\b",
        r"\bstudy\b",
        r"\bstudies\b",
        r"\bresearch\b",
        r"\breport\b",
        r"\breports\b",
        r"\bsurvey\b",
        r"\bsurveys\b",
        r"\bdata\b",
        r"\bstatistics\b",
        r"\bstatistic\b",
        r"\bevidence\b",
        r"\bexample\b",
        r"\bexamples\b",
        r"\bresearch shows\b",
        r"\bstudies show\b",
    )

    REASONING_PATTERNS = (
        r"\bbecause\b",
        r"\bsince\b",
        r"\btherefore\b",
        r"\bthus\b",
        r"\bso\b",
        r"\bas a result\b",
        r"\bwhich means\b",
        r"\bthis means\b",
        r"\bleads to\b",
        r"\bresults in\b",
        r"\bcauses\b",
        r"\bcaused by\b",
        r"\bdue to\b",
        r"\bif\b",
        r"\bthen\b",
    )

    def __init__(self) -> None:
        self.last_metrics: (
            EvidenceReasoningMetrics | None
        ) = None

    def analyze(
        self,
        user_arguments: list[Argument],
    ) -> EvidenceAnalysis:
        """
        Analyze evidence and reasoning across user arguments.

        The objective metrics for the latest analysis are stored
        in self.last_metrics.
        """

        if user_arguments is None:
            raise ValueError(
                "User arguments cannot be None."
            )

        if not user_arguments:
            self.last_metrics = (
                EvidenceReasoningMetrics(
                    total_arguments=0,
                    evidence_arguments=0,
                    reasoning_arguments=0,
                    evidence_coverage=0.0,
                    reasoning_coverage=0.0,
                )
            )

            return EvidenceAnalysis(
                evidence_quality="No evidence identified.",
                reasoning_quality="No reasoning identified.",
            )

        for argument in user_arguments:
            if argument is None:
                raise ValueError(
                    "User arguments cannot contain None."
                )

            if argument.speaker != "user":
                raise ValueError(
                    "All arguments must be from the user."
                )

        evidence_points: list[str] = []
        missing_evidence: list[str] = []

        reasoning_points: list[str] = []
        reasoning_gaps: list[str] = []

        evidence_arguments = 0
        reasoning_arguments = 0

        for argument in user_arguments:
            has_evidence = self._contains_evidence(
                argument.text
            )

            has_reasoning = self._contains_reasoning(
                argument.text
            )

            if has_evidence:
                evidence_arguments += 1

                evidence_points.append(
                    (
                        f"Round {argument.round}: "
                        "Evidence signals were identified."
                    )
                )
            else:
                missing_evidence.append(
                    (
                        f"Round {argument.round}: "
                        "No explicit evidence signals were identified."
                    )
                )

            if has_reasoning:
                reasoning_arguments += 1

                reasoning_points.append(
                    (
                        f"Round {argument.round}: "
                        "Reasoning signals were identified."
                    )
                )
            else:
                reasoning_gaps.append(
                    (
                        f"Round {argument.round}: "
                        "No explicit reasoning signals were identified."
                    )
                )

        total_arguments = len(user_arguments)

        evidence_coverage = (
            evidence_arguments / total_arguments
        )

        reasoning_coverage = (
            reasoning_arguments / total_arguments
        )

        self.last_metrics = EvidenceReasoningMetrics(
            total_arguments=total_arguments,
            evidence_arguments=evidence_arguments,
            reasoning_arguments=reasoning_arguments,
            evidence_coverage=evidence_coverage,
            reasoning_coverage=reasoning_coverage,
        )

        evidence_quality = (
            self._classify_evidence_quality(
                evidence_arguments=evidence_arguments,
                total_arguments=total_arguments,
            )
        )

        reasoning_quality = (
            self._classify_reasoning_quality(
                reasoning_arguments=reasoning_arguments,
                total_arguments=total_arguments,
            )
        )

        return EvidenceAnalysis(
            evidence_quality=evidence_quality,
            reasoning_quality=reasoning_quality,
            evidence_points=evidence_points,
            missing_evidence=missing_evidence,
            reasoning_points=reasoning_points,
            reasoning_gaps=reasoning_gaps,
        )

    @classmethod
    def _contains_evidence(
        cls,
        text: str,
    ) -> bool:
        cleaned_text = text.strip().lower()

        return any(
            re.search(
                pattern,
                cleaned_text,
            )
            for pattern in cls.EVIDENCE_PATTERNS
        )

    @classmethod
    def _contains_reasoning(
        cls,
        text: str,
    ) -> bool:
        cleaned_text = text.strip().lower()

        return any(
            re.search(
                pattern,
                cleaned_text,
            )
            for pattern in cls.REASONING_PATTERNS
        )

    @staticmethod
    def _classify_evidence_quality(
        evidence_arguments: int,
        total_arguments: int,
    ) -> str:
        if total_arguments == 0:
            return "No evidence identified."

        evidence_ratio = (
            evidence_arguments / total_arguments
        )

        if evidence_ratio >= 0.75:
            return "Strong evidence usage."

        if evidence_ratio >= 0.50:
            return "Moderate evidence usage."

        if evidence_ratio > 0:
            return "Limited evidence usage."

        return "No evidence identified."

    @staticmethod
    def _classify_reasoning_quality(
        reasoning_arguments: int,
        total_arguments: int,
    ) -> str:
        if total_arguments == 0:
            return "No reasoning identified."

        reasoning_ratio = (
            reasoning_arguments / total_arguments
        )

        if reasoning_ratio >= 0.75:
            return "Strong reasoning structure."

        if reasoning_ratio >= 0.50:
            return "Moderate reasoning structure."

        if reasoning_ratio > 0:
            return "Limited reasoning structure."

        return "No explicit reasoning structure identified."