import pytest

from debate_arena.debate.coaching_priority_analyzer import (
    CoachingPriorityAnalyzer,
)
from debate_arena.debate.round_performance import RoundPerformance


def create_round(
    round_number: int,
    argument_quality: str = "Strong argument quality.",
    communication_quality: str = "Clear communication.",
    evidence_usage: str = "Strong evidence usage.",
    reasoning_quality: str = "Strong reasoning.",
    responsiveness: str | None = "Highly responsive.",
) -> RoundPerformance:
    return RoundPerformance(
        round=round_number,
        argument_quality=argument_quality,
        communication_quality=communication_quality,
        evidence_usage=evidence_usage,
        reasoning_quality=reasoning_quality,
        responsiveness=responsiveness,
    )


def test_detects_argument_quality_priority():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze(
        [
            create_round(
                1,
                argument_quality="Limited argument quality.",
            )
        ]
    )

    assert any(
        "Strengthen the structure" in priority
        for priority in priorities
    )


def test_detects_communication_priority():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze(
        [
            create_round(
                1,
                communication_quality="Weak communication.",
            )
        ]
    )

    assert any(
        "Improve the clarity" in priority
        for priority in priorities
    )


def test_detects_evidence_priority():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze(
        [
            create_round(
                1,
                evidence_usage="Limited evidence usage.",
            )
        ]
    )

    assert any(
        "Support major claims" in priority
        for priority in priorities
    )


def test_detects_reasoning_priority():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze(
        [
            create_round(
                1,
                reasoning_quality="Weak reasoning.",
            )
        ]
    )

    assert any(
        "logical connection" in priority
        for priority in priorities
    )


def test_detects_responsiveness_priority():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze(
        [
            create_round(
                1,
                responsiveness="Not responsive to opponent.",
            )
        ]
    )

    assert any(
        "opponent's main point" in priority
        for priority in priorities
    )


def test_deduplicates_same_priority_across_rounds():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze(
        [
            create_round(
                1,
                evidence_usage="Limited evidence usage.",
            ),
            create_round(
                2,
                evidence_usage="Limited evidence usage.",
            ),
            create_round(
                3,
                evidence_usage="Limited evidence usage.",
            ),
        ]
    )

    evidence_priorities = [
        priority
        for priority in priorities
        if "Support major claims" in priority
    ]

    assert len(evidence_priorities) == 1


def test_detects_multiple_priorities():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze(
        [
            create_round(
                1,
                argument_quality="Weak argument quality.",
                evidence_usage="Limited evidence usage.",
                reasoning_quality="Weak reasoning.",
            )
        ]
    )

    assert len(priorities) == 3


def test_does_not_create_priority_for_strong_performance():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze(
        [
            create_round(
                1,
                argument_quality="Strong argument quality.",
                communication_quality="Excellent communication.",
                evidence_usage="Strong evidence usage.",
                reasoning_quality="Strong reasoning.",
                responsiveness="Highly responsive.",
            )
        ]
    )

    assert priorities == []


def test_ignores_missing_responsiveness():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze(
        [
            create_round(
                1,
                responsiveness=None,
            )
        ]
    )

    assert priorities == []


def test_handles_empty_input():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze([])

    assert priorities == []


def test_rejects_none_input():
    analyzer = CoachingPriorityAnalyzer()

    with pytest.raises(
        ValueError,
        match="Round performances cannot be None",
    ):
        analyzer.analyze(None)


def test_rejects_none_round_performance():
    analyzer = CoachingPriorityAnalyzer()

    with pytest.raises(
        ValueError,
        match="Round performances cannot contain None",
    ):
        analyzer.analyze([None])


def test_ignores_blank_dimension_values():
    analyzer = CoachingPriorityAnalyzer()

    priorities = []

    analyzer._check_dimension(
        priorities,
        "argument quality",
        "",
    )

    analyzer._check_dimension(
        priorities,
        "communication quality",
        "  ",
    )

    assert priorities == []


def test_preserves_priority_order():
    analyzer = CoachingPriorityAnalyzer()

    priorities = analyzer.analyze(
        [
            create_round(
                1,
                argument_quality="Weak argument quality.",
                communication_quality="Weak communication.",
                evidence_usage="Limited evidence usage.",
            )
        ]
    )

    assert priorities[0].startswith("Strengthen")
    assert priorities[1].startswith("Improve")
    assert priorities[2].startswith("Support")