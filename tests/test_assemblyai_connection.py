from debate_arena.assemblyai.client import get_client


def test_assemblyai_connection():
    client = get_client()

    assert client is not None