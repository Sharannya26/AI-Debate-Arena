import json

import pytest

from debate_arena.llm.client import LLMClient


class FakeResponse:
    def __init__(self, text: str | None):
        self.text = text


class FakeModels:
    def __init__(self, response: FakeResponse):
        self.response = response
        self.last_call = None

    def generate_content(
        self,
        *,
        model,
        contents,
        config,
    ):
        self.last_call = {
            "model": model,
            "contents": contents,
            "config": config,
        }

        return self.response


class FakeClient:
    def __init__(self, response: FakeResponse):
        self.models = FakeModels(response)


def create_client(response_text: str | None) -> LLMClient:
    client = object.__new__(LLMClient)

    client.model = "test-model"
    client.client = FakeClient(
        FakeResponse(response_text)
    )

    return client


def test_analyze_responsiveness_returns_dict():
    response = {
        "responsiveness": "Highly responsive.",
        "addressed_points": [
            "Cost of transportation."
        ],
        "ignored_points": [
            "Environmental impact."
        ],
    }

    client = create_client(json.dumps(response))

    result = client.analyze_responsiveness(
        "Analyze this response."
    )

    assert result == response


def test_analyze_responsiveness_rejects_empty_prompt():
    client = create_client("{}")

    with pytest.raises(
        ValueError,
        match="Prompt cannot be empty.",
    ):
        client.analyze_responsiveness("   ")


def test_analyze_responsiveness_rejects_empty_response():
    client = create_client(None)

    with pytest.raises(
        RuntimeError,
        match="Gemini returned an empty responsiveness analysis.",
    ):
        client.analyze_responsiveness(
            "Analyze this response."
        )


def test_analyze_responsiveness_rejects_invalid_json():
    client = create_client(
        "This is not valid JSON."
    )

    with pytest.raises(
        RuntimeError,
        match="Gemini returned invalid responsiveness-analysis JSON.",
    ):
        client.analyze_responsiveness(
            "Analyze this response."
        )


def test_analyze_responsiveness_rejects_non_dict_json():
    client = create_client(
        json.dumps(["invalid"])
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "Gemini returned an invalid "
            "responsiveness-analysis structure."
        ),
    ):
        client.analyze_responsiveness(
            "Analyze this response."
        )


def test_analyze_responsiveness_uses_json_configuration():
    response = {
        "responsiveness": "Partially responsive.",
        "addressed_points": ["Cost"],
        "ignored_points": ["Environment"],
    }

    client = create_client(json.dumps(response))

    client.analyze_responsiveness(
        "Analyze this response."
    )

    call = client.client.models.last_call

    assert call["model"] == "test-model"
    assert call["contents"] == "Analyze this response."

    config = call["config"]

    assert config["response_mime_type"] == "application/json"

    schema = config["response_schema"]

    assert schema["type"] == "object"

    assert set(schema["properties"]) == {
        "responsiveness",
        "addressed_points",
        "ignored_points",
    }

    assert schema["required"] == [
        "responsiveness",
        "addressed_points",
        "ignored_points",
    ]