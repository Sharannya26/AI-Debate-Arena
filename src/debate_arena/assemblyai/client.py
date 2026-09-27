import assemblyai as aai

from debate_arena.config.settings import ASSEMBLYAI_API_KEY


def create_client() -> None:
    """Configure the AssemblyAI SDK using our project API key."""
    if not ASSEMBLYAI_API_KEY:
        raise RuntimeError("ASSEMBLYAI_API_KEY is not configured.")

    aai.settings.api_key = ASSEMBLYAI_API_KEY


def get_client() -> aai.Client:
    """Create and return an authenticated AssemblyAI client."""
    create_client()
    return aai.Client()


def submit_test_transcription(audio_url: str):
    """Submit an audio URL to AssemblyAI and return the transcript job."""
    create_client()

    transcriber = aai.Transcriber()
    return transcriber.submit(audio_url)