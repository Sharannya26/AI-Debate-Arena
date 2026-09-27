from debate_arena.tts.gemini_tts import GeminiTTS


def main() -> None:
    tts = GeminiTTS()

    text = (
        "That argument overlooks an important point. "
        "The issue is not simply whether social media is useful, "
        "but whether its benefits outweigh its risks for students."
    )

    output_path = tts.speak(text)

    print(f"TTS module test successful! ✅")
    print(f"Audio saved to: {output_path}")


if __name__ == "__main__":
    main()