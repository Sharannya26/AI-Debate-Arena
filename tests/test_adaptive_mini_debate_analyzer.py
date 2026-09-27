import pytest

from debate_arena.debate.adaptive_mini_debate import (
    AdaptiveMiniDebate,
)
from debate_arena.debate.adaptive_mini_debate_analyzer import (
    AdaptiveMiniDebateAnalyzer,
)
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)


def make_priority(
    focus_area: str = "Improve evidence usage",
) -> PersonalizedImprovementPriority:
    return PersonalizedImprovementPriority(
        priority="Improve evidence usage",
        reason="Evidence usage declined across the debate.",
        focus_area=focus_area,
        supporting_evidence=[
            "Round 1: strong evidence usage.",
            "Round 2: weaker evidence usage.",
        ],
    )


def test_analyzer_returns_adaptive_mini_debate():
    analyzer = AdaptiveMiniDebateAnalyzer()

    result = analyzer.analyze(
        priority=make_priority(),
        topic="Should college education be free?",
    )

    assert isinstance(
        result,
        AdaptiveMiniDebate,
    )


def test_analyzer_preserves_topic():
    analyzer = AdaptiveMiniDebateAnalyzer()

    result = analyzer.analyze(
        priority=make_priority(),
        topic="Should college education be free?",
    )

    assert (
        result.topic
        == "Should college education be free?"
    )


def test_analyzer_preserves_focus_area():
    analyzer = AdaptiveMiniDebateAnalyzer()

    result = analyzer.analyze(
        priority=make_priority(
            "Improve evidence usage"
        ),
        topic="Should college education be free?",
    )

    assert (
        result.focus_area
        == "Improve evidence usage"
    )


def test_evidence_usage_generates_evidence_prompt():
    analyzer = AdaptiveMiniDebateAnalyzer()

    result = analyzer.analyze(
        priority=make_priority(
            "Improve evidence usage"
        ),
        topic="Should college education be free?",
    )

    assert "claim" in result.user_prompt.lower()
    assert "evidence" in result.user_prompt.lower()
    assert (
        "evidence" in result.ai_prompt.lower()
    )


@pytest.mark.parametrize(
    "focus_area",
    [
        "Improve argument quality",
        "Improve communication quality",
        "Improve evidence usage",
        "Improve reasoning quality",
        "Improve responsiveness",
    ],
)
def test_analyzer_supports_known_focus_areas(
    focus_area,
):
    analyzer = AdaptiveMiniDebateAnalyzer()

    result = analyzer.analyze(
        priority=make_priority(focus_area),
        topic="Practice debate",
    )

    assert isinstance(
        result,
        AdaptiveMiniDebate,
    )

    assert result.user_prompt
    assert result.ai_prompt


def test_analyzer_can_extract_dimension_from_priority():
    analyzer = AdaptiveMiniDebateAnalyzer()

    priority = PersonalizedImprovementPriority(
        priority="Improve reasoning quality",
        reason="Reasoning needs improvement.",
        focus_area="General debate performance",
    )

    result = analyzer.analyze(
        priority=priority,
        topic="Practice debate",
    )

    assert (
        "reasoning" in result.user_prompt.lower()
        or "evidence" in result.user_prompt.lower()
    )


def test_analyzer_has_fallback_for_unknown_focus_area():
    analyzer = AdaptiveMiniDebateAnalyzer()

    priority = PersonalizedImprovementPriority(
        priority="Improve strategic thinking",
        reason="Strategic thinking needs improvement.",
        focus_area="Strategic thinking",
    )

    result = analyzer.analyze(
        priority=priority,
        topic="Practice debate",
    )

    assert isinstance(
        result,
        AdaptiveMiniDebate,
    )

    assert result.user_prompt
    assert result.ai_prompt


def test_analyzer_rejects_none_priority():
    analyzer = AdaptiveMiniDebateAnalyzer()

    with pytest.raises(
        ValueError,
        match="Improvement priority cannot be None.",
    ):
        analyzer.analyze(
            priority=None,
            topic="Practice debate",
        )


def test_analyzer_rejects_empty_topic():
    analyzer = AdaptiveMiniDebateAnalyzer()

    with pytest.raises(
        ValueError,
        match="Mini-debate topic cannot be empty.",
    ):
        analyzer.analyze(
            priority=make_priority(),
            topic="",
        )


def test_analyzer_strips_topic_whitespace():
    analyzer = AdaptiveMiniDebateAnalyzer()

    result = analyzer.analyze(
        priority=make_priority(),
        topic="  Practice debate  ",
    )

    assert result.topic == "Practice debate"


def test_analyzer_initializes_user_turn():
    analyzer = AdaptiveMiniDebateAnalyzer()

    result = analyzer.analyze(
        priority=make_priority(),
        topic="Practice debate",
    )

    assert result.current_turn == "user"
    assert result.round_number == 1
    assert result.max_rounds == 2