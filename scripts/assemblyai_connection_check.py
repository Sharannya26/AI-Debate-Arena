from debate_arena.assemblyai.client import submit_test_transcription


TEST_AUDIO_URL = "https://assembly.ai/wildfires.mp3"


def main():
    print("Connecting to AssemblyAI...")

    transcript = submit_test_transcription(TEST_AUDIO_URL)

    print("AssemblyAI connection successful! ✅")
    print(f"Transcript ID: {transcript.id}")
    print(f"Status: {transcript.status}")


if __name__ == "__main__":
    main()