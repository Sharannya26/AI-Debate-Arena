from debate_arena.debate.argument import Argument
from debate_arena.debate.debate_analyzer import (
    DebateAnalysis,
    DebateAnalyzer,
)
from debate_arena.debate.state import DebateState


class FakeLLM:
    """Fake LLM used to test full-debate analysis."""

    def __init__(self):
        self.received_debate_data = None

    def analyze_debate(self, debate_data: dict) -> dict:
        self.received_debate_data = debate_data

        return {
            "summary": "The user presented a consistent position.",
            "strongest_argument": (
                "Students can learn responsible social media usage."
            ),
            "weakest_argument": (
                "Social media provides educational opportunities."
            ),
            "strengths": [
                "Consistent position",
                "Clear reasoning",
            ],
            "weaknesses": [
                "Limited evidence",
            ],
            "evidence_usage": (
                "The user relied mainly on reasoning rather than evidence."
            ),
            "consistency": (
                "The user's position remained consistent throughout."
            ),
            "responsiveness": (
                "The user addressed the opposing position."
            ),
            "recommendations": [
                "Use concrete evidence to support major claims.",
            ],
        }


def create_test_state() -> DebateState:
    """Create a sample debate for analysis."""

    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    state.add_user_argument(
        Argument(
            speaker="user",
            text="Social media provides educational opportunities.",
            round=1,
            turn=1,
        )
    )

    state.add_ai_argument(
        Argument(
            speaker="ai",
            text="Those benefits do not eliminate its risks.",
            round=1,
            turn=1,
        )
    )

    state.add_user_argument(
        Argument(
            speaker="user",
            text="Students can learn responsible social media usage.",
            round=2,
            turn=2,
        )
    )

    state.add_ai_argument(
        Argument(
            speaker="ai",
            text="Responsible usage is difficult to maintain.",
            round=2,
            turn=2,
        )
    )

    return state


def test_debate_analyzer_returns_structured_analysis():
    llm = FakeLLM()
    analyzer = DebateAnalyzer(llm_client=llm)

    state = create_test_state()

    analysis = analyzer.analyze(state)

    assert isinstance(analysis, DebateAnalysis)

    assert analysis.summary == (
        "The user presented a consistent position."
    )

    assert analysis.strongest_argument == (
        "Students can learn responsible social media usage."
    )

    assert analysis.weakest_argument == (
        "Social media provides educational opportunities."
    )

    assert analysis.strengths == [
        "Consistent position",
        "Clear reasoning",
    ]

    assert analysis.weaknesses == [
        "Limited evidence",
    ]


def test_debate_analyzer_sends_complete_debate_to_llm():
    llm = FakeLLM()
    analyzer = DebateAnalyzer(llm_client=llm)

    state = create_test_state()

    analyzer.analyze(state)

    assert llm.received_debate_data is not None

    assert (
        llm.received_debate_data["topic"]
        == "Should social media be banned for students?"
    )

    history = llm.received_debate_data["history"]

    assert len(history) == 4

    assert (
        history[0]["text"]
        == "Social media provides educational opportunities."
    )

    assert (
        history[1]["text"]
        == "Those benefits do not eliminate its risks."
    )

    assert (
        history[2]["text"]
        == "Students can learn responsible social media usage."
    )

    assert (
        history[3]["text"]
        == "Responsible usage is difficult to maintain."
    )


def test_debate_analyzer_rejects_none_state():
    llm = FakeLLM()
    analyzer = DebateAnalyzer(llm_client=llm)

    try:
        analyzer.analyze(None)
    except ValueError as exc:
        assert "Debate state cannot be None." in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for None debate state."
        )


def test_debate_analyzer_rejects_empty_debate():
    llm = FakeLLM()
    analyzer = DebateAnalyzer(llm_client=llm)

    state = DebateState(
        topic="Test topic",
        user_position="Against",
        ai_position="For",
    )

    try:
        analyzer.analyze(state)
    except ValueError as exc:
        assert "Cannot analyze a debate with no history." in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for empty debate."
        )