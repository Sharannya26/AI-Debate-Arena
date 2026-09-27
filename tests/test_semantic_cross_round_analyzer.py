import pytest

from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis
from debate_arena.debate.semantic_cross_round_analyzer import (
    SemanticCrossRoundAnalyzer,
)


class FakeLLMClient:
    def __init__(self, response_data):
        self.response_data = response_data
        self.prompts = []

    def analyze_cross_round_performance(self, prompt):
        self.prompts.append(prompt)
        return self.response_data


def make_analysis():
    return CrossRoundAnalysis(
        overall_trajectory="Performance improved across the debate.",
        improvement_patterns=[
            "Reasoning quality improved across the debate."
        ],
        decline_patterns=[
            "Communication quality declined across the debate."
        ],
        stable_patterns=[
            "Responsiveness remained stable across the debate."
        ],
        recurring_patterns=[
            "Evidence usage remained consistently limited."
        ],
        cross_dimension_patterns=[],
        key_insights=[],
    )


def make_response_data():
    return {
        "overall_interpretation": (
            "Performance became stronger in later rounds."
        ),
        "improvement_interpretation": (
            "Reasoning quality showed improvement."
        ),
        "decline_interpretation": (
            "Communication quality declined in later rounds."
        ),
        "stability_interpretation": (
            "Responsiveness remained stable."
        ),
        "recurring_interpretation": (
            "Limited evidence usage appeared repeatedly."
        ),
        "cross_dimension_interpretation": (
            "Reasoning improved while evidence usage remained limited."
        ),
        "key_insights": [
            "Later rounds showed stronger reasoning."
        ],
    }


def make_analyzer():
    fake_llm = FakeLLMClient(make_response_data())

    analyzer = SemanticCrossRoundAnalyzer(
        llm_client=fake_llm,
        prompt_builder=lambda analysis: "fake cross-round prompt",
    )

    return analyzer, fake_llm


def test_analyzer_rejects_none_analysis():
    analyzer, _ = make_analyzer()

    with pytest.raises(ValueError):
        analyzer.analyze(None)


def test_analyzer_returns_cross_round_analysis():
    analyzer, _ = make_analyzer()

    result = analyzer.analyze(make_analysis())

    assert isinstance(result, CrossRoundAnalysis)


def test_analyzer_maps_overall_interpretation():
    analyzer, _ = make_analyzer()

    result = analyzer.analyze(make_analysis())

    assert result.overall_trajectory == (
        "Performance became stronger in later rounds."
    )


def test_analyzer_maps_all_interpretations():
    analyzer, _ = make_analyzer()

    result = analyzer.analyze(make_analysis())

    assert result.improvement_patterns == [
        "Reasoning quality showed improvement."
    ]

    assert result.decline_patterns == [
        "Communication quality declined in later rounds."
    ]

    assert result.stable_patterns == [
        "Responsiveness remained stable."
    ]

    assert result.recurring_patterns == [
        "Limited evidence usage appeared repeatedly."
    ]

    assert result.cross_dimension_patterns == [
        "Reasoning improved while evidence usage remained limited."
    ]


def test_analyzer_maps_key_insights():
    analyzer, _ = make_analyzer()

    result = analyzer.analyze(make_analysis())

    assert result.key_insights == [
        "Later rounds showed stronger reasoning."
    ]


def test_analyzer_uses_prompt_builder():
    analyzer, fake_llm = make_analyzer()

    analyzer.analyze(make_analysis())

    assert fake_llm.prompts == [
        "fake cross-round prompt"
    ]


def test_analyzer_stores_last_analysis():
    analyzer, _ = make_analyzer()

    result = analyzer.analyze(make_analysis())

    assert analyzer.last_analysis is result


def test_analyzer_rejects_non_dictionary_response():
    class InvalidLLMClient:
        def analyze_cross_round_performance(self, prompt):
            return "invalid"

    analyzer = SemanticCrossRoundAnalyzer(
        llm_client=InvalidLLMClient(),
        prompt_builder=lambda analysis: "fake prompt",
    )

    with pytest.raises(RuntimeError):
        analyzer.analyze(make_analysis())


def test_analyzer_rejects_missing_response_fields():
    class IncompleteLLMClient:
        def analyze_cross_round_performance(self, prompt):
            return {
                "overall_interpretation": "Some interpretation."
            }

    analyzer = SemanticCrossRoundAnalyzer(
        llm_client=IncompleteLLMClient(),
        prompt_builder=lambda analysis: "fake prompt",
    )

    with pytest.raises(RuntimeError):
        analyzer.analyze(make_analysis())


def test_analyzer_rejects_empty_prompt():
    analyzer = SemanticCrossRoundAnalyzer(
        llm_client=FakeLLMClient(make_response_data()),
        prompt_builder=lambda analysis: "",
    )

    with pytest.raises(RuntimeError):
        analyzer.analyze(make_analysis())