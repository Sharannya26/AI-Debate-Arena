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

    print("🔊 Starting live Gemini TTS...")

    start_time = time.perf_counter()
    first_audio_time = None

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

    print("🎧 Opening speaker stream...")

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

                if first_audio_time is None:
                    first_audio_time = time.perf_counter()

                    print(
                        f"⚡ First audio chunk received: "
                        f"{first_audio_time - start_time:.2f} seconds"
                    )

                    print("🔊 PLAYBACK STARTED!")

                audio_output.write(audio_data)

    total_time = time.perf_counter() - start_time

    print(f"⏱️ Total streaming time: {total_time:.2f} seconds")

    if first_audio_time is not None:
        print(
            f"🚀 Time to first audio: "
            f"{first_audio_time - start_time:.2f} seconds"
        )

    print("✅ Live TTS test complete!")


if __name__ == "__main__":
    asyncio.run(main())