from debate_arena.debate.argument import Argument
from debate_arena.debate.semantic_responsiveness_analyzer import (
    SemanticResponsivenessAnalyzer,
)


class FakeLLMClient:
    def __init__(self):
        self.prompt = None

    def analyze_responsiveness(self, prompt: str) -> dict:
        self.prompt = prompt

        return {
            "responsiveness": "Highly responsive.",
            "addressed_points": [
                "Cost of transportation."
            ],
            "ignored_points": [
                "Environmental impact."
            ],
        }


def create_ai_argument() -> Argument:
    return Argument(
        speaker="ai",
        text=(
            "Public transportation is expensive "
            "and its environmental impact should "
            "also be considered."
        ),
        round=1,
        turn=2,
    )


def create_user_argument() -> Argument:
    return Argument(
        speaker="user",
        text=(
            "Government subsidies could make "
            "public transportation more affordable."
        ),
        round=1,
        turn=3,
    )


def test_analyzer_returns_responsiveness_analysis():
    llm = FakeLLMClient()

    analyzer = SemanticResponsivenessAnalyzer(
        llm_client=llm
    )

    result = analyzer.analyze(
        create_ai_argument(),
        create_user_argument(),
    )

    assert result.responsiveness == (
        "Highly responsive."
    )

    assert result.addressed_points == [
        "Cost of transportation."
    ]

    assert result.ignored_points == [
        "Environmental impact."
    ]


def test_analyzer_calls_gemini():
    llm = FakeLLMClient()

    analyzer = SemanticResponsivenessAnalyzer(
        llm_client=llm
    )

    analyzer.analyze(
        create_ai_argument(),
        create_user_argument(),
    )

    assert llm.prompt is not None

    assert "Public transportation is expensive" in (
        llm.prompt
    )

    assert "Government subsidies" in (
        llm.prompt
    )


def test_analyzer_rejects_missing_ai_argument():
    analyzer = SemanticResponsivenessAnalyzer(
        llm_client=FakeLLMClient()
    )

    try:
        analyzer.analyze(
            None,
            create_user_argument(),
        )
        assert False
    except ValueError as exc:
        assert str(exc) == (
            "Previous AI argument cannot be None."
        )


def test_analyzer_rejects_missing_user_argument():
    analyzer = SemanticResponsivenessAnalyzer(
        llm_client=FakeLLMClient()
    )

    try:
        analyzer.analyze(
            create_ai_argument(),
            None,
        )
        assert False
    except ValueError as exc:
        assert str(exc) == (
            "User argument cannot be None."
        )


def test_analyzer_requires_ai_argument():
    analyzer = SemanticResponsivenessAnalyzer(
        llm_client=FakeLLMClient()
    )

    invalid_ai_argument = Argument(
        speaker="user",
        text="This is not an AI argument.",
        round=1,
        turn=2,
    )

    try:
        analyzer.analyze(
            invalid_ai_argument,
            create_user_argument(),
        )
        assert False
    except ValueError as exc:
        assert str(exc) == (
            "Previous argument must be from the AI."
        )


def test_analyzer_requires_user_argument():
    analyzer = SemanticResponsivenessAnalyzer(
        llm_client=FakeLLMClient()
    )

    invalid_user_argument = Argument(
        speaker="ai",
        text="This is not a user response.",
        round=1,
        turn=3,
    )

    try:
        analyzer.analyze(
            create_ai_argument(),
            invalid_user_argument,
        )
        assert False
    except ValueError as exc:
        assert str(exc) == (
            "User argument must be from the user."
        )


def test_analyzer_uses_default_when_response_is_missing():
    class IncompleteLLMClient:
        def analyze_responsiveness(
            self,
            prompt: str,
        ) -> dict:
            return {}

    analyzer = SemanticResponsivenessAnalyzer(
        llm_client=IncompleteLLMClient()
    )

    result = analyzer.analyze(
        create_ai_argument(),
        create_user_argument(),
    )

    assert result.responsiveness == (
        "Unable to determine responsiveness."
    )

    assert result.addressed_points == []
    assert result.ignored_points == []