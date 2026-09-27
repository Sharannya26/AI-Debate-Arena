import pytest

from debate_arena.debate.advanced_debate_analysis import (
    AdvancedDebateAnalysis,
)


def test_creates_valid_analysis():
    analysis = AdvancedDebateAnalysis(
        overall_interpretation="The user's performance became more structured.",
        cross_dimension_patterns=[
            "Strong reasoning worked alongside good responsiveness."
        ],
        round_patterns=[
            "Reasoning became clearer in later rounds."
        ],
        strengths_interpretation="The user consistently developed logical responses.",
        weaknesses_interpretation="Some claims lacked supporting evidence.",
        coaching_interpretation="Support major claims with concrete examples.",
        key_insights=[
            "Reasoning remained a recurring strength.",
            "Evidence support could be improved.",
        ],
    )

    assert (
        analysis.overall_interpretation
        == "The user's performance became more structured."
    )
    assert len(analysis.cross_dimension_patterns) == 1
    assert len(analysis.round_patterns) == 1
    assert len(analysis.key_insights) == 2


def test_strips_text_fields():
    analysis = AdvancedDebateAnalysis(
        overall_interpretation="  Overall interpretation.  ",
        strengths_interpretation="  Strength interpretation.  ",
        weaknesses_interpretation="  Weakness interpretation.  ",
        coaching_interpretation="  Coaching interpretation.  ",
    )

    assert analysis.overall_interpretation == "Overall interpretation."
    assert analysis.strengths_interpretation == "Strength interpretation."
    assert analysis.weaknesses_interpretation == "Weakness interpretation."
    assert analysis.coaching_interpretation == "Coaching interpretation."


def test_filters_empty_list_items():
    analysis = AdvancedDebateAnalysis(
        overall_interpretation="Valid interpretation.",
        cross_dimension_patterns=[
            " Pattern one ",
            "",
            "   ",
            "Pattern two",
        ],
        round_patterns=[
            "",
            " Round pattern ",
        ],
        key_insights=[
            " Insight one ",
            "",
            None,
            "Insight two",
        ],
    )

    assert analysis.cross_dimension_patterns == [
        "Pattern one",
        "Pattern two",
    ]

    assert analysis.round_patterns == [
        "Round pattern",
    ]

    assert analysis.key_insights == [
        "Insight one",
        "Insight two",
    ]


def test_rejects_empty_overall_interpretation():
    with pytest.raises(ValueError, match="Overall interpretation cannot be empty"):
        AdvancedDebateAnalysis(
            overall_interpretation="   ",
        )


def test_all_optional_fields_default_to_empty_values():
    analysis = AdvancedDebateAnalysis(
        overall_interpretation="Valid interpretation."
    )

    assert analysis.cross_dimension_patterns == []
    assert analysis.round_patterns == []
    assert analysis.strengths_interpretation == ""
    assert analysis.weaknesses_interpretation == ""
    assert analysis.coaching_interpretation == ""
    assert analysis.key_insights == []