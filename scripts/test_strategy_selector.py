from debate_arena.debate.argument_analyzer import ArgumentAnalysis
from debate_arena.debate.strategy import DebateStrategy
from debate_arena.debate.strategy_selector import StrategySelector


class FakeLLM:
    """Fake LLM used for testing strategy selection."""

    def __init__(self, response: str):
        self.response = response
        self.last_prompt = None

    def generate_response(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self.response


def test_strategy_selector_returns_strategy() -> None:
    llm = FakeLLM("alternative_solution")

    selector = StrategySelector(llm=llm)

    strategy = selector.select(
        context="Debate context",
        latest_argument="Latest user argument",
    )

    assert strategy == DebateStrategy.ALTERNATIVE_SOLUTION


def test_strategy_selector_uses_structured_argument_analysis() -> None:
    llm = FakeLLM("assumption_challenge")

    selector = StrategySelector(llm=llm)

    analysis = ArgumentAnalysis(
        claim="Students can use social media responsibly.",
        reasoning="Education can teach responsible usage.",
        assumptions=[
            "Students will follow responsible usage guidelines."
        ],
        evidence=[
            "No specific evidence was provided."
        ],
        weaknesses=[
            "The argument does not address misuse."
        ],
        argument_type="prescriptive",
    )

    strategy = selector.select(
        context="Debate about whether social media should be banned.",
        latest_argument=(
            "Social media should not be banned because "
            "students can use it for education."
        ),
        analysis=analysis,
    )

    assert strategy == DebateStrategy.ASSUMPTION_CHALLENGE

    assert llm.last_prompt is not None

    assert "Students can use social media responsibly." in llm.last_prompt
    assert "Education can teach responsible usage." in llm.last_prompt
    assert (
        "Students will follow responsible usage guidelines."
        in llm.last_prompt
    )
    assert (
        "The argument does not address misuse."
        in llm.last_prompt
    )
    assert "prescriptive" in llm.last_prompt


def test_strategy_selector_rejects_invalid_strategy() -> None:
    llm = FakeLLM("not_a_real_strategy")

    selector = StrategySelector(llm=llm)

    try:
        selector.select(
            context="Debate context",
            latest_argument="Latest user argument",
        )
    except RuntimeError as exc:
        assert "invalid debate strategy" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError")


def test_strategy_selector_rejects_empty_argument() -> None:
    llm = FakeLLM("alternative_solution")

    selector = StrategySelector(llm=llm)

    try:
        selector.select(
            context="Debate context",
            latest_argument="",
        )
    except ValueError as exc:
        assert "Latest argument cannot be empty." in str(exc)
    else:
        raise AssertionError("Expected ValueError")