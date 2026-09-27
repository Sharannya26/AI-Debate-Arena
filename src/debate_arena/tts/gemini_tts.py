from __future__ import annotations

import asyncio
import wave

from google import genai
from google.genai import types

from debate_arena.config.settings import GEMINI_API_KEY


class GeminiTTS:
    """
    Converts AI debate responses into spoken audio using Gemini TTS.

    Cloud-safe design:
        synthesize() -> WAV file

    Local Windows design:
        speak() -> WAV + winsound
        speak_stream() -> Gemini streaming + sounddevice

    Hardware-specific dependencies are imported only inside the
    methods that actually need them.
    """

    def __init__(
        self,
        model: str = "gemini-3.1-flash-tts-preview",
        voice: str = "Kore",
    ):
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = model
        self.voice = voice

    def synthesize(
        self,
        text: str,
        output_path: str = "gemini_tts_output.wav",
    ) -> str:
        """
        Convert text into a complete WAV audio file.

        This method is completely cloud-safe because it does not
        access a microphone or speaker.
        """

        if not text.strip():
            raise ValueError(
                "TTS text cannot be empty."
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=(
                            types.PrebuiltVoiceConfig(
                                voice_name=self.voice,
                            )
                        )
                    )
                ),
            ),
        )

        audio_data = (
            response
            .candidates[0]
            .content
            .parts[0]
            .inline_data
            .data
        )

        with wave.open(
            output_path,
            "wb",
        ) as audio_file:
            audio_file.setnchannels(1)
            audio_file.setsampwidth(2)
            audio_file.setframerate(24000)
            audio_file.writeframes(audio_data)

        return output_path

    def speak(
        self,
        text: str,
    ) -> str:
        """
        Generate complete speech and play it locally.

        Windows-only playback is imported lazily so this method does
        not affect Streamlit Cloud imports.
        """

        output_path = self.synthesize(
            text
        )

        import winsound

        winsound.PlaySound(
            output_path,
            winsound.SND_FILENAME,
        )

        return output_path

    async def speak_stream_async(
        self,
        text: str,
    ) -> None:
        """
        Stream Gemini TTS directly to a local speaker.

        This is intended for the local Windows application.
        """

        if not text.strip():
            raise ValueError(
                "TTS text cannot be empty."
            )

        import sounddevice as sd

        stream = (
            await self.client.aio.models.generate_content_stream(
                model=self.model,
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=(
                                types.PrebuiltVoiceConfig(
                                    voice_name=self.voice,
                                )
                            )
                        )
                    ),
                ),
            )
        )

        with sd.RawOutputStream(
            samplerate=24000,
            channels=1,
            dtype="int16",
        ) as audio_output:

            async for chunk in stream:

                if not chunk.candidates:
                    continue

                content = (
                    chunk.candidates[0]
                    .content
                )

                if (
                    not content
                    or not content.parts
                ):
                    continue

                for part in content.parts:

                    if not part.inline_data:
                        continue

                    audio_data = (
                        part.inline_data.data
                    )

                    if not audio_data:
                        continue

                    audio_output.write(
                        audio_data
                    )

    def speak_stream(
        self,
        text: str,
    ) -> None:
        """
        Stream Gemini TTS and play it immediately
        on the local machine.
        """

        if not text.strip():
            raise ValueError(
                "TTS text cannot be empty."
            )

        asyncio.run(
            self.speak_stream_async(
                text
            )
        )