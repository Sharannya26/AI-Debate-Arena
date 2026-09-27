def build_responsiveness_prompt(
    previous_ai_argument: str,
    user_argument: str,
) -> str:
    """
    Build a prompt for Gemini to semantically evaluate how
    directly the user's argument responds to the AI's
    previous argument.
    """

    if not previous_ai_argument or not previous_ai_argument.strip():
        raise ValueError(
            "Previous AI argument cannot be empty."
        )

    if not user_argument or not user_argument.strip():
        raise ValueError(
            "User argument cannot be empty."
        )

    previous_ai_argument = previous_ai_argument.strip()
    user_argument = user_argument.strip()

    return f"""
You are analyzing a debate conversation.

Your task is to evaluate how directly the user's response
addresses the AI's previous argument.

Do NOT judge whether the user's position is politically,
morally, or personally correct.

Focus only on whether the user actually engaged with
the points raised by the AI.

Previous AI argument:
{previous_ai_argument}

Current user response:
{user_argument}

Analyze the semantic relationship between the two arguments.

Return ONLY valid JSON with this exact structure:

{{
    "responsiveness": "string",
    "addressed_points": ["string"],
    "ignored_points": ["string"]
}}

Requirements:

- "responsiveness" should briefly describe how directly the
  user responded to the AI's argument.
- "addressed_points" should list the important ideas from
  the AI argument that the user directly addressed.
- "ignored_points" should list important ideas from the AI
  argument that the user did not meaningfully address.
- Consider paraphrases and semantically equivalent ideas.
- Do not require exact word overlap.
- Do not invent points that are not present in either argument.
- Keep the analysis concise.
""".strip()