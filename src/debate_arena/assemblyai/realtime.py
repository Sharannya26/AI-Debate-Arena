from collections.abc import Callable

import pyaudio

from assemblyai.streaming.v3 import (
    BeginEvent,
    RealTimeError,
    RealTimeEvents,
    RealTimeParameters,
    RealTimeTranscriber,
    RealTimeTranscriberOptions,
    TerminationEvent,
    TurnEvent,
)

from debate_arena.config.settings import ASSEMBLYAI_API_KEY


SAMPLE_RATE = 16000
CHANNELS = 1
FRAMES_PER_BUFFER = 800


def on_begin(
    client: RealTimeTranscriber,
    event: BeginEvent,
) -> None:
    print("\n" + "=" * 60)
    print("🎙️ AssemblyAI Realtime Session Started")
    print(f"Session ID: {event.id}")
    print("=" * 60)


def on_turn(
    client: RealTimeTranscriber,
    event: TurnEvent,
    on_final_transcript: Callable[[str], None] | None = None,
) -> None:
    """Handle partial and final AssemblyAI transcripts."""

    if not event.transcript:
        return

    if event.end_of_turn:
        print(f"\n📝 FINAL: {event.transcript}")

        if on_final_transcript:
            on_final_transcript(event.transcript)

    else:
        print(
            f"\r🎤 Listening: {event.transcript}",
            end="",
            flush=True,
        )


def on_terminated(
    client: RealTimeTranscriber,
    event: TerminationEvent,
) -> None:
    print("\n\n" + "=" * 60)
    print("🛑 AssemblyAI Realtime Session Ended")
    print(
        f"Audio processed: "
        f"{event.audio_duration_seconds:.2f} seconds"
    )
    print("=" * 60)


def on_error(
    client: RealTimeTranscriber,
    error: RealTimeError,
) -> None:
    print(f"\n❌ AssemblyAI Realtime Error: {error}")


def start_realtime_transcription(
    on_final_transcript: Callable[[str], None] | None = None,
) -> None:
    """
    Start microphone streaming and send final transcripts
    to the optional callback.
    """

    if not ASSEMBLYAI_API_KEY:
        raise RuntimeError(
            "ASSEMBLYAI_API_KEY is not configured."
        )

    client = RealTimeTranscriber(
        RealTimeTranscriberOptions(),
        api_key=ASSEMBLYAI_API_KEY,
    )

    client.on(
        RealTimeEvents.Begin,
        on_begin,
    )

    client.on(
        RealTimeEvents.Turn,
        lambda client, event: on_turn(
            client,
            event,
            on_final_transcript,
        ),
    )

    client.on(
        RealTimeEvents.Termination,
        on_terminated,
    )

    client.on(
        RealTimeEvents.Error,
        on_error,
    )

    client.connect(
        RealTimeParameters(
            speech_model="universal-3-5-pro",
            sample_rate=SAMPLE_RATE,
        )
    )

    audio = pyaudio.PyAudio()

    microphone = audio.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER,
    )

    print("\n🎤 Microphone is ready!")
    print("Speak normally.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            audio_chunk = microphone.read(
                FRAMES_PER_BUFFER,
                exception_on_overflow=False,
            )

            client.stream(audio_chunk)

    except KeyboardInterrupt:
        print("\n\nStopping microphone...")

    finally:
        microphone.stop_stream()
        microphone.close()
        audio.terminate()
        client.disconnect(terminate=True)


if __name__ == "__main__":
    start_realtime_transcription()