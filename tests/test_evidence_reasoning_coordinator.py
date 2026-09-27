from debate_arena.debate.argument import Argument
from debate_arena.debate.evidence_analysis import EvidenceAnalysis
from debate_arena.debate.evidence_reasoning_analyzer import (
    EvidenceReasoningAnalyzer,
)
from debate_arena.debate.evidence_reasoning_coordinator import (
    EvidenceReasoningCoordinator,
)
from debate_arena.debate.evidence_reasoning_metrics import (
    EvidenceReasoningMetrics,
)
from debate_arena.debate.semantic_evidence_reasoning_analyzer import (
    SemanticEvidenceReasoningAnalyzer,
)


class FakeDeterministicAnalyzer:
    def __init__(self):
        self.last_metrics = None

    def analyze(self, user_arguments):
        self.last_metrics = EvidenceReasoningMetrics(
            total_arguments=2,
            evidence_arguments=1,
            reasoning_arguments=1,
            evidence_coverage=0.5,
            reasoning_coverage=0.5,
        )

        return EvidenceAnalysis(
            evidence_quality="Moderate evidence usage.",
            reasoning_quality="Moderate reasoning structure.",
        )


class FakeSemanticAnalyzer:
    def analyze(self, user_arguments):
        return EvidenceAnalysis(
            evidence_quality="Strong evidence usage.",
            reasoning_quality="Strong reasoning structure.",
            evidence_points=[
                "Round 1 contains meaningful supporting evidence."
            ],
            missing_evidence=[
                "Round 2 contains an unsupported claim."
            ],
            reasoning_points=[
                "Round 2 clearly connects a cause to its consequence."
            ],
            reasoning_gaps=[],
        )


def create_user_argument(
    text: str,
    round_number: int,
) -> Argument:
    return Argument(
        speaker="user",
        text=text,
        round=round_number,
        turn="user",
    )


def test_coordinator_combines_metrics_and_semantic_analysis():
    coordinator = EvidenceReasoningCoordinator(
        deterministic_analyzer=FakeDeterministicAnalyzer(),
        semantic_analyzer=FakeSemanticAnalyzer(),
    )

    arguments = [
        create_user_argument(
            "Research supports this claim.",
            1,
        ),
        create_user_argument(
            "This causes better outcomes because it helps students.",
            2,
        ),
    ]

    result = coordinator.analyze(arguments)

    assert result.evidence_coverage == 0.5
    assert result.reasoning_coverage == 0.5

    assert result.evidence_strength == (
        "Strong evidence usage."
    )

    assert result.reasoning_strength == (
        "Strong reasoning structure."
    )

    assert len(result.analysis.evidence_points) == 1
    assert len(result.analysis.reasoning_points) == 1


def test_coordinator_stores_last_insight():
    coordinator = EvidenceReasoningCoordinator(
        deterministic_analyzer=FakeDeterministicAnalyzer(),
        semantic_analyzer=FakeSemanticAnalyzer(),
    )

    arguments = [
        create_user_argument(
            "Research supports this claim.",
            1,
        ),
    ]

    result = coordinator.analyze(arguments)

    assert coordinator.last_insight is result


def test_coordinator_adds_evidence_coaching():
    coordinator = EvidenceReasoningCoordinator(
        deterministic_analyzer=FakeDeterministicAnalyzer(),
        semantic_analyzer=FakeSemanticAnalyzer(),
    )

    coaching = coordinator._build_coaching_points(
        evidence_coverage=0.25,
        reasoning_coverage=0.75,
        analysis=EvidenceAnalysis(
            evidence_quality="Limited evidence usage.",
            reasoning_quality="Strong reasoning structure.",
            missing_evidence=["Round 1 needs evidence."],
        ),
    )

    assert any(
        "evidence" in point.lower()
        for point in coaching
    )


def test_coordinator_adds_reasoning_coaching():
    coordinator = EvidenceReasoningCoordinator(
        deterministic_analyzer=FakeDeterministicAnalyzer(),
        semantic_analyzer=FakeSemanticAnalyzer(),
    )

    coaching = coordinator._build_coaching_points(
        evidence_coverage=0.75,
        reasoning_coverage=0.25,
        analysis=EvidenceAnalysis(
            evidence_quality="Strong evidence usage.",
            reasoning_quality="Limited reasoning structure.",
            reasoning_gaps=["Round 2 needs clearer reasoning."],
        ),
    )

    assert any(
        "logical" in point.lower()
        or "reasoning" in point.lower()
        for point in coaching
    )


def test_coordinator_rejects_none_arguments():
    coordinator = EvidenceReasoningCoordinator(
        deterministic_analyzer=FakeDeterministicAnalyzer(),
        semantic_analyzer=FakeSemanticAnalyzer(),
    )

    try:
        coordinator.analyze(None)
        assert False
    except ValueError as exc:
        assert "cannot be None" in str(exc)


def test_coordinator_rejects_empty_arguments():
    coordinator = EvidenceReasoningCoordinator(
        deterministic_analyzer=FakeDeterministicAnalyzer(),
        semantic_analyzer=FakeSemanticAnalyzer(),
    )

    try:
        coordinator.analyze([])
        assert False
    except ValueError as exc:
        assert "At least one user argument" in str(exc)