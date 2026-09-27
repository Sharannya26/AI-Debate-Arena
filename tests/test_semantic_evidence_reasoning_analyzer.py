import pytest

from debate_arena.debate.argument import Argument
from debate_arena.debate.semantic_evidence_reasoning_analyzer import (
    SemanticEvidenceReasoningAnalyzer,
)


class FakeLLMClient:
    def __init__(self, response):
        self.response = response
        self.last_prompt = None

    def analyze_evidence_reasoning(self, prompt):
        self.last_prompt = prompt
        return self.response


def create_user_argument(
    text: str,
    round_number: int,
) -> Argument:
    return Argument(
        speaker="user",
        text=text,
        round=round_number,
        turn="user",
    )


def test_semantic_analyzer_returns_structured_analysis():
    fake_llm = FakeLLMClient(
        {
            "evidence_quality": "Strong evidence usage.",
            "reasoning_quality": "Moderate reasoning structure.",
            "evidence_points": [
                "Round 1 contains a research-based claim."
            ],
            "missing_evidence": [
                "Round 2 contains an unsupported general claim."
            ],
            "reasoning_points": [
                "Round 2 explains a cause-and-effect relationship."
            ],
            "reasoning_gaps": [
                "Round 3 does not clearly connect its claim to a conclusion."
            ],
        }
    )

    analyzer = SemanticEvidenceReasoningAnalyzer(
        llm_client=fake_llm
    )

    arguments = [
        create_user_argument(
            "According to research, online education helps students.",
            1,
        ),
        create_user_argument(
            "Online education provides flexibility because students "
            "can learn remotely.",
            2,
        ),
        create_user_argument(
            "Students need access to education.",
            3,
        ),
    ]

    result = analyzer.analyze(arguments)

    assert result.evidence_quality == "Strong evidence usage."
    assert result.reasoning_quality == "Moderate reasoning structure."

    assert result.evidence_points == [
        "Round 1 contains a research-based claim."
    ]

    assert result.missing_evidence == [
        "Round 2 contains an unsupported general claim."
    ]

    assert result.reasoning_points == [
        "Round 2 explains a cause-and-effect relationship."
    ]

    assert result.reasoning_gaps == [
        "Round 3 does not clearly connect its claim to a conclusion."
    ]


def test_semantic_analyzer_sends_user_arguments_to_llm():
    fake_llm = FakeLLMClient(
        {
            "evidence_quality": "Limited evidence usage.",
            "reasoning_quality": "Strong reasoning structure.",
            "evidence_points": [],
            "missing_evidence": [],
            "reasoning_points": [],
            "reasoning_gaps": [],
        }
    )

    analyzer = SemanticEvidenceReasoningAnalyzer(
        llm_client=fake_llm
    )

    arguments = [
        create_user_argument(
            "Research shows that exercise improves health.",
            1,
        ),
        create_user_argument(
            "Exercise improves health because it strengthens "
            "the cardiovascular system.",
            2,
        ),
    ]

    analyzer.analyze(arguments)

    assert fake_llm.last_prompt is not None
    assert (
        "Research shows that exercise improves health."
        in fake_llm.last_prompt
    )
    assert (
        "Exercise improves health because it strengthens "
        "the cardiovascular system."
        in fake_llm.last_prompt
    )


def test_semantic_analyzer_rejects_none_arguments():
    fake_llm = FakeLLMClient({})

    analyzer = SemanticEvidenceReasoningAnalyzer(
        llm_client=fake_llm
    )

    with pytest.raises(ValueError, match="cannot be None"):
        analyzer.analyze(None)


def test_semantic_analyzer_rejects_empty_arguments():
    fake_llm = FakeLLMClient({})

    analyzer = SemanticEvidenceReasoningAnalyzer(
        llm_client=fake_llm
    )

    with pytest.raises(
        ValueError,
        match="At least one user argument is required",
    ):
        analyzer.analyze([])


def test_semantic_analyzer_rejects_none_argument_inside_list():
    fake_llm = FakeLLMClient({})

    analyzer = SemanticEvidenceReasoningAnalyzer(
        llm_client=fake_llm
    )

    arguments = [
        create_user_argument(
            "Education is important.",
            1,
        ),
        None,
    ]

    with pytest.raises(
        ValueError,
        match="cannot contain None",
    ):
        analyzer.analyze(arguments)


def test_semantic_analyzer_rejects_non_user_argument():
    fake_llm = FakeLLMClient({})

    analyzer = SemanticEvidenceReasoningAnalyzer(
        llm_client=fake_llm
    )

    arguments = [
        Argument(
            speaker="ai",
            text="Education is important.",
            round=1,
            turn="ai",
        )
    ]

    with pytest.raises(
        ValueError,
        match="All arguments must be from the user",
    ):
        analyzer.analyze(arguments)