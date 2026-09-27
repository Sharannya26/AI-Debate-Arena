from __future__ import annotations

import io
import tempfile
import time
import wave
from pathlib import Path
from typing import Any

import assemblyai as aai
from google import genai
from google.genai import types

from debate_arena.config.settings import GEMINI_API_KEY
from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.speech_sample import SpeechSample


class CloudVoiceAgent:
    """
    Browser/cloud voice adapter for Streamlit Community Cloud.

    Unlike the local VoiceAgent, this class never imports or uses PyAudio,
    sounddevice, or winsound. Streamlit receives the browser microphone
    recording and passes it here as an UploadedFile/file-like object.
    """

    def __init__(
        self,
        engine: DebateEngine,
        api_key: str,
        gemini_api_key: str | None = None,
    ) -> None:
        self.engine = engine
        self.api_key = api_key
        self.gemini_api_key = gemini_api_key or GEMINI_API_KEY
        self._running = False

    def start(self) -> None:
        if not self.api_key:
            raise RuntimeError("ASSEMBLYAI_API_KEY is not configured.")

        self._running = True

    def stop(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running

    @staticmethod
    def _audio_duration(audio_bytes: bytes) -> float:
        """Read duration from the browser-generated WAV container."""
        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                if rate:
                    return frames / float(rate)
        except (wave.Error, EOFError, ValueError):
            pass

        return 0.0

    def _transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe one browser recording with AssemblyAI."""
        aai.settings.api_key = self.api_key
        transcriber = aai.Transcriber()

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(audio_bytes)

        try:
            transcript = transcriber.transcribe(str(temp_path))
        finally:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass

        status = getattr(transcript, "status", None)
        if status is not None:
            status_value = str(getattr(status, "value", status)).lower()
            if status_value == "error":
                error = getattr(transcript, "error", "Unknown AssemblyAI error")
                raise RuntimeError(f"AssemblyAI transcription failed: {error}")

        text = str(getattr(transcript, "text", "") or "").strip()

        if not text:
            raise RuntimeError(
                "AssemblyAI did not detect any speech in that recording. "
                "Please record your argument again."
            )

        return text

    def _generate_tts_wav(self, text: str) -> bytes:
        """Generate browser-playable WAV bytes with Gemini TTS."""
        if not self.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured.")

        client = genai.Client(api_key=self.gemini_api_key)

        response = client.models.generate_content(
            model="gemini-3.1-flash-tts-preview",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Kore"
                        )
                    )
                ),
            ),
        )

        try:
            audio_data = response.candidates[0].content.parts[0].inline_data.data
        except (AttributeError, IndexError, TypeError) as exc:
            raise RuntimeError(
                "Gemini TTS returned no audio data."
            ) from exc

        if not audio_data:
            raise RuntimeError("Gemini TTS returned empty audio data.")

        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(24_000)
            wav_file.writeframes(audio_data)

        return wav_buffer.getvalue()

    def process_audio(self, audio_file: Any) -> dict[str, Any]:
        """
        Process one completed browser recording.

        Returns a small serializable result dictionary so the Streamlit layer
        can update session state and play the returned WAV bytes with st.audio.
        """
        if not self._running:
            raise RuntimeError("Cloud voice agent is not running.")

        if self.engine.state.is_finished():
            raise RuntimeError("The debate is already complete.")

        if not self.engine.is_user_turn():
            raise RuntimeError("Please wait for the AI rebuttal to finish.")

        audio_bytes = audio_file.getvalue()
        if not audio_bytes:
            raise RuntimeError("The browser recording was empty.")

        started_at = time.perf_counter()
        transcript_text = self._transcribe(audio_bytes)
        duration = self._audio_duration(audio_bytes)

        current_round = self.engine.state.current_round
        turn_number = len(self.engine.state.user_arguments) + 1
        previous_ai_argument = (
            self.engine.state.ai_arguments[-1]
            if self.engine.state.ai_arguments
            else None
        )

        speech_sample = SpeechSample(
            text=transcript_text,
            duration=duration,
            round=current_round,
            turn=turn_number,
        )

        self.engine.submit_user_argument(transcript_text)

        round_performance = self.engine.round_performance_analyzer.analyze(
            speech_sample,
            previous_ai_argument,
        )

        if round_performance is not None:
            self.engine.round_performances.append(round_performance)

        ai_rebuttal = self.engine.generate_and_submit_ai_rebuttal()

        if not self.engine.is_finished():
            self.engine.complete_round()

        debate_finished = self.engine.state.is_finished()

        audio_bytes_output: bytes | None = None
        audio_error: str | None = None

        try:
            audio_bytes_output = self._generate_tts_wav(ai_rebuttal)
        except Exception as exc:
            # The text debate remains valid even if TTS has a temporary cloud
            # problem. The UI reports the audio problem without losing the turn.
            audio_error = f"AI audio unavailable: {type(exc).__name__}: {exc}"

        elapsed = time.perf_counter() - started_at
        self._last_processing_seconds = elapsed

        return {
            "user_transcript": transcript_text,
            "ai_transcript": ai_rebuttal,
            "audio_bytes": audio_bytes_output,
            "audio_error": audio_error,
            "debate_finished": debate_finished,
        }
