from unittest.mock import Mock

import pytest

from debate_arena.debate.argument_analyzer import (
    ArgumentAnalysis,
    ArgumentAnalyzer,
)


@pytest.fixture
def mock_llm():
    client = Mock()

    client.analyze_argument.return_value = {
        "claim": "A complete ban is excessive.",
        "reasoning": (
            "Students can learn responsible social media usage."
        ),
        "assumptions": [
            "Students can successfully learn responsible usage."
        ],
        "evidence": [],
        "weaknesses": [
            (
                "The argument does not address "
                "enforcement challenges."
            )
        ],
        "argument_type": "prescriptive",
    }

    return client


@pytest.fixture
def analyzer(mock_llm):
    return ArgumentAnalyzer(llm_client=mock_llm)


def test_analyzer_returns_argument_analysis(analyzer):
    result = analyzer.analyze(
        "A complete ban is excessive because students "
        "can learn responsible social media usage."
    )

    assert isinstance(result, ArgumentAnalysis)


def test_analyzer_uses_llm_client(analyzer, mock_llm):
    argument = (
        "Schools should teach responsible social media usage."
    )

    analyzer.analyze(argument)

    mock_llm.analyze_argument.assert_called_once_with(argument)


def test_analyzer_returns_claim(analyzer):
    result = analyzer.analyze(
        "A complete ban is excessive."
    )

    assert result.claim
    assert isinstance(result.claim, str)


def test_analyzer_returns_reasoning(analyzer):
    result = analyzer.analyze(
        "A complete ban is excessive."
    )

    assert result.reasoning
    assert isinstance(result.reasoning, str)


def test_analyzer_returns_assumptions(analyzer):
    result = analyzer.analyze(
        "A complete ban is excessive."
    )

    assert isinstance(result.assumptions, list)


def test_analyzer_returns_evidence(analyzer):
    result = analyzer.analyze(
        "Studies show that social media improves communication."
    )

    assert isinstance(result.evidence, list)


def test_analyzer_returns_weaknesses(analyzer):
    result = analyzer.analyze(
        "A complete ban is excessive."
    )

    assert isinstance(result.weaknesses, list)


def test_analyzer_returns_argument_type(analyzer):
    result = analyzer.analyze(
        "Schools should teach responsible social media usage."
    )

    assert result.argument_type == "prescriptive"


def test_analyzer_rejects_empty_argument(analyzer):
    with pytest.raises(ValueError):
        analyzer.analyze("")


def test_analyzer_rejects_whitespace_argument(analyzer):
    with pytest.raises(ValueError):
        analyzer.analyze("   ")