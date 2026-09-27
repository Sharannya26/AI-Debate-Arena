import json

import pytest

from debate_arena.llm.client import LLMClient


class FakeResponse:
    def __init__(self, data: dict):
        self.text = json.dumps(data)


class FakeModels:
    def __init__(self, response_data: dict):
        self.response_data = response_data
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return FakeResponse(self.response_data)


class FakeGeminiClient:
    def __init__(self, response_data: dict):
        self.models = FakeModels(response_data)


def make_response_data() -> dict:
    return {
        "overall_interpretation": (
            "Performance improved across the later rounds."
        ),
        "improvement_interpretation": (
            "Reasoning became stronger across the debate."
        ),
        "decline_interpretation": (
            "Communication became less consistent in later rounds."
        ),
        "stability_interpretation": (
            "Responsiveness remained stable."
        ),
        "recurring_interpretation": (
            "Limited evidence usage appeared repeatedly."
        ),
        "cross_dimension_interpretation": (
            "Reasoning improved while evidence usage remained limited."
        ),
        "key_insights": [
            "Later rounds showed stronger reasoning."
        ],
    }


def make_llm_client():
    fake_client = FakeGeminiClient(make_response_data())

    llm = LLMClient.__new__(LLMClient)
    llm.client = fake_client
    llm.model = "fake-model"

    return llm, fake_client


def test_cross_round_analysis_rejects_empty_prompt():
    llm, _ = make_llm_client()

    with pytest.raises(ValueError):
        llm.analyze_cross_round_performance("")


def test_cross_round_analysis_rejects_whitespace_prompt():
    llm, _ = make_llm_client()

    with pytest.raises(ValueError):
        llm.analyze_cross_round_performance("   ")


def test_cross_round_analysis_returns_dictionary():
    llm, _ = make_llm_client()

    result = llm.analyze_cross_round_performance(
        "Analyze the supplied cross-round findings."
    )

    assert isinstance(result, dict)


def test_cross_round_analysis_returns_expected_fields():
    llm, _ = make_llm_client()

    result = llm.analyze_cross_round_performance(
        "Analyze the supplied cross-round findings."
    )

    assert result["overall_interpretation"] == (
        "Performance improved across the later rounds."
    )
    assert result["improvement_interpretation"] == (
        "Reasoning became stronger across the debate."
    )
    assert result["decline_interpretation"] == (
        "Communication became less consistent in later rounds."
    )
    assert result["stability_interpretation"] == (
        "Responsiveness remained stable."
    )
    assert result["recurring_interpretation"] == (
        "Limited evidence usage appeared repeatedly."
    )
    assert result["cross_dimension_interpretation"] == (
        "Reasoning improved while evidence usage remained limited."
    )
    assert result["key_insights"] == [
        "Later rounds showed stronger reasoning."
    ]


def test_cross_round_analysis_sends_prompt_to_gemini():
    llm, fake_client = make_llm_client()

    prompt = "Analyze these cross-round findings."

    llm.analyze_cross_round_performance(prompt)

    assert len(fake_client.models.calls) == 1
    assert fake_client.models.calls[0]["contents"] == prompt


def test_cross_round_analysis_uses_configured_model():
    llm, fake_client = make_llm_client()

    llm.analyze_cross_round_performance(
        "Analyze these cross-round findings."
    )

    assert fake_client.models.calls[0]["model"] == "fake-model"


def test_cross_round_analysis_requests_json_response():
    llm, fake_client = make_llm_client()

    llm.analyze_cross_round_performance(
        "Analyze these cross-round findings."
    )

    assert fake_client.models.calls[0]["config"] == {
        "response_mime_type": "application/json"
    }


def test_cross_round_analysis_does_not_make_multiple_calls():
    llm, fake_client = make_llm_client()

    llm.analyze_cross_round_performance(
        "Analyze these cross-round findings."
    )

    assert len(fake_client.models.calls) == 1