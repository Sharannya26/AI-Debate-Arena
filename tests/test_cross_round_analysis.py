import pytest

from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis


def test_cross_round_analysis_accepts_valid_data():
    analysis = CrossRoundAnalysis(
        overall_trajectory="Performance improved across later rounds.",
        improvement_patterns=["Reasoning became stronger."],
        decline_patterns=["Communication became less clear."],
        stable_patterns=["Responsiveness remained stable."],
        recurring_patterns=["Limited evidence usage appeared repeatedly."],
        cross_dimension_patterns=[
            "Stronger reasoning appeared alongside stronger responsiveness."
        ],
        key_insights=["Later rounds showed stronger overall performance."],
    )

    assert analysis.overall_trajectory == (
        "Performance improved across later rounds."
    )
    assert analysis.improvement_patterns == [
        "Reasoning became stronger."
    ]
    assert analysis.decline_patterns == [
        "Communication became less clear."
    ]
    assert analysis.stable_patterns == [
        "Responsiveness remained stable."
    ]
    assert analysis.recurring_patterns == [
        "Limited evidence usage appeared repeatedly."
    ]
    assert analysis.cross_dimension_patterns == [
        "Stronger reasoning appeared alongside stronger responsiveness."
    ]
    assert analysis.key_insights == [
        "Later rounds showed stronger overall performance."
    ]


def test_cross_round_analysis_requires_overall_trajectory():
    with pytest.raises(ValueError):
        CrossRoundAnalysis(overall_trajectory="")


def test_cross_round_analysis_strips_whitespace():
    analysis = CrossRoundAnalysis(
        overall_trajectory="  Performance improved.  ",
        improvement_patterns=["  Reasoning improved.  "],
        decline_patterns=["  Communication declined.  "],
        stable_patterns=["  Responsiveness stayed stable.  "],
        recurring_patterns=["  Evidence remained limited.  "],
        cross_dimension_patterns=["  Reasoning and responsiveness aligned.  "],
        key_insights=["  Later rounds were stronger.  "],
    )

    assert analysis.overall_trajectory == "Performance improved."
    assert analysis.improvement_patterns == ["Reasoning improved."]
    assert analysis.decline_patterns == ["Communication declined."]
    assert analysis.stable_patterns == ["Responsiveness stayed stable."]
    assert analysis.recurring_patterns == ["Evidence remained limited."]
    assert analysis.cross_dimension_patterns == [
        "Reasoning and responsiveness aligned."
    ]
    assert analysis.key_insights == ["Later rounds were stronger."]


def test_cross_round_analysis_filters_empty_list_items():
    analysis = CrossRoundAnalysis(
        overall_trajectory="Performance remained stable.",
        improvement_patterns=["Reasoning improved.", "", "   "],
        decline_patterns=["Communication declined.", None, ""],
        stable_patterns=["Responsiveness stayed stable.", "   "],
        recurring_patterns=["Evidence remained limited.", None],
        cross_dimension_patterns=["Reasoning aligned with responsiveness.", ""],
        key_insights=["Important insight.", "   ", None],
    )

    assert analysis.improvement_patterns == ["Reasoning improved."]
    assert analysis.decline_patterns == ["Communication declined."]
    assert analysis.stable_patterns == ["Responsiveness stayed stable."]
    assert analysis.recurring_patterns == ["Evidence remained limited."]
    assert analysis.cross_dimension_patterns == [
        "Reasoning aligned with responsiveness."
    ]
    assert analysis.key_insights == ["Important insight."]


def test_cross_round_analysis_defaults_lists_to_empty():
    analysis = CrossRoundAnalysis(
        overall_trajectory="Performance remained stable."
    )

    assert analysis.improvement_patterns == []
    assert analysis.decline_patterns == []
    assert analysis.stable_patterns == []
    assert analysis.recurring_patterns == []
    assert analysis.cross_dimension_patterns == []
    assert analysis.key_insights == []