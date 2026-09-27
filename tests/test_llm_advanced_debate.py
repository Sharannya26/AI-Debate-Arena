import json

import pytest

from debate_arena.llm.client import LLMClient


class FakeResponse:
    def __init__(self, text: str):
        self.text = text


class FakeModels:
    def __init__(self):
        self.last_call = None

    def generate_content(self, **kwargs):
        self.last_call = kwargs

        return FakeResponse(
            json.dumps(
                {
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
            )
        )


class FakeGeminiClient:
    def __init__(self):
        self.models = FakeModels()


def create_client():
    client = LLMClient.__new__(LLMClient)

    fake_client = FakeGeminiClient()

    client.client = fake_client
    client.model = "test-model"

    return client


def test_analyze_advanced_debate_performance_returns_dict():
    client = create_client()

    result = client.analyze_advanced_debate_performance(
        "Analyze this debate performance."
    )

    assert isinstance(result, dict)
    assert (
        result["overall_interpretation"]
        == "The user's reasoning became more developed."
    )


def test_analyze_advanced_debate_performance_returns_expected_fields():
    client = create_client()

    result = client.analyze_advanced_debate_performance(
        "Analyze this debate performance."
    )

    assert "overall_interpretation" in result
    assert "cross_dimension_patterns" in result
    assert "round_patterns" in result
    assert "strengths_interpretation" in result
    assert "weaknesses_interpretation" in result
    assert "coaching_interpretation" in result
    assert "key_insights" in result


def test_analyze_advanced_debate_performance_uses_json_response():
    client = create_client()

    client.analyze_advanced_debate_performance(
        "Analyze this debate performance."
    )

    call = client.client.models.last_call

    assert call["config"]["response_mime_type"] == "application/json"


def test_analyze_advanced_debate_performance_uses_configured_model():
    client = create_client()

    client.analyze_advanced_debate_performance(
        "Analyze this debate performance."
    )

    call = client.client.models.last_call

    assert call["model"] == "test-model"


def test_analyze_advanced_debate_performance_rejects_empty_prompt():
    client = create_client()

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        client.analyze_advanced_debate_performance("   ")