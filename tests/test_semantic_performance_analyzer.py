from debate_arena.debate.performance_summary import (
    PerformanceSummary,
)
from debate_arena.debate.semantic_performance_analyzer import (
    SemanticPerformanceAnalyzer,
)


class FakeLLMClient:
    def __init__(self):
        self.received_prompt = None

    def analyze_semantic_performance(
        self,
        prompt: str,
    ) -> dict:
        self.received_prompt = prompt

        return {
            "overall_interpretation": (
                "The user's performance became "
                "more structured across the debate."
            ),
            "strengths_interpretation": (
                "Reasoning remained a notable strength."
            ),
            "weaknesses_interpretation": (
                "Evidence usage remained inconsistent."
            ),
            "coaching_interpretation": (
                "Focus on supporting major claims "
                "with concrete evidence."
            ),
            "key_insights": [
                "Reasoning remained strong.",
                "Evidence usage needs attention.",
            ],
        }


def create_summary():
    return PerformanceSummary(
        overall_summary="Performance improved.",
        dimension_summaries={
            "reasoning quality":
                "Reasoning quality remained consistent.",
            "evidence usage":
                "Evidence usage varied across the debate.",
        },
        strongest_moments=[
            "Round 2: Strong reasoning."
        ],
        weakest_moments=[
            "Round 3: Weak evidence usage."
        ],
        coaching_priorities=[
            "Support major claims with evidence."
        ],
    )


def test_semantic_analyzer_returns_analysis():
    fake_llm = FakeLLMClient()

    analyzer = SemanticPerformanceAnalyzer(
        llm_client=fake_llm
    )

    result = analyzer.analyze(
        create_summary()
    )

    assert (
        result.overall_interpretation
        == "The user's performance became "
        "more structured across the debate."
    )

    assert (
        result.strengths_interpretation
        == "Reasoning remained a notable strength."
    )

    assert (
        result.weaknesses_interpretation
        == "Evidence usage remained inconsistent."
    )

    assert (
        result.coaching_interpretation
        == "Focus on supporting major claims "
        "with concrete evidence."
    )

    assert result.key_insights == [
        "Reasoning remained strong.",
        "Evidence usage needs attention.",
    ]


def test_semantic_analyzer_sends_prompt_to_llm():
    fake_llm = FakeLLMClient()

    analyzer = SemanticPerformanceAnalyzer(
        llm_client=fake_llm
    )

    analyzer.analyze(
        create_summary()
    )

    assert fake_llm.received_prompt is not None
    assert "Performance improved." in (
        fake_llm.received_prompt
    )


def test_semantic_analyzer_rejects_none_summary():
    fake_llm = FakeLLMClient()

    analyzer = SemanticPerformanceAnalyzer(
        llm_client=fake_llm
    )

    try:
        analyzer.analyze(None)
    except ValueError as error:
        assert str(error) == (
            "Performance summary cannot be None."
        )
    else:
        raise AssertionError(
            "Expected ValueError."
        )