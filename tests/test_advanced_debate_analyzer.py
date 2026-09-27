from debate_arena.debate.advanced_debate_analysis import (
    AdvancedDebateAnalysis,
)
from debate_arena.debate.advanced_debate_analyzer import (
    AdvancedDebateAnalyzer,
)
from debate_arena.debate.debate_performance import DebatePerformance
from debate_arena.debate.performance_summary import PerformanceSummary
from debate_arena.debate.round_performance import RoundPerformance


class FakeLLMClient:
    def __init__(self):
        self.received_prompt = None

    def analyze_advanced_debate_performance(self, prompt):
        self.received_prompt = prompt

        return {
            "overall_interpretation": (
                "The user's reasoning became more developed."
            ),
            "cross_dimension_patterns": [
                "Reasoning and responsiveness worked together."
            ],
            "round_patterns": [
                "Reasoning improved in the later round."
            ],
            "strengths_interpretation": (
                "The user consistently developed logical responses."
            ),
            "weaknesses_interpretation": (
                "Some claims lacked supporting evidence."
            ),
            "coaching_interpretation": (
                "Support major claims with concrete evidence."
            ),
            "key_insights": [
                "Reasoning was a recurring strength."
            ],
        }


class FakePromptBuilder:
    def __init__(self):
        self.received_performance = None
        self.received_summary = None

    def __call__(self, performance, summary):
        self.received_performance = performance
        self.received_summary = summary

        return "Advanced debate analysis prompt."


def create_performance():
    return DebatePerformance(
        round_performances=[
            RoundPerformance(
                round=1,
                argument_quality="Argument contains a clear claim.",
                communication_quality="Speech was delivered clearly.",
                evidence_usage="Limited evidence was identified.",
                reasoning_quality="Reasoning was identified.",
                responsiveness="Response addressed the opponent's point.",
            )
        ],
        argument_quality="Argument quality was clear.",
        communication_quality="Communication remained clear.",
        responsiveness="Responsiveness was strong.",
        consistency="Mostly consistent.",
        evidence_usage="Evidence usage was limited.",
        reasoning_quality="Reasoning was clear.",
        strongest_moments=["Strong reasoning was identified."],
        weakest_moments=["Limited evidence was identified."],
        coaching_priorities=[
            "Support major claims with concrete evidence."
        ],
    )


def create_summary():
    return PerformanceSummary(
        overall_summary="Performance was generally clear.",
        dimension_summaries={
            "argument quality": "Argument quality was clear.",
            "communication quality": "Communication remained clear.",
            "responsiveness": "Responsiveness was strong.",
            "consistency": "Mostly consistent.",
            "evidence usage": "Evidence usage was limited.",
            "reasoning quality": "Reasoning was clear.",
        },
        strongest_moments=["Strong reasoning was identified."],
        weakest_moments=["Limited evidence was identified."],
        coaching_priorities=[
            "Support major claims with concrete evidence."
        ],
    )


def create_analyzer():
    llm = FakeLLMClient()
    prompt_builder = FakePromptBuilder()

    analyzer = AdvancedDebateAnalyzer(
        llm_client=llm,
        prompt_builder=prompt_builder,
    )

    return analyzer, llm, prompt_builder


def test_analyzer_returns_advanced_analysis():
    analyzer, _, _ = create_analyzer()

    analysis = analyzer.analyze(
        create_performance(),
        create_summary(),
    )

    assert isinstance(analysis, AdvancedDebateAnalysis)
    assert (
        analysis.overall_interpretation
        == "The user's reasoning became more developed."
    )


def test_analyzer_maps_all_response_fields():
    analyzer, _, _ = create_analyzer()

    analysis = analyzer.analyze(
        create_performance(),
        create_summary(),
    )

    assert analysis.cross_dimension_patterns == [
        "Reasoning and responsiveness worked together."
    ]

    assert analysis.round_patterns == [
        "Reasoning improved in the later round."
    ]

    assert (
        analysis.strengths_interpretation
        == "The user consistently developed logical responses."
    )

    assert (
        analysis.weaknesses_interpretation
        == "Some claims lacked supporting evidence."
    )

    assert (
        analysis.coaching_interpretation
        == "Support major claims with concrete evidence."
    )

    assert analysis.key_insights == [
        "Reasoning was a recurring strength."
    ]


def test_analyzer_passes_performance_and_summary_to_prompt_builder():
    analyzer, _, prompt_builder = create_analyzer()

    performance = create_performance()
    summary = create_summary()

    analyzer.analyze(performance, summary)

    assert prompt_builder.received_performance is performance
    assert prompt_builder.received_summary is summary


def test_analyzer_passes_prompt_to_llm():
    analyzer, llm, _ = create_analyzer()

    analyzer.analyze(
        create_performance(),
        create_summary(),
    )

    assert llm.received_prompt == (
        "Advanced debate analysis prompt."
    )


def test_analyzer_stores_last_analysis():
    analyzer, _, _ = create_analyzer()

    analysis = analyzer.analyze(
        create_performance(),
        create_summary(),
    )

    assert analyzer.last_analysis is analysis


def test_analyzer_rejects_none_performance():
    analyzer, _, _ = create_analyzer()

    try:
        analyzer.analyze(None, create_summary())
    except ValueError as exc:
        assert str(exc) == "Debate performance cannot be None."
    else:
        raise AssertionError("Expected ValueError.")


def test_analyzer_rejects_none_summary():
    analyzer, _, _ = create_analyzer()

    try:
        analyzer.analyze(create_performance(), None)
    except ValueError as exc:
        assert str(exc) == "Performance summary cannot be None."
    else:
        raise AssertionError("Expected ValueError.")


def test_analyzer_rejects_non_dictionary_response():
    class BadLLM:
        def analyze_advanced_debate_performance(self, prompt):
            return "invalid response"

    analyzer = AdvancedDebateAnalyzer(
        llm_client=BadLLM(),
    )

    try:
        analyzer.analyze(
            create_performance(),
            create_summary(),
        )
    except RuntimeError as exc:
        assert (
            str(exc)
            == "Advanced debate analysis response must be a dictionary."
        )
    else:
        raise AssertionError("Expected RuntimeError.")


def test_analyzer_rejects_missing_response_fields():
    class IncompleteLLM:
        def analyze_advanced_debate_performance(self, prompt):
            return {
                "overall_interpretation": "Some interpretation."
            }

    analyzer = AdvancedDebateAnalyzer(
        llm_client=IncompleteLLM(),
    )

    try:
        analyzer.analyze(
            create_performance(),
            create_summary(),
        )
    except RuntimeError as exc:
        assert "missing fields" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError.")


def test_analyzer_rejects_empty_prompt():
    class EmptyPromptBuilder:
        def __call__(self, performance, summary):
            return "   "

    analyzer = AdvancedDebateAnalyzer(
        llm_client=FakeLLMClient(),
        prompt_builder=EmptyPromptBuilder(),
    )

    try:
        analyzer.analyze(
            create_performance(),
            create_summary(),
        )
    except RuntimeError as exc:
        assert (
            str(exc)
            == "Advanced debate analysis prompt cannot be empty."
        )
    else:
        raise AssertionError("Expected RuntimeError.")