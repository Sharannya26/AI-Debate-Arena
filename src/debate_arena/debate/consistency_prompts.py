def build_consistency_prompt(
    user_arguments: list[str],
) -> str:
    """
    Build a prompt for semantic consistency analysis.

    Gemini should determine whether the user's arguments
    remain logically consistent across debate rounds.

    The model should analyze consistency of the user's
    expressed position, not whether that position is
    objectively correct.
    """

    if user_arguments is None:
        raise ValueError("User arguments cannot be None.")

    cleaned_arguments = [
        argument.strip()
        for argument in user_arguments
        if argument and argument.strip()
    ]

    if len(cleaned_arguments) < 2:
        raise ValueError(
            "At least two user arguments are required."
        )

    formatted_arguments = "\n\n".join(
        (
            f"Round {index + 1}:\n"
            f"{argument}"
        )
        for index, argument in enumerate(cleaned_arguments)
    )

    return f"""
You are analyzing consistency in a debate.

Your task is to determine whether the USER'S arguments
remain logically and semantically consistent across
different debate rounds.

Do NOT judge whether the user's overall position is:

- correct or incorrect
- morally right or wrong
- politically desirable or undesirable
- persuasive or unpersuasive

Focus ONLY on whether the user's own claims remain
consistent with one another.

Consider:

- whether the user maintains the same core position
- whether later arguments contradict earlier claims
- whether the user changes an important assumption
- whether the user introduces a claim that conflicts
  with something they previously stated
- whether different wording expresses the same idea
- whether apparent differences are merely changes in
  examples or supporting details

Do NOT treat different wording as a contradiction
when the underlying meaning is compatible.

Do NOT invent contradictions that are not supported
by the arguments.

User arguments:

{formatted_arguments}

Return ONLY valid JSON with exactly this structure:

{{
    "consistency": "string",
    "consistent_points": ["string"],
    "inconsistent_points": ["string"]
}}

Requirements:

- "consistency" should briefly summarize the overall
  semantic consistency across the arguments.
- "consistent_points" should identify important ideas
  that remain compatible across rounds.
- "inconsistent_points" should identify specific claims
  or assumptions that appear to conflict.
- Mention the relevant rounds when describing a
  consistency or inconsistency.
- Consider paraphrases and semantically equivalent ideas.
- Do not rely only on exact keyword overlap.
- Do not invent information that is absent from the
  user's arguments.
- Keep the analysis concise and evidence-based.
""".strip()