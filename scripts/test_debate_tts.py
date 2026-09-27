from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState
import time


def main() -> None:
    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    engine = DebateEngine(state)

    user_argument = (
        "Social media should not be banned because students can use it "
        "to communicate, collaborate, and access educational resources."
    )

    print("\n🎙️ USER:")
    print(user_argument)

    engine.submit_user_argument(user_argument)

    print("\n🧠 Generating AI rebuttal...")

    reasoning_start = time.perf_counter()

    rebuttal = engine.generate_ai_rebuttal()

    reasoning_time = time.perf_counter() - reasoning_start

    print(f"⏱️ Gemini reasoning time: {reasoning_time:.2f} seconds")

    print("\n🤖 AI REBUTTAL:")
    print(rebuttal)

    print("\n🔊 AI SPEAKING...")

    tts_start = time.perf_counter()

    
    engine.speak_ai_rebuttal(rebuttal)

    
    tts_time = time.perf_counter() - tts_start

    print(f"⏱️ Gemini TTS time: {tts_time:.2f} seconds")
    print("\n✅ Streaming voice rebuttal complete!")

   


if __name__ == "__main__":
    main()