from google import genai

from debate_arena.config.settings import GEMINI_API_KEY


def main() -> None:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=(
            "You are testing the reasoning engine of an AI debate application. "
            "Give me a one-sentence rebuttal to this argument: "
            "'Social media is always harmful to students.'"
        ),
    )

    print("Gemini response:")
    print(response.text)


if __name__ == "__main__":
    main()