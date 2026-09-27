from unittest.mock import Mock

import pytest

from debate_arena.debate.communication_analysis import (
    CommunicationAnalysis,
)
from debate_arena.debate.communication_feedback import (
    CommunicationFeedback,
)
from debate_arena.debate.communication_gemini_analyzer import (
    CommunicationGeminiAnalyzer,
)
from debate_arena.debate.communication_metrics import (
    CommunicationMetrics,
)
from debate_arena.debate.filler_metrics import (
    FillerMetrics,
)
from debate_arena.debate.speaking_pace import (
    SpeakingPace,
)


def create_analysis() -> CommunicationAnalysis:
    communication_metrics = CommunicationMetrics(
        word_count=20,
        sentence_count=3,
        duration=10.0,
        words_per_minute=120.0,
        average_words_per_sentence=20 / 3,
        speaking_pace=SpeakingPace.MODERATE,
    )

    filler_metrics = FillerMetrics(
        total_filler_count=2,
        filler_counts={
            "um": 1,
            "like": 1,
        },
        total_word_count=20,
        filler_rate=0.1,
    )

    return CommunicationAnalysis(
        communication_metrics=communication_metrics,
        filler_metrics=filler_metrics,
    )


def create_llm(
    response: dict,
) -> Mock:
    llm = Mock()

    llm.analyze_communication.return_value = (
        response
    )

    return llm


def test_analyze_returns_communication_feedback() -> None:
    response = {
        "clarity": (
            "The speaker communicates the main ideas clearly."
        ),
        "conciseness": (
            "The response is reasonably concise."
        ),
        "delivery": (
            "The speaking pace is moderate with some filler words."
        ),
        "strengths": [
            "Clear ideas",
            "Good structure",
        ],
        "weaknesses": [
            "Occasional filler words",
        ],
        "recommendations": [
            "Reduce filler words",
            "Use deliberate pauses",
        ],
    }

    llm = create_llm(response)

    analyzer = CommunicationGeminiAnalyzer(
        llm=llm
    )

    result = analyzer.analyze(
        create_analysis()
    )

    assert isinstance(
        result,
        CommunicationFeedback,
    )

    assert result.clarity == (
        "The speaker communicates the main ideas clearly."
    )

    assert result.conciseness == (
        "The response is reasonably concise."
    )

    assert result.delivery == (
        "The speaking pace is moderate with some filler words."
    )

    assert result.strengths == [
        "Clear ideas",
        "Good structure",
    ]

    assert result.weaknesses == [
        "Occasional filler words",
    ]

    assert result.recommendations == [
        "Reduce filler words",
        "Use deliberate pauses",
    ]


def test_analyze_sends_prompt_to_llm() -> None:
    response = {
        "clarity": "Clear.",
        "conciseness": "Concise.",
        "delivery": "Moderate.",
        "strengths": [
            "Clear ideas",
        ],
        "weaknesses": [
            "Some fillers",
        ],
        "recommendations": [
            "Pause more",
        ],
    }

    llm = create_llm(response)

    analyzer = CommunicationGeminiAnalyzer(
        llm=llm
    )

    analyzer.analyze(
        create_analysis()
    )

    llm.analyze_communication.assert_called_once()

    prompt = (
        llm.analyze_communication.call_args.args[0]
    )

    assert "Word count: 20" in prompt
    assert "Sentence count: 3" in prompt
    assert "Duration: 10.0 seconds" in prompt
    assert "Words per minute: 120.0" in prompt
    assert "Speaking pace: moderate" in prompt
    assert "Total filler count: 2" in prompt
    assert "Filler rate: 0.1" in prompt


def test_analyze_rejects_none_analysis() -> None:
    llm = Mock()

    analyzer = CommunicationGeminiAnalyzer(
        llm=llm
    )

    with pytest.raises(
        ValueError,
        match="Communication analysis cannot be None",
    ):
        analyzer.analyze(None)


def test_analyze_rejects_non_dictionary_response() -> None:
    llm = Mock()

    llm.analyze_communication.return_value = (
        "invalid response"
    )

    analyzer = CommunicationGeminiAnalyzer(
        llm=llm
    )

    with pytest.raises(
        ValueError,
        match="must be a dictionary",
    ):
        analyzer.analyze(
            create_analysis()
        )


def test_analyze_rejects_missing_required_fields() -> None:
    llm = Mock()

    llm.analyze_communication.return_value = {
        "clarity": "Clear.",
        "conciseness": "Concise.",
    }

    analyzer = CommunicationGeminiAnalyzer(
        llm=llm
    )

    with pytest.raises(
        ValueError,
        match="missing required fields",
    ):
        analyzer.analyze(
            create_analysis()
        )


def test_build_analysis_data() -> None:
    analysis = create_analysis()

    result = (
        CommunicationGeminiAnalyzer._build_analysis_data(
            analysis
        )
    )

    assert result == {
        "word_count": 20,
        "sentence_count": 3,
        "duration": 10.0,
        "words_per_minute": 120.0,
        "speaking_pace": "moderate",
        "average_words_per_sentence": 20 / 3,
        "total_filler_count": 2,
        "filler_counts": {
            "um": 1,
            "like": 1,
        },
        "filler_rate": 0.1,
    }