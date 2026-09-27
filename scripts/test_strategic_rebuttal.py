from debate_arena.debate.prompts import build_rebuttal_prompt
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

    strategy = "alternative_solution"

    prompt = build_rebuttal_prompt(
        context=context,
        latest_argument=latest_argument,
        strategy=strategy,
    )

    llm = LLMClient()

    response = llm.generate_response(prompt)

    print("Selected strategy:")
    print(strategy)

    print("\nStrategic AI rebuttal:")
    print(response)


if __name__ == "__main__":
    main()