import asyncio
import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

from debate_arena.voice.voice_agent import VoiceAgent


class FakeWebSocket:
    """Minimal websocket double for testing VoiceAgent events."""

    def __init__(self, messages: list[dict]):
        self.messages = [json.dumps(message) for message in messages]
        self.sent_messages: list[dict] = []

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.messages:
            raise StopAsyncIteration

        return self.messages.pop(0)

    async def send(self, message: str) -> None:
        self.sent_messages.append(json.loads(message))


class FakeMonotonicClock:
    """Deterministic clock for testing speech duration."""

    def __init__(self, values: list[float]):
        self.values = values
        self.index = 0

    def __call__(self) -> float:
        if self.index < len(self.values):
            value = self.values[self.index]
            self.index += 1
            return value

        return self.values[-1]


def create_voice_agent() -> VoiceAgent:
    engine = Mock()

    engine.state.is_finished.return_value = False
    engine.is_finished.return_value = False
    engine.is_user_turn.return_value = True

    return VoiceAgent(
        engine=engine,
        api_key="test-api-key",
    )


def test_voice_agent_initializes_speech_duration_state() -> None:
    agent = create_voice_agent()

    assert agent._speech_started_at is None
    assert agent._last_speech_duration == 0.0


def test_speech_started_and_stopped_track_duration() -> None:
    agent = create_voice_agent()

    messages = [
        {
            "type": "input.speech.started",
        },
        {
            "type": "input.speech.stopped",
        },
    ]

    websocket = FakeWebSocket(messages)

    fake_clock = FakeMonotonicClock(
        [
            100.0,
            102.5,
        ]
    )

    fake_time = SimpleNamespace(
        monotonic=fake_clock,
    )

    with patch(
        "debate_arena.voice.voice_agent.time",
        fake_time,
    ):
        asyncio.run(agent._handle_messages(websocket))

    assert agent._speech_started_at is None
    assert agent._last_speech_duration == 2.5

def test_submit_user_argument_records_round_performance():
    from unittest.mock import Mock

    from debate_arena.debate.argument_analyzer import ArgumentAnalysis
    from debate_arena.debate.round_performance import RoundPerformance
    from debate_arena.debate.state import DebateState
    from debate_arena.debate.engine import DebateEngine
    from debate_arena.voice.voice_agent import VoiceAgent


    class FakeLLM:
        def generate_debate_response(self, prompt):
            response = Mock()
            response.strategy = None
            response.rebuttal = "That is an interesting argument."
            return response


    class FakeArgumentAnalyzer:
        def analyze(self, argument):
            return ArgumentAnalysis(
                claim=argument,
                reasoning="Test reasoning.",
                assumptions=[],
                evidence=[],
                weaknesses=[],
                argument_type="general",
            )


    class FakeRoundPerformanceAnalyzer:
        def analyze(self, speech_sample, previous_ai_argument=None):
            assert speech_sample.text == "Social media is useful."
            assert speech_sample.duration == 5.0
            assert speech_sample.round == 1
            assert speech_sample.turn == 1

            return RoundPerformance(
                round=1,
                argument_quality="Good",
                communication_quality="Clear",
                evidence_usage="Limited",
                reasoning_quality="Logical",
                responsiveness=None,
            )


    state = DebateState(
        topic="Should social media be banned?",
        user_position="Against",
        ai_position="For",
    )

    engine = DebateEngine(
        state=state,
        llm=FakeLLM(),
        argument_analyzer=FakeArgumentAnalyzer(),
        round_performance_analyzer=FakeRoundPerformanceAnalyzer(),
    )

    agent = VoiceAgent(
        engine=engine,
        api_key="test-key",
    )

    agent._last_speech_duration = 5.0

    result = agent._submit_user_argument(
        {"argument": "Social media is useful."}
    )

    assert result["status"] == "success"
    assert len(engine.round_performances) == 1
    assert engine.round_performances[0].round == 1
    assert engine.round_performances[0].argument_quality == "Good"