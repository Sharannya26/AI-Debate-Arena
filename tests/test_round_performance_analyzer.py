from unittest.mock import Mock

from debate_arena.debate.argument import Argument
from debate_arena.debate.argument_analyzer import ArgumentAnalysis
from debate_arena.debate.communication_analyzer import (
    CommunicationAnalyzer,
)
from debate_arena.debate.responsiveness_analysis import (
    ResponsivenessAnalysis,
)
from debate_arena.debate.responsiveness_analyzer import (
    ResponsivenessAnalyzer,
)
from debate_arena.debate.round_performance_analyzer import (
    RoundPerformanceAnalyzer,
)
from debate_arena.debate.speaking_pace import SpeakingPace
from debate_arena.debate.speech_sample import SpeechSample


def make_argument_analysis() -> ArgumentAnalysis:
    return ArgumentAnalysis(
        claim="Public transport reduces traffic.",
        reasoning=(
            "Fewer private vehicles means fewer cars on roads."
        ),
        assumptions=[
            "People will use public transport."
        ],
        evidence=["Traffic studies"],
        weaknesses=[],
        argument_type="causal",
    )


def make_communication_metrics():
    metrics = Mock()
    metrics.speaking_pace = SpeakingPace.MODERATE
    return metrics


def make_previous_ai_argument() -> Argument:
    return Argument(
        speaker="ai",
        text=(
            "Public transport is unreliable and expensive."
        ),
        round=1,
        turn=1,
    )


def make_responsiveness_analysis() -> ResponsivenessAnalysis:
    return ResponsivenessAnalysis(
        responsiveness="Highly responsive.",
        addressed_points=[
            "public",
            "transport",
        ],
        ignored_points=[
            "expensive",
        ],
    )


def make_analyzer(
    responsiveness_analyzer=None,
):
    argument_analyzer = Mock()
    argument_analyzer.analyze.return_value = (
        make_argument_analysis()
    )

    communication_analyzer = Mock()
    communication_analyzer.analyze.return_value = (
        make_communication_metrics()
    )

    return RoundPerformanceAnalyzer(
        argument_analyzer=argument_analyzer,
        communication_analyzer=communication_analyzer,
        responsiveness_analyzer=responsiveness_analyzer,
    ), argument_analyzer, communication_analyzer


def test_round_performance_analyzer_combines_analysis():
    analyzer, _, _ = make_analyzer()

    sample = SpeechSample(
        text="Public transport reduces traffic.",
        duration=10.0,
        round=1,
        turn=1,
    )

    result = analyzer.analyze(sample)

    assert result.round == 1

    assert result.argument_quality == (
        "Argument contains a clear claim supported by reasoning."
    )

    assert result.communication_quality == (
        "Speech was delivered at a moderate pace."
    )

    assert result.evidence_usage == (
        "The argument used 1 identified piece(s) of evidence."
    )

    assert result.reasoning_quality == (
        "Reasoning was identified in the argument."
    )

    assert result.responsiveness is None


def test_round_performance_analyzer_calls_argument_analyzer():
    analyzer, argument_analyzer, _ = make_analyzer()

    sample = SpeechSample(
        text="Public transport reduces traffic.",
        duration=10.0,
        round=2,
        turn=1,
    )

    analyzer.analyze(sample)

    argument_analyzer.analyze.assert_called_once_with(
        sample.text
    )


def test_round_performance_analyzer_calls_communication_analyzer():
    analyzer, _, communication_analyzer = make_analyzer()

    sample = SpeechSample(
        text="Public transport reduces traffic.",
        duration=10.0,
        round=2,
        turn=1,
    )

    analyzer.analyze(sample)

    communication_analyzer.analyze.assert_called_once_with(
        sample
    )


def test_round_one_has_no_responsiveness():
    responsiveness_analyzer = Mock()

    analyzer, _, _ = make_analyzer(
        responsiveness_analyzer=responsiveness_analyzer,
    )

    sample = SpeechSample(
        text="Public transport reduces traffic.",
        duration=10.0,
        round=1,
        turn=1,
    )

    result = analyzer.analyze(sample)

    assert result.responsiveness is None
    responsiveness_analyzer.analyze.assert_not_called()


def test_later_round_analyzes_responsiveness():
    responsiveness_analyzer = Mock()

    responsiveness_analyzer.analyze.return_value = (
        make_responsiveness_analysis()
    )

    analyzer, _, _ = make_analyzer(
        responsiveness_analyzer=responsiveness_analyzer,
    )

    sample = SpeechSample(
        text=(
            "Public transport is expensive, "
            "but subsidies can reduce the cost."
        ),
        duration=10.0,
        round=2,
        turn=2,
    )

    previous_ai_argument = make_previous_ai_argument()

    result = analyzer.analyze(
        sample,
        previous_ai_argument=previous_ai_argument,
    )

    assert result.responsiveness == (
        "Highly responsive."
    )

    responsiveness_analyzer.analyze.assert_called_once()

    called_ai_argument = (
        responsiveness_analyzer.analyze.call_args.args[0]
    )

    called_user_argument = (
        responsiveness_analyzer.analyze.call_args.args[1]
    )

    assert called_ai_argument == previous_ai_argument
    assert called_user_argument.speaker == "user"
    assert called_user_argument.text == sample.text
    assert called_user_argument.round == sample.round
    assert called_user_argument.turn == sample.turn


def test_responsiveness_is_not_used_when_previous_ai_argument_is_none():
    responsiveness_analyzer = Mock()

    analyzer, _, _ = make_analyzer(
        responsiveness_analyzer=responsiveness_analyzer,
    )

    sample = SpeechSample(
        text="Public transport reduces traffic.",
        duration=10.0,
        round=2,
        turn=2,
    )

    result = analyzer.analyze(
        sample,
        previous_ai_argument=None,
    )

    assert result.responsiveness is None
    responsiveness_analyzer.analyze.assert_not_called()


def test_none_sample_is_rejected():
    analyzer, _, _ = make_analyzer()

    try:
        analyzer.analyze(None)
        assert False
    except ValueError as exc:
        assert str(exc) == "Speech sample cannot be None."