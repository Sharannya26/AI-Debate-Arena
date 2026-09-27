import wave
import winsound

from google import genai
from google.genai import types

from debate_arena.config.settings import GEMINI_API_KEY


def main() -> None:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    text = (
        "Hello! Welcome to the AI Debate Arena. "
        "Let's begin the debate."
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Kore",
                    )
                )
            ),
        ),
    )

    audio_data = response.candidates[0].content.parts[0].inline_data.data

    wav_path = "gemini_tts_test.wav"

    with wave.open(wav_path, "wb") as audio_file:
        audio_file.setnchannels(1)
        audio_file.setsampwidth(2)
        audio_file.setframerate(24000)
        audio_file.writeframes(audio_data)

    print("Gemini TTS generation successful! 🔊")
    print(f"Audio saved to: {wav_path}")

    print("Playing audio...")
    winsound.PlaySound(wav_path, winsound.SND_FILENAME)

    print("Playback complete! ✅")


if __name__ == "__main__":
    main()