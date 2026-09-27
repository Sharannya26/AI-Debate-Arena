import asyncio
import time

import sounddevice as sd

from google import genai
from google.genai import types

from debate_arena.config.settings import GEMINI_API_KEY


MODEL = "gemini-3.1-flash-tts-preview"
VOICE = "Kore"

SAMPLE_RATE = 24000
CHANNELS = 1
DTYPE = "int16"


async def main() -> None:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    text = (
        "That argument overlooks an important point. "
        "The issue is not simply whether social media is useful, "
        "but whether its benefits outweigh its risks for students."
    )

    print("🔊 Starting Gemini TTS playback diagnostic...")

    start_time = time.perf_counter()
    first_audio_time = None
    total_chunks = 0

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

    print("🎧 Opening speaker...")

    with sd.RawOutputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
    ) as audio_output:

        async for chunk in stream:

            if not chunk.candidates:
                continue

            content = chunk.candidates[0].content

            if not content or not content.parts:
                continue

            for part in content.parts:

                if not part.inline_data:
                    continue

                audio_data = part.inline_data.data

                if not audio_data:
                    continue

                total_chunks += 1

                if first_audio_time is None:
                    first_audio_time = time.perf_counter()

                    print(
                        f"⚡ First Gemini audio: "
                        f"{first_audio_time - start_time:.2f}s"
                    )

                before_write = time.perf_counter()

                audio_output.write(audio_data)

                after_write = time.perf_counter()

                write_time = after_write - before_write

                if total_chunks <= 5:
                    print(
                        f"🔊 Chunk {total_chunks}: "
                        f"{len(audio_data)} bytes | "
                        f"speaker write: {write_time:.4f}s"
                    )

    total_time = time.perf_counter() - start_time

    print()
    print(f"📦 Total chunks: {total_chunks}")
    print(f"⏱️ Total time: {total_time:.2f}s")

    if first_audio_time is not None:
        print(
            f"🚀 Time to first audio: "
            f"{first_audio_time - start_time:.2f}s"
        )

    print("✅ Playback diagnostic complete!")


if __name__ == "__main__":
    asyncio.run(main())