from debate_arena.llm.client import LLMClient


def main() -> None:
    llm = LLMClient()

    response = llm.generate_response(
        "Give me a one-sentence rebuttal to this argument: "
        "'Students should never use social media.'"
    )

    print("LLMClient response:")
    print(response)


if __name__ == "__main__":
    main()