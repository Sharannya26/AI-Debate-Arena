import json
from unittest.mock import Mock

from debate_arena.debate.strategy import DebateStrategy
from debate_arena.llm.client import LLMClient


def test_generate_debate_response() -> None:
    fake_response = Mock()

    fake_response.text = json.dumps(
        {
            "strategy": "direct_counter",
            "rebuttal": (
                "The educational benefits do not "
                "necessarily outweigh the risks "
                "of unrestricted use."
            ),
        }
    )

    client = LLMClient.__new__(
        LLMClient
    )

    client.model = "test-model"

    client.client = Mock()

    client.client.models.generate_content.return_value = (
        fake_response
    )

    result = client.generate_debate_response(
        "Test debate prompt."
    )

    assert (
        result.strategy
        == DebateStrategy.DIRECT_COUNTER
    )

    assert result.rebuttal == (
        "The educational benefits do not "
        "necessarily outweigh the risks "
        "of unrestricted use."
    )


def test_generate_debate_response_rejects_empty_prompt() -> None:
    client = LLMClient.__new__(
        LLMClient
    )

    try:
        client.generate_debate_response(
            "   "
        )

    except ValueError as exc:
        assert (
            str(exc)
            == "Prompt cannot be empty."
        )

    else:
        raise AssertionError(
            "Expected ValueError for empty prompt."
        )