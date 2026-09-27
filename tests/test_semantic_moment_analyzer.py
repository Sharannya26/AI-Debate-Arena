from debate_arena.debate.moment_analysis import MomentAnalysis
from debate_arena.debate.semantic_moment_analysis import (
    SemanticMomentAnalysis,
)
from debate_arena.debate.semantic_moment_analyzer import (
    SemanticMomentAnalyzer,
)


class FakeLLMClient:
    def __init__(self):
        self.calls = []

    def analyze_moment_analysis(
        self,
        prompt,
    ):
        self.calls.append(prompt)

        return {
            "strongest_interpretation": (
                "The strongest moments showed clear "
                "argument structure."
            ),
            "weakest_interpretation": (
                "The weakest moments showed limited "
                "evidence support."
            ),
            "key_insights": [
                "Argument structure was clearer later."
            ],
        }


def create_moment_analysis():
    return MomentAnalysis(
        strongest_moments=[
            "Round 2: Strong argument quality — Strong argument."
        ],
        weakest_moments=[
            "Round 1: Weak evidence usage — Limited evidence."
        ],
    )


def test_analyzer_returns_semantic_moment_analysis():
    fake_llm = FakeLLMClient()

    analyzer = SemanticMomentAnalyzer(
        llm_client=fake_llm
    )

    result = analyzer.analyze(
        create_moment_analysis()
    )

    assert isinstance(
        result,
        SemanticMomentAnalysis,
    )


def test_analyzer_returns_strongest_interpretation():
    analyzer = SemanticMomentAnalyzer(
        llm_client=FakeLLMClient()
    )

    result = analyzer.analyze(
        create_moment_analysis()
    )

    assert (
        result.strongest_interpretation
        == (
            "The strongest moments showed clear "
            "argument structure."
        )
    )


def test_analyzer_returns_weakest_interpretation():
    analyzer = SemanticMomentAnalyzer(
        llm_client=FakeLLMClient()
    )

    result = analyzer.analyze(
        create_moment_analysis()
    )

    assert (
        result.weakest_interpretation
        == (
            "The weakest moments showed limited "
            "evidence support."
        )
    )


def test_analyzer_returns_key_insights():
    analyzer = SemanticMomentAnalyzer(
        llm_client=FakeLLMClient()
    )

    result = analyzer.analyze(
        create_moment_analysis()
    )

    assert result.key_insights == [
        "Argument structure was clearer later."
    ]


def test_analyzer_sends_prompt_to_llm():
    fake_llm = FakeLLMClient()

    analyzer = SemanticMomentAnalyzer(
        llm_client=fake_llm
    )

    analyzer.analyze(
        create_moment_analysis()
    )

    assert len(fake_llm.calls) == 1

    assert (
        "Strong argument quality"
        in fake_llm.calls[0]
    )


def test_analyzer_rejects_none():
    analyzer = SemanticMomentAnalyzer(
        llm_client=FakeLLMClient()
    )

    try:
        analyzer.analyze(None)
    except ValueError as error:
        assert str(error) == (
            "Moment analysis cannot be None."
        )
    else:
        raise AssertionError(
            "Expected ValueError."
        )