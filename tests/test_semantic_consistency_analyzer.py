from unittest.mock import Mock

import pytest

from debate_arena.debate.argument import Argument
from debate_arena.debate.consistency_analysis import (
    ConsistencyAnalysis,
)
from debate_arena.debate.semantic_consistency_analyzer import (
    SemanticConsistencyAnalyzer,
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


def test_semantic_consistency_uses_llm():
    llm = Mock()

    llm.analyze_consistency.return_value = {
        "consistency": "Highly consistent.",
        "consistent_points": [
            "The user maintains the same position."
        ],
        "inconsistent_points": [],
    }

    analyzer = SemanticConsistencyAnalyzer(
        llm_client=llm,
    )

    arguments = [
        create_user_argument(
            "Students should have access to online education.",
            1,
        ),
        create_user_argument(
            "Learning platforms provide students with opportunities.",
            2,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert isinstance(
        result,
        ConsistencyAnalysis,
    )

    assert (
        result.consistency
        == "Highly consistent."
    )

    assert result.consistent_points == [
        "The user maintains the same position."
    ]

    assert result.inconsistent_points == []

    llm.analyze_consistency.assert_called_once()


def test_semantic_consistency_passes_all_arguments_to_prompt():
    llm = Mock()

    llm.analyze_consistency.return_value = {
        "consistency": "Mostly consistent.",
        "consistent_points": [],
        "inconsistent_points": [],
    }

    analyzer = SemanticConsistencyAnalyzer(
        llm_client=llm,
    )

    first_argument = (
        "Students should have access to online education."
    )

    second_argument = (
        "Learning platforms provide students with opportunities."
    )

    analyzer.analyze(
        [
            create_user_argument(
                first_argument,
                1,
            ),
            create_user_argument(
                second_argument,
                2,
            ),
        ]
    )

    prompt = (
        llm.analyze_consistency
        .call_args[0][0]
    )

    assert first_argument in prompt
    assert second_argument in prompt


def test_semantic_consistency_rejects_ai_argument():
    llm = Mock()

    analyzer = SemanticConsistencyAnalyzer(
        llm_client=llm,
    )

    arguments = [
        create_user_argument(
            "Students should have access to education.",
            1,
        ),
        Argument(
            speaker="ai",
            text="Education has risks.",
            round=2,
            turn=1,
        ),
    ]

    with pytest.raises(
        ValueError,
        match="All arguments must be from the user",
    ):
        analyzer.analyze(arguments)

    llm.analyze_consistency.assert_not_called()


def test_semantic_consistency_rejects_none_argument():
    llm = Mock()

    analyzer = SemanticConsistencyAnalyzer(
        llm_client=llm,
    )

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

    llm.analyze_consistency.assert_not_called()


def test_semantic_consistency_requires_two_arguments():
    llm = Mock()

    analyzer = SemanticConsistencyAnalyzer(
        llm_client=llm,
    )

    with pytest.raises(
        ValueError,
        match="At least two user arguments are required",
    ):
        analyzer.analyze(
            [
                create_user_argument(
                    "Only one argument.",
                    1,
                )
            ]
        )

    llm.analyze_consistency.assert_not_called()


def test_semantic_consistency_handles_inconsistent_result():
    llm = Mock()

    llm.analyze_consistency.return_value = {
        "consistency": "Inconsistent.",
        "consistent_points": [],
        "inconsistent_points": [
            (
                "Round 1 supports access to social media, "
                "while Round 2 opposes access."
            )
        ],
    }

    analyzer = SemanticConsistencyAnalyzer(
        llm_client=llm,
    )

    result = analyzer.analyze(
        [
            create_user_argument(
                "Teenagers should have access to social media.",
                1,
            ),
            create_user_argument(
                "Teenagers should not have access to social media.",
                2,
            ),
        ]
    )

    assert result.consistency == "Inconsistent."

    assert len(
        result.inconsistent_points
    ) == 1