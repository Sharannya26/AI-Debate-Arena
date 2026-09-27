from debate_arena.debate.strategy import DebateStrategy
from debate_arena.debate.strategy_prompts import build_strategy_prompt
from debate_arena.llm.client import LLMClient


def main() -> None:
    context = """
Topic: Should social media be banned for students?
User position: Against
AI position: For

Debate history:
Round 1 - User: Social media helps students collaborate and access educational resources.
Round 1 - AI: Educational platforms can provide these benefits without the distractions of social media.
Round 2 - User: Those risks can be reduced through screen-time limits and digital literacy education.
""".strip()

    latest_argument = (
        "Those risks can be reduced through screen-time limits "
        "and digital literacy education."
    )

    strategy_prompt = build_strategy_prompt(
        context=context,
        latest_argument=latest_argument,
    )

    llm = LLMClient()

    strategy_response = llm.generate_response(strategy_prompt)

    print("Gemini strategy selection:")
    print(strategy_response)

    selected_strategy = strategy_response.strip().lower()

    valid_strategies = {
        strategy.value
        for strategy in DebateStrategy
    }

    if selected_strategy not in valid_strategies:
        raise RuntimeError(
            f"Gemini returned an invalid strategy: {selected_strategy!r}"
        )

    print("\nValid strategy selected:")
    print(selected_strategy)


if __name__ == "__main__":
    main()