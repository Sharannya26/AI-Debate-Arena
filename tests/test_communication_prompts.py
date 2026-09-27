from debate_arena.debate.communication_prompts import (
    build_communication_analysis_prompt,
)


def create_analysis_data() -> dict:
    return {
        "word_count": 30,
        "sentence_count": 3,
        "duration": 15.0,
        "words_per_minute": 120.0,
        "speaking_pace": "moderate",
        "average_words_per_sentence": 10.0,
        "total_filler_count": 2,
        "filler_counts": {
            "um": 1,
            "like": 1,
        },
        "filler_rate": 2 / 30,
    }


def test_prompt_contains_word_count():
    prompt = build_communication_analysis_prompt(
        create_analysis_data()
    )

    assert "Word count: 30" in prompt


def test_prompt_contains_sentence_count():
    prompt = build_communication_analysis_prompt(
        create_analysis_data()
    )

    assert "Sentence count: 3" in prompt


def test_prompt_contains_duration():
    prompt = build_communication_analysis_prompt(
        create_analysis_data()
    )

    assert "Duration: 15.0 seconds" in prompt


def test_prompt_contains_words_per_minute():
    prompt = build_communication_analysis_prompt(
        create_analysis_data()
    )

    assert "Words per minute: 120.0" in prompt


def test_prompt_contains_speaking_pace():
    prompt = build_communication_analysis_prompt(
        create_analysis_data()
    )

    assert "Speaking pace: moderate" in prompt


def test_prompt_contains_filler_data():
    prompt = build_communication_analysis_prompt(
        create_analysis_data()
    )

    assert "Total filler count: 2" in prompt
    assert "Filler counts:" in prompt
    assert "Filler rate:" in prompt


def test_prompt_contains_feedback_categories():
    prompt = build_communication_analysis_prompt(
        create_analysis_data()
    )

    assert "clarity" in prompt
    assert "conciseness" in prompt
    assert "delivery" in prompt
    assert "strengths" in prompt
    assert "weaknesses" in prompt
    assert "recommendations" in prompt


def test_prompt_contains_safety_rules():
    prompt = build_communication_analysis_prompt(
        create_analysis_data()
    )

    assert "Do not invent measurements." in prompt
    assert "Do not diagnose the speaker." in prompt


def test_prompt_is_not_empty():
    prompt = build_communication_analysis_prompt(
        create_analysis_data()
    )

    assert prompt.strip()