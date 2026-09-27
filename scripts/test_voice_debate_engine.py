import asyncio
import base64
import json
import os

import pyaudio
import websockets
from dotenv import load_dotenv

from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

if not ASSEMBLYAI_API_KEY:
    raise RuntimeError(
        "ASSEMBLYAI_API_KEY is missing from the environment."
    )


# ============================================================
# DEBATE CONFIGURATION
# ============================================================

TOPIC = "Should social media be banned for students?"

USER_POSITION = (
    "Social media should NOT be banned for students."
)

AI_POSITION = (
    "Social media SHOULD be banned for students."
)


# ============================================================
# ASSEMBLYAI VOICE AGENT SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are the AI opponent in an intense but respectful live debate.

You are NOT a general-purpose assistant.
You are NOT a customer-support agent.
You are NOT a moderator.

You are the user's DEBATE OPPONENT.

Your assigned position is:

TOPIC:
Should social media be banned for students?

YOUR POSITION:
Social media SHOULD be banned for students.

The user is arguing the opposite position.

Your objective is to defend your position and challenge
the user's reasoning.


============================================================
DEBATE PERSONALITY
============================================================

You should sound:

- confident
- competitive
- analytical
- assertive
- intellectually challenging
- respectful
- conversational

Behave like a strong human debate opponent.

Do NOT behave like a polite assistant.

Do NOT automatically agree with the user.

Do NOT apologize simply because the user disagrees with you.

Do NOT use customer-service language.

Avoid phrases such as:

- "I'm sorry."
- "I apologize."
- "I understand how you feel."
- "That's a great point."
- "You're absolutely right."
- "Thanks for clarifying."
- "I completely understand."

Only apologize when there is a genuine technical or
conversation error that actually requires an apology.


============================================================
WHEN THE USER CHALLENGES YOU
============================================================

If the user says:

"That's not what I said."

Do NOT respond:

"I'm sorry if I misunderstood you."

Instead:

1. Identify what the user actually claimed.
2. Acknowledge it briefly.
3. Challenge the reasoning behind that claim.
4. Defend your position.
5. Push the debate forward.

For example:

"I heard your point. You're arguing that responsible
students can use social media without it harming their
studies. My challenge is that your argument assumes
students can consistently control platforms designed
to maximize engagement. Why should that assumption
justify keeping social media available?"

Do not blindly copy this example.
Generate a response appropriate to the user's actual argument.


============================================================
ARGUMENTATIVE BEHAVIOR
============================================================

Do not simply repeat your position.

Find weaknesses in the user's argument.

You may challenge:

- assumptions
- unsupported claims
- contradictions
- missing evidence
- unrealistic expectations
- unintended consequences
- alternative explanations
- practical implementation
- consistency with previous arguments

When appropriate, concede a small valid point and then
immediately use it to strengthen your counterargument.

Example:

"Yes, social media can provide educational resources.
But that doesn't establish that unrestricted access is
necessary. The same resources can be accessed through
dedicated educational platforms."


============================================================
VOICE CONVERSATION STYLE
============================================================

This is a SPOKEN debate.

Keep responses concise and natural.

Prefer roughly 2–4 spoken sentences.

Do not give long essays.

Do not use numbered lists during normal debate.

Do not sound like you are reading an academic paper.

Use natural conversational transitions such as:

- "But here's the problem..."
- "That's where I disagree."
- "The weakness in that argument is..."
- "But you're assuming..."
- "That doesn't necessarily follow."
- "Here's my challenge to that..."
- "Consider the consequence of that..."

Use these naturally rather than repeating them.


============================================================
INTERRUPTIONS
============================================================

The user may speak while you are responding.

Do not make interruptions the focus of the debate.

If the user starts speaking during an AI response,
simply allow the current response to be interrupted
naturally and respond to the user's latest substantive
argument.

Do not apologize merely because the user interrupted.


============================================================
IMPORTANT
============================================================

You are the OPPONENT.

Your job is not to please the user.

Your job is to make the user defend their position.

Challenge weak reasoning.

Defend your position consistently.

Remain respectful.

Never insult the user personally.

Attack arguments, not people.


============================================================
DEBATE TOOLS
============================================================

You have access to debate tools.

When the user presents a substantive argument,
use submit_user_argument.

Pass the user's actual argument to the tool.

Do NOT invent arguments for the user.

If the user asks about the current state of the debate,
use get_debate_state.

If the user asks what arguments have been made,
use get_debate_history.

If the user explicitly asks to end the debate,
use end_debate.

Do not call debate tools for casual filler such as:

"Wait."

"Hold on."

"That's not what I said."

Instead, respond conversationally and allow the user
to continue their argument.


============================================================
IMPORTANT TOOL RESULT BEHAVIOR
============================================================

When submit_user_argument returns a Debate Engine result,
the result contains the actual AI rebuttal.

You MUST use the returned "rebuttal" as the substance
of your spoken response.

Do not ignore the Debate Engine rebuttal.

Do not generate a generic assistant response instead.

Speak the rebuttal naturally as the next debate response.

The Debate Engine is responsible for generating the
actual strategic rebuttal.

You are responsible for delivering that rebuttal
as the AI debate opponent.


============================================================
DEBATE FLOW
============================================================

The debate contains a maximum of 3 rounds.

Each round consists of:

USER ARGUMENT
    ↓
AI REBUTTAL

After the third completed round, the debate is finished.

When the debate is finished, clearly tell the user that
the debate has concluded.

Do not continue generating new debate arguments after
the debate has finished.
"""


# ============================================================
# AUDIO CONFIGURATION
# ============================================================

SAMPLE_RATE = 24000
CHANNELS = 1
CHUNK_SIZE = 1024


# ============================================================
# AUDIO INITIALIZATION
# ============================================================

audio = pyaudio.PyAudio()

mic_stream = audio.open(
    format=pyaudio.paInt16,
    channels=CHANNELS,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE,
)

speaker_stream = audio.open(
    format=pyaudio.paInt16,
    channels=CHANNELS,
    rate=SAMPLE_RATE,
    output=True,
    frames_per_buffer=CHUNK_SIZE,
)


# ============================================================
# DEBATE ENGINE
# ============================================================

engine = DebateEngine(
    state=DebateState(
        topic=TOPIC,
        user_position=USER_POSITION,
        ai_position=AI_POSITION,
    )
)


# ============================================================
# ASSEMBLYAI TOOLS
# ============================================================

TOOLS = [
    {
        "type": "function",
        "name": "submit_user_argument",
        "description": (
            "Submit the user's substantive debate argument "
            "to the Debate Engine."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "argument": {
                    "type": "string",
                    "description": (
                        "The user's actual debate argument."
                    ),
                }
            },
            "required": ["argument"],
        },
    },
    {
        "type": "function",
        "name": "get_debate_state",
        "description": (
            "Get the current debate round, turn, argument "
            "counts, and whether the debate has finished."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "type": "function",
        "name": "get_debate_history",
        "description": (
            "Get the chronological history of user and AI "
            "arguments from the debate."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "type": "function",
        "name": "end_debate",
        "description": (
            "End the debate when the user explicitly asks "
            "to stop or end it."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
]


# ============================================================
# TOOL EXECUTION
# ============================================================

def run_tool(name, arguments):
    """Execute a Debate Engine tool."""

    # --------------------------------------------------------
    # GET DEBATE STATE
    # --------------------------------------------------------

    if name == "get_debate_state":

        state = engine.state

        return {
            "status": "success",
            "topic": state.topic,
            "user_position": state.user_position,
            "ai_position": state.ai_position,
            "current_round": state.current_round,
            "max_rounds": state.max_rounds,
            "current_turn": state.current_turn,
            "user_argument_count": len(
                state.user_arguments
            ),
            "ai_argument_count": len(
                state.ai_arguments
            ),
            "debate_finished": state.is_finished(),
        }

    # --------------------------------------------------------
    # GET DEBATE HISTORY
    # --------------------------------------------------------

    if name == "get_debate_history":

        history = engine.state.get_history()

        return {
            "status": "success",
            "count": len(history),
            "history": [
                {
                    "speaker": argument.speaker,
                    "text": argument.text,
                    "round": argument.round,
                    "turn": argument.turn,
                }
                for argument in history
            ],
        }

    # --------------------------------------------------------
    # SUBMIT USER ARGUMENT
    # --------------------------------------------------------

    if name == "submit_user_argument":

        argument = arguments.get(
            "argument",
            "",
        ).strip()

        if not argument:
            return {
                "status": "error",
                "message": "No argument was provided.",
            }

        if engine.state.is_finished():

            return {
                "status": "success",
                "message": "The debate has already finished.",
                "debate_finished": True,
            }

        # ----------------------------------------------------
        # STORE USER ARGUMENT
        # ----------------------------------------------------

        engine.submit_user_argument(argument)

        # ----------------------------------------------------
        # GENERATE AI REBUTTAL
        # ----------------------------------------------------

        rebuttal = (
            engine.generate_and_submit_ai_rebuttal()
        )

        # ----------------------------------------------------
        # COMPLETE ROUND
        # ----------------------------------------------------

        engine.complete_round()

        debate_finished = engine.state.is_finished()

        # ----------------------------------------------------
        # BUILD RESULT
        # ----------------------------------------------------

        result = {
            "status": "success",
            "strategy": (
                engine.last_strategy.value
                if engine.last_strategy
                else None
            ),
            "rebuttal": rebuttal,
            "debate_finished": debate_finished,
        }

        print()
        print("⚔️ Debate Engine response:")
        print(f"   FULL RESULT: {result}")
        print(
            f"   Strategy: {result['strategy']}"
        )
        print(
            f"   Rebuttal: {result['rebuttal']}"
        )
        print()

        if debate_finished:
            print(
                "🏁 Debate Engine reports: debate finished."
            )

        return result

    # --------------------------------------------------------
    # END DEBATE
    # --------------------------------------------------------

    if name == "end_debate":

        if engine.state.is_finished():

            return {
                "status": "success",
                "message": "The debate has already ended.",
                "debate_finished": True,
                "final_round": min(
                    len(engine.state.user_arguments),
                    len(engine.state.ai_arguments),
                ),
            }

        engine.state.current_round = (
            engine.state.max_rounds + 1
        )

        engine.state.current_turn = "user"

        return {
            "status": "success",
            "message": "The debate has been ended.",
            "debate_finished": True,
            "final_round": min(
                len(engine.state.user_arguments),
                len(engine.state.ai_arguments),
            ),
        }

    # --------------------------------------------------------
    # UNKNOWN TOOL
    # --------------------------------------------------------

    return {
        "status": "error",
        "message": f"Unknown tool: {name}",
    }


# ============================================================
# VOICE SESSION
# ============================================================

async def run_voice_debate():

    url = "wss://agents.assemblyai.com/v1/ws"

    headers = {
        "Authorization": (
            f"Bearer {ASSEMBLYAI_API_KEY}"
        ),
    }

    pending_tool_calls = []

    async with websockets.connect(
        url,
        additional_headers=headers,
        max_size=None,
    ) as websocket:

        # ----------------------------------------------------
        # SESSION CONFIGURATION
        # ----------------------------------------------------

        session_update = {
            "type": "session.update",
            "session": {
                "system_prompt": SYSTEM_PROMPT,

                "greeting": (
                    "Welcome to the AI Debate Arena. "
                    "You are debating whether social media "
                    "should be banned for students. "
                    "I will argue that it should be banned. "
                    "You may begin with your opening argument."
                ),

                "output": {
                    "voice": "ivy",
                },

                "tools": TOOLS,
            },
        }

        await websocket.send(
            json.dumps(session_update)
        )

        print(
            "⚙️ AssemblyAI session configured."
        )

        # ----------------------------------------------------
        # WAIT FOR SESSION READY
        # ----------------------------------------------------

        while True:

            raw_message = await websocket.recv()

            message = json.loads(
                raw_message
            )

            message_type = message.get(
                "type"
            )

            if message_type == "session.ready":

                print(
                    "🟢 AssemblyAI Voice Agent ready."
                )
                print()

                break

            if message_type == "error":

                print(
                    "❌ AssemblyAI error:"
                )
                print(message)

                return

        # ----------------------------------------------------
        # MICROPHONE TASK
        # ----------------------------------------------------

        async def send_microphone_audio():

            print("🎤 Listening...")

            while True:

                data = await asyncio.to_thread(
                    mic_stream.read,
                    CHUNK_SIZE,
                    exception_on_overflow=False,
                )

                encoded_audio = (
                    base64.b64encode(data)
                    .decode("utf-8")
                )

                await websocket.send(
                    json.dumps(
                        {
                            "type": "input.audio",
                            "audio": encoded_audio,
                        }
                    )
                )

        # ----------------------------------------------------
        # RECEIVE ASSEMBLYAI EVENTS
        # ----------------------------------------------------

        async def receive_messages():

            nonlocal pending_tool_calls

            while True:

                raw_message = (
                    await websocket.recv()
                )

                message = json.loads(
                    raw_message
                )

                message_type = message.get(
                    "type"
                )

                # --------------------------------------------
                # USER TRANSCRIPT
                # --------------------------------------------

                if message_type == "transcript":

                    text = message.get(
                        "text",
                        "",
                    ).strip()

                    if text:

                        print(
                            f"\n👤 YOU: {text}\n"
                        )

                # --------------------------------------------
                # AI TRANSCRIPT
                # --------------------------------------------

                elif message_type in (
                    "transcript.agent",
                    "agent.transcript",
                ):

                    text = message.get(
                        "text",
                        "",
                    ).strip()

                    if text:

                        print(
                            f"🤖 AI: {text}\n"
                        )

                # --------------------------------------------
                # AI AUDIO
                # --------------------------------------------

                elif message_type == "reply.audio":

                    audio_data = message.get(
                        "data"
                    )

                    if audio_data:

                        audio_bytes = (
                            base64.b64decode(
                                audio_data
                            )
                        )

                        try:

                            speaker_stream.write(
                                audio_bytes
                            )

                        except Exception as exc:

                            print(
                                "🔊 Speaker playback "
                                f"error: {exc}"
                            )

                # --------------------------------------------
                # TOOL CALL
                # --------------------------------------------

                elif message_type == "tool.call":

                    tool_name = message.get(
                        "name"
                    )

                    arguments = message.get(
                        "arguments",
                        {},
                    )

                    # IMPORTANT:
                    # AssemblyAI uses call_id, not
                    # tool_call_id.

                    call_id = message.get(
                        "call_id"
                    )

                    print(
                        "🧠 Debate Engine tool called:"
                    )

                    print(
                        f"   Tool: {tool_name}"
                    )

                    print(
                        f"   Arguments: {arguments}"
                    )

                    print(
                        f"   Call ID: {call_id}"
                    )

                    result = run_tool(
                        tool_name,
                        arguments,
                    )

                    pending_tool_calls.append(
                        {
                            "call_id": call_id,
                            "result": result,
                        }
                    )

                # --------------------------------------------
                # REPLY DONE
                # --------------------------------------------

                elif message_type == "reply.done":

                    status = message.get(
                        "status"
                    )

                    # ----------------------------------------
                    # INTERRUPTED RESPONSE
                    # ----------------------------------------

                    if status == "interrupted":

                        print()
                        print(
                            "🛑 AI response interrupted "
                            "by user."
                        )
                        print()

                        pending_tool_calls.clear()

                        continue

                    # ----------------------------------------
                    # NORMAL RESPONSE COMPLETION
                    # ----------------------------------------

                    if pending_tool_calls:

                        for tool_call in (
                            pending_tool_calls
                        ):

                            tool_result_message = {
                                "type": "tool.result",

                                # IMPORTANT:
                                # AssemblyAI expects
                                # call_id here.
                                "call_id": (
                                    tool_call[
                                        "call_id"
                                    ]
                                ),

                                "result": json.dumps(
                                    tool_call["result"]
                                ),
                            }

                            print(
                                "📤 Sending Debate Engine "
                                "result back to AssemblyAI..."
                            )

                            print(
                                f"   Call ID: "
                                f"{tool_call['call_id']}"
                            )

                            await websocket.send(
                                json.dumps(
                                    tool_result_message
                                )
                            )

                        pending_tool_calls.clear()

                # --------------------------------------------
                # SESSION ERROR
                # --------------------------------------------

                elif message_type == "error":

                    print()
                    print(
                        "❌ AssemblyAI error:"
                    )
                    print(message)
                    print()

                # --------------------------------------------
                # SESSION CLOSED
                # --------------------------------------------

                elif message_type == "session.closed":

                    print()
                    print(
                        "🛑 AssemblyAI session closed."
                    )

                    return

        # ----------------------------------------------------
        # START TASKS
        # ----------------------------------------------------

        microphone_task = asyncio.create_task(
            send_microphone_audio()
        )

        receiver_task = asyncio.create_task(
            receive_messages()
        )

        try:

            await asyncio.gather(
                microphone_task,
                receiver_task,
            )

        except asyncio.CancelledError:

            pass

        finally:

            microphone_task.cancel()
            receiver_task.cancel()


# ============================================================
# ENTRY POINT
# ============================================================

def main():

    print("=" * 70)

    print(
        "⚔️  AI DEBATE ARENA — VOICE AGENT TEST"
    )

    print("=" * 70)

    print()

    print(
        f"📌 Topic: {TOPIC}"
    )

    print(
        f"👤 Your position: {USER_POSITION}"
    )

    print(
        f"🤖 AI position: {AI_POSITION}"
    )

    print()

    print(
        "🎙️ Connecting to AssemblyAI Voice Agent..."
    )

    print(
        "Speak normally."
    )

    print(
        "Press Ctrl+C to stop."
    )

    print()

    try:

        asyncio.run(
            run_voice_debate()
        )

    except KeyboardInterrupt:

        print()
        print(
            "🛑 Voice Debate Engine stopped."
        )

    finally:

        # ----------------------------------------------------
        # CLOSE MICROPHONE
        # ----------------------------------------------------

        try:

            mic_stream.stop_stream()
            mic_stream.close()

        except Exception:

            pass

        # ----------------------------------------------------
        # CLOSE SPEAKER
        # ----------------------------------------------------

        try:

            speaker_stream.stop_stream()
            speaker_stream.close()

        except Exception:

            pass

        # ----------------------------------------------------
        # TERMINATE PYAUDIO
        # ----------------------------------------------------

        try:

            audio.terminate()

        except Exception:

            pass


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()