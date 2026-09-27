import json

from debate_arena.llm.client import LLMClient


class FakeResponse:
    def __init__(self, text):
        self.text = text


class FakeModels:
    def __init__(self):
        self.calls = []

    def generate_content(
        self,
        *,
        model,
        contents,
        config,
    ):
        self.calls.append(
            {
                "model": model,
                "contents": contents,
                "config": config,
            }
        )

        return FakeResponse(
            json.dumps(
                {
                    "strongest_interpretation": (
                        "The strongest moments showed clear "
                        "argument structure."
                    ),
                    "weakest_interpretation": (
                        "The weakest moments showed areas "
                        "where additional support could help."
                    ),
                    "key_insights": [
                        "Later rounds contained clearer argument structure."
                    ],
                }
            )
        )


class FakeGeminiClient:
    def __init__(self):
        self.models = FakeModels()


def create_client():
    client = LLMClient.__new__(LLMClient)

    client.client = FakeGeminiClient()
    client.model = "fake-model"

    return client


def test_analyze_moment_analysis_returns_dict():
    client = create_client()

    result = client.analyze_moment_analysis(
        "test prompt"
    )

    assert isinstance(result, dict)


def test_analyze_moment_analysis_returns_expected_fields():
    client = create_client()

    result = client.analyze_moment_analysis(
        "test prompt"
    )

    assert result["strongest_interpretation"]
    assert result["weakest_interpretation"]
    assert result["key_insights"]


def test_analyze_moment_analysis_uses_configured_model():
    client = create_client()

    client.analyze_moment_analysis(
        "test prompt"
    )

    call = client.client.models.calls[0]

    assert call["model"] == "fake-model"


def test_analyze_moment_analysis_passes_prompt():
    client = create_client()

    prompt = "Analyze these debate moments."

    client.analyze_moment_analysis(prompt)

    call = client.client.models.calls[0]

    assert call["contents"] == prompt


def test_analyze_moment_analysis_requests_json():
    client = create_client()

    client.analyze_moment_analysis(
        "test prompt"
    )

    call = client.client.models.calls[0]

    assert call["config"] == {
        "response_mime_type": "application/json"
    }


def test_analyze_moment_analysis_parses_json():
    client = create_client()

    result = client.analyze_moment_analysis(
        "test prompt"
    )

    assert result == {
        "strongest_interpretation": (
            "The strongest moments showed clear "
            "argument structure."
        ),
        "weakest_interpretation": (
            "The weakest moments showed areas "
            "where additional support could help."
        ),
        "key_insights": [
            "Later rounds contained clearer argument structure."
        ],
    }