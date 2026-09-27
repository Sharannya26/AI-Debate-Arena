import asyncio
import time
import wave

from google import genai
from google.genai import types

from debate_arena.config.settings import GEMINI_API_KEY


MODEL = "gemini-3.1-flash-tts-preview"
VOICE = "Kore"


async def main() -> None:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    text = (
        "That argument overlooks an important point. "
        "The issue is not simply whether social media is useful, "
        "but whether its benefits outweigh its risks for students."
    )

    print("🔊 Starting Gemini TTS stream...")

    start_time = time.perf_counter()
    first_audio_time = None
    audio_chunks = []

    stream = await client.aio.models.generate_content_stream(
        model=MODEL,
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=VOICE,
                    )
                )
            ),
        ),
    )

    async for chunk in stream:
        if not chunk.candidates:
            continue

        content = chunk.candidates[0].content

        if not content or not content.parts:
            continue

        for part in content.parts:
            if part.inline_data and part.inline_data.data:
                if first_audio_time is None:
                    first_audio_time = time.perf_counter()
                    print(
                        f"⚡ First audio chunk received: "
                        f"{first_audio_time - start_time:.2f} seconds"
                    )

                audio_chunks.append(part.inline_data.data)

    total_time = time.perf_counter() - start_time

    audio_data = b"".join(audio_chunks)

    print(f"📦 Audio chunks received: {len(audio_chunks)}")
    print(f"🎵 Total audio bytes: {len(audio_data)}")
    print(f"⏱️ Total streaming time: {total_time:.2f} seconds")

    if first_audio_time is not None:
        print(
            f"🚀 Time to first audio: "
            f"{first_audio_time - start_time:.2f} seconds"
        )

    wav_path = "gemini_tts_stream_test.wav"

    with wave.open(wav_path, "wb") as audio_file:
        audio_file.setnchannels(1)
        audio_file.setsampwidth(2)
        audio_file.setframerate(24000)
        audio_file.writeframes(audio_data)

    print(f"💾 Audio saved to: {wav_path}")
    print("✅ Streaming TTS test complete!")


if __name__ == "__main__":
    asyncio.run(main())