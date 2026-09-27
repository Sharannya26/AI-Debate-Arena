import json
from unittest.mock import Mock

import pytest

from debate_arena.llm.client import LLMClient


def create_client(
    response_data: dict,
) -> LLMClient:
    fake_response = Mock()

    fake_response.text = json.dumps(
        response_data
    )

    client = LLMClient.__new__(
        LLMClient
    )

    client.model = "test-model"
    client.client = Mock()

    client.client.models.generate_content.return_value = (
        fake_response
    )

    return client


def test_analyze_communication() -> None:
    client = create_client(
        {
            "clarity": (
                "The speaker communicates the main "
                "ideas clearly."
            ),
            "conciseness": (
                "The response is reasonably concise."
            ),
            "delivery": (
                "The speaking pace is moderate "
                "with occasional filler words."
            ),
            "strengths": [
                "Clear ideas",
                "Good structure",
            ],
            "weaknesses": [
                "Occasional filler words",
            ],
            "recommendations": [
                "Use deliberate pauses",
                "Reduce filler words",
            ],
        }
    )

    result = client.analyze_communication(
        "Test communication prompt."
    )

    assert result["clarity"] == (
        "The speaker communicates the main "
        "ideas clearly."
    )

    assert result["conciseness"] == (
        "The response is reasonably concise."
    )

    assert result["delivery"] == (
        "The speaking pace is moderate "
        "with occasional filler words."
    )

    assert result["strengths"] == [
        "Clear ideas",
        "Good structure",
    ]

    assert result["weaknesses"] == [
        "Occasional filler words",
    ]

    assert result["recommendations"] == [
        "Use deliberate pauses",
        "Reduce filler words",
    ]


def test_analyze_communication_rejects_empty_prompt() -> None:
    client = LLMClient.__new__(
        LLMClient
    )

    with pytest.raises(
        ValueError,
        match="Prompt cannot be empty",
    ):
        client.analyze_communication(
            "   "
        )


def test_analyze_communication_rejects_empty_response() -> None:
    fake_response = Mock()
    fake_response.text = ""

    client = LLMClient.__new__(
        LLMClient
    )

    client.model = "test-model"
    client.client = Mock()

    client.client.models.generate_content.return_value = (
        fake_response
    )

    with pytest.raises(
        RuntimeError,
        match="Gemini returned an empty communication analysis",
    ):
        client.analyze_communication(
            "Test communication prompt."
        )


def test_analyze_communication_rejects_invalid_json() -> None:
    fake_response = Mock()
    fake_response.text = "not valid json"

    client = LLMClient.__new__(
        LLMClient
    )

    client.model = "test-model"
    client.client = Mock()

    client.client.models.generate_content.return_value = (
        fake_response
    )

    with pytest.raises(
        RuntimeError,
        match="invalid communication-analysis JSON",
    ):
        client.analyze_communication(
            "Test communication prompt."
        )


def test_analyze_communication_rejects_non_dictionary_response() -> None:
    fake_response = Mock()

    fake_response.text = json.dumps(
        [
            "invalid",
            "structure",
        ]
    )

    client = LLMClient.__new__(
        LLMClient
    )

    client.model = "test-model"
    client.client = Mock()

    client.client.models.generate_content.return_value = (
        fake_response
    )

    with pytest.raises(
        RuntimeError,
        match="invalid communication-analysis structure",
    ):
        client.analyze_communication(
            "Test communication prompt."
        )