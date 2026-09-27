from debate_arena.debate.moment_analysis import MomentAnalysis
from debate_arena.debate.moment_prompts import (
    build_moment_analysis_prompt,
)


def create_analysis():
    return MomentAnalysis(
        strongest_moments=[
            "Round 2: Strong argument quality — Strong argument quality."
        ],
        weakest_moments=[
            "Round 1: Weak evidence usage — Limited evidence usage."
        ],
        key_insights=[
            "Reasoning became clearer in later rounds."
        ],
    )


def test_prompt_builder_returns_string():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert isinstance(prompt, str)
    assert prompt.strip()


def test_prompt_contains_strongest_moments():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert (
        "Strong argument quality"
        in prompt
    )


def test_prompt_contains_weakest_moments():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert (
        "Limited evidence usage"
        in prompt
    )


def test_prompt_contains_key_insights():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert (
        "Reasoning became clearer in later rounds."
        in prompt
    )


def test_prompt_requires_json_output():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert "Return ONLY valid JSON" in prompt
    assert '"strongest_interpretation"' in prompt
    assert '"weakest_interpretation"' in prompt
    assert '"key_insights"' in prompt


def test_prompt_forbids_numerical_scores():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert "Do NOT introduce numerical scores." in prompt


def test_prompt_forbids_inventing_information():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert (
        "Do NOT invent arguments, examples, evidence, statistics, events,"
        in prompt
    )


def test_prompt_forbids_fact_checking():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert "Do NOT fact-check the debate." in prompt


def test_prompt_forbids_political_judgment():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert "Do NOT judge political positions." in prompt


def test_prompt_forbids_personality_inference():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert (
        "Do NOT make claims about personality, intelligence, mental state,"
        in prompt
    )


def test_prompt_rejects_none_analysis():
    try:
        build_moment_analysis_prompt(None)
    except ValueError as error:
        assert str(error) == (
            "Moment analysis cannot be None."
        )
    else:
        raise AssertionError(
            "Expected ValueError."
        )


def test_prompt_mentions_deterministic_analysis():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert (
        "deterministic Python analysis"
        in prompt
    )


def test_prompt_mentions_strongest_and_weakest_interpretation():
    prompt = build_moment_analysis_prompt(
        create_analysis()
    )

    assert "Strongest moments" in prompt
    assert "Weakest moments" in prompt