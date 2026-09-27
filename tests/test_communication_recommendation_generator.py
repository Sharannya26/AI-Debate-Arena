import pytest

from debate_arena.debate.communication_analysis import (
    CommunicationAnalysis,
)
from debate_arena.debate.communication_feedback import (
    CommunicationFeedback,
)
from debate_arena.debate.communication_improvement_target import (
    CommunicationImprovementTarget,
)
from debate_arena.debate.communication_metrics import (
    CommunicationMetrics,
)
from debate_arena.debate.communication_recommendation_generator import (
    CommunicationRecommendationGenerator,
)
from debate_arena.debate.filler_metrics import (
    FillerMetrics,
)
from debate_arena.debate.speaking_pace import (
    SpeakingPace,
)


def build_analysis(
    *,
    words_per_minute: float = 120.0,
    speaking_pace: SpeakingPace = SpeakingPace.MODERATE,
    average_words_per_sentence: float = 12.0,
    filler_rate: float = 0.02,
) -> CommunicationAnalysis:

    word_count = 100

    total_filler_count = int(
        word_count * filler_rate
    )

    communication_metrics = CommunicationMetrics(
        word_count=word_count,
        sentence_count=8,
        duration=50.0,
        words_per_minute=words_per_minute,
        average_words_per_sentence=average_words_per_sentence,
        speaking_pace=speaking_pace,
    )

    filler_metrics = FillerMetrics(
        total_filler_count=total_filler_count,
        filler_counts=(
            {"um": total_filler_count}
            if total_filler_count > 0
            else {}
        ),
        total_word_count=word_count,
        filler_rate=(
            total_filler_count / word_count
        ),
    )

    return CommunicationAnalysis(
        communication_metrics=communication_metrics,
        filler_metrics=filler_metrics,
    )


def build_feedback(
    weaknesses: list[str] | None = None,
) -> CommunicationFeedback:

    return CommunicationFeedback(
        clarity="The argument was generally clear.",
        conciseness="The response was reasonably concise.",
        delivery="The delivery was understandable.",
        strengths=[
            "Clear main claim."
        ],
        weaknesses=(
            weaknesses
            or [
                "Could improve argument delivery."
            ]
        ),
        recommendations=[
            "Use clearer structure."
        ],
    )


def test_generates_filler_word_focus() -> None:
    analysis = build_analysis(
        filler_rate=0.08
    )

    feedback = build_feedback()

    generator = CommunicationRecommendationGenerator()

    result = generator.generate(
        analysis,
        feedback,
    )

    assert result.primary_focus == (
        CommunicationImprovementTarget.FILLER_WORDS
    )

    assert "filler" in (
        result.improvement_goal.lower()
    )

    assert len(result.action_plan) >= 1


def test_generates_fast_speaking_focus() -> None:
    analysis = build_analysis(
        speaking_pace=SpeakingPace.FAST,
        filler_rate=0.0,
    )

    feedback = build_feedback()

    generator = CommunicationRecommendationGenerator()

    result = generator.generate(
        analysis,
        feedback,
    )

    assert result.primary_focus == (
        CommunicationImprovementTarget.SPEAKING_PACE
    )

    assert len(result.action_plan) >= 1


def test_generates_slow_speaking_focus() -> None:
    analysis = build_analysis(
        speaking_pace=SpeakingPace.SLOW,
        filler_rate=0.0,
    )

    feedback = build_feedback()

    generator = CommunicationRecommendationGenerator()

    result = generator.generate(
        analysis,
        feedback,
    )

    assert result.primary_focus == (
        CommunicationImprovementTarget.SPEAKING_PACE
    )


def test_generates_sentence_length_focus() -> None:
    analysis = build_analysis(
        average_words_per_sentence=30.0,
        filler_rate=0.0,
    )

    feedback = build_feedback()

    generator = CommunicationRecommendationGenerator()

    result = generator.generate(
        analysis,
        feedback,
    )

    assert result.primary_focus == (
        CommunicationImprovementTarget.SENTENCE_LENGTH
    )


def test_uses_feedback_as_secondary_signal() -> None:
    analysis = build_analysis(
        filler_rate=0.0,
        average_words_per_sentence=10.0,
    )

    feedback = build_feedback(
        weaknesses=[
            "Argument delivery could be more direct."
        ]
    )

    generator = CommunicationRecommendationGenerator()

    result = generator.generate(
        analysis,
        feedback,
    )

    assert result.primary_focus == (
        CommunicationImprovementTarget.ARGUMENT_DELIVERY
    )

    assert len(result.action_plan) >= 1


def test_uses_feedback_when_objective_metrics_are_normal() -> None:
    analysis = build_analysis(
        filler_rate=0.0,
        speaking_pace=SpeakingPace.MODERATE,
        average_words_per_sentence=10.0,
    )

    feedback = build_feedback(
        weaknesses=[
            "The argument structure could be clearer."
        ]
    )

    generator = CommunicationRecommendationGenerator()

    result = generator.generate(
        analysis,
        feedback,
    )

    assert result.primary_focus == (
        CommunicationImprovementTarget.ARGUMENT_DELIVERY
    )

    assert len(result.action_plan) >= 1


def test_rejects_none_analysis() -> None:
    generator = CommunicationRecommendationGenerator()

    with pytest.raises(
        ValueError,
        match="Communication analysis cannot be None",
    ):
        generator.generate(
            None,
            build_feedback(),
        )


def test_rejects_none_feedback() -> None:
    generator = CommunicationRecommendationGenerator()

    with pytest.raises(
        ValueError,
        match="Communication feedback cannot be None",
    ):
        generator.generate(
            build_analysis(),
            None,
        )


def test_high_filler_rate_adds_extra_action() -> None:
    analysis = build_analysis(
        filler_rate=0.15
    )

    feedback = build_feedback()

    generator = CommunicationRecommendationGenerator()

    result = generator.generate(
        analysis,
        feedback,
    )

    assert result.primary_focus == (
        CommunicationImprovementTarget.FILLER_WORDS
    )

    assert len(result.action_plan) == 4