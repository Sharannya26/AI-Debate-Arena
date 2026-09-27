import pytest

from debate_arena.debate.argument import Argument
from debate_arena.debate.evidence_reasoning_analyzer import (
    EvidenceReasoningAnalyzer,
)


def create_user_argument(
    text: str,
    round_number: int,
) -> Argument:
    return Argument(
        speaker="user",
        text=text,
        round=round_number,
        turn=1,
    )


def test_analyzer_requires_valid_arguments():
    analyzer = EvidenceReasoningAnalyzer()

    result = analyzer.analyze([])

    assert (
        result.evidence_quality
        == "No evidence identified."
    )

    assert (
        result.reasoning_quality
        == "No reasoning identified."
    )


def test_analyzer_detects_evidence_signals():
    analyzer = EvidenceReasoningAnalyzer()

    arguments = [
        create_user_argument(
            "According to a recent study, 65% of students "
            "use social media for educational purposes.",
            1,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert (
        result.evidence_quality
        == "Strong evidence usage."
    )

    assert len(result.evidence_points) == 1
    assert len(result.missing_evidence) == 0


def test_analyzer_detects_reasoning_signals():
    analyzer = EvidenceReasoningAnalyzer()

    arguments = [
        create_user_argument(
            "Students should have access to online education "
            "because it provides flexible learning opportunities.",
            1,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert (
        result.reasoning_quality
        == "Strong reasoning structure."
    )

    assert len(result.reasoning_points) == 1
    assert len(result.reasoning_gaps) == 0


def test_analyzer_detects_missing_evidence():
    analyzer = EvidenceReasoningAnalyzer()

    arguments = [
        create_user_argument(
            "Social media is useful because students can "
            "learn from educational content.",
            1,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert (
        result.evidence_quality
        == "No evidence identified."
    )

    assert len(result.missing_evidence) == 1


def test_analyzer_detects_missing_reasoning():
    analyzer = EvidenceReasoningAnalyzer()

    arguments = [
        create_user_argument(
            "Students need access to education.",
            1,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert (
        result.reasoning_quality
        == "No explicit reasoning structure identified."
    )

    assert len(result.reasoning_gaps) == 1


def test_analyzer_handles_mixed_evidence_usage():
    analyzer = EvidenceReasoningAnalyzer()

    arguments = [
        create_user_argument(
            "According to a study, online learning "
            "helps students.",
            1,
        ),
        create_user_argument(
            "Online education provides flexibility "
            "because students can learn remotely.",
            2,
        ),
        create_user_argument(
            "Students should have access to education.",
            3,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert (
        result.evidence_quality
        == "Limited evidence usage."
    )

    assert len(result.evidence_points) == 1
    assert len(result.missing_evidence) == 2


def test_analyzer_handles_mixed_reasoning_usage():
    analyzer = EvidenceReasoningAnalyzer()

    arguments = [
        create_user_argument(
            "Online education is useful because "
            "students can learn remotely.",
            1,
        ),
        create_user_argument(
            "Students benefit from education.",
            2,
        ),
        create_user_argument(
            "Technology improves access, therefore "
            "students can reach more resources.",
            3,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert (
        result.reasoning_quality
        == "Moderate reasoning structure."
    )

    assert len(result.reasoning_points) == 2
    assert len(result.reasoning_gaps) == 1


def test_non_user_argument_is_rejected():
    analyzer = EvidenceReasoningAnalyzer()

    arguments = [
        create_user_argument(
            "Students need education.",
            1,
        ),
        Argument(
            speaker="ai",
            text="Education has benefits.",
            round=2,
            turn=1,
        ),
    ]

    with pytest.raises(
        ValueError,
        match="All arguments must be from the user",
    ):
        analyzer.analyze(arguments)


def test_none_argument_is_rejected():
    analyzer = EvidenceReasoningAnalyzer()

    arguments = [
        create_user_argument(
            "Students need education.",
            1,
        ),
        None,
    ]

    with pytest.raises(
        ValueError,
        match="User arguments cannot contain None",
    ):
        analyzer.analyze(arguments)


def test_round_numbers_are_preserved_in_findings():
    analyzer = EvidenceReasoningAnalyzer()

    arguments = [
        create_user_argument(
            "According to research, education helps students.",
            2,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert (
        "Round 2"
        in result.evidence_points[0]
    )

def test_analyzer_calculates_evidence_metrics():
    analyzer = EvidenceReasoningAnalyzer()

    arguments = [
        create_user_argument(
            "According to research, online education helps students.",
            1,
        ),
        create_user_argument(
            "Online education provides flexibility because students "
            "can learn remotely.",
            2,
        ),
        create_user_argument(
            "Students need access to education.",
            3,
        ),
    ]

    analyzer.analyze(arguments)

    assert analyzer.last_metrics is not None

    assert analyzer.last_metrics.total_arguments == 3
    assert analyzer.last_metrics.evidence_arguments == 1
    assert analyzer.last_metrics.reasoning_arguments == 1

    assert analyzer.last_metrics.evidence_coverage == pytest.approx(
        1 / 3
    )

    assert analyzer.last_metrics.reasoning_coverage == pytest.approx(
        1 / 3
    )


def test_analyzer_metrics_are_zero_for_empty_arguments():
    analyzer = EvidenceReasoningAnalyzer()

    analyzer.analyze([])

    assert analyzer.last_metrics is not None

    assert analyzer.last_metrics.total_arguments == 0
    assert analyzer.last_metrics.evidence_arguments == 0
    assert analyzer.last_metrics.reasoning_arguments == 0
    assert analyzer.last_metrics.evidence_coverage == 0.0
    assert analyzer.last_metrics.reasoning_coverage == 0.0


def test_analyzer_updates_metrics_on_each_analysis():
    analyzer = EvidenceReasoningAnalyzer()

    first_arguments = [
        create_user_argument(
            "According to research, education helps students.",
            1,
        ),
    ]

    analyzer.analyze(first_arguments)

    assert analyzer.last_metrics is not None
    assert analyzer.last_metrics.evidence_arguments == 1

    second_arguments = [
        create_user_argument(
            "Students need education.",
            1,
        ),
        create_user_argument(
            "Education provides opportunities because "
            "students can learn.",
            2,
        ),
    ]

    analyzer.analyze(second_arguments)

    assert analyzer.last_metrics is not None
    assert analyzer.last_metrics.total_arguments == 2
    assert analyzer.last_metrics.evidence_arguments == 0
    assert analyzer.last_metrics.reasoning_arguments == 1    