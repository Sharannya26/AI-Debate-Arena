def build_evidence_reasoning_prompt(
    user_arguments: list[str],
) -> str:
    if user_arguments is None:
        raise ValueError("User arguments cannot be None.")

    cleaned_arguments = [
        argument.strip()
        for argument in user_arguments
        if argument and argument.strip()
    ]

    if not cleaned_arguments:
        raise ValueError(
            "At least one user argument is required."
        )

    formatted_arguments = "\n\n".join(
        f"Round {index + 1}:\n{argument}"
        for index, argument in enumerate(cleaned_arguments)
    )

    return f"""
You are analyzing evidence usage and reasoning quality
in a debate.

Analyze ONLY the user's arguments.

Your task is to determine:

1. Evidence usage
2. Reasoning quality

Evidence means support for a claim through things such as:
- statistics
- research findings
- studies
- reports
- surveys
- factual data
- concrete examples
- clearly identified real-world evidence

Do NOT assume that a claim is evidence merely because
it sounds factual.

Reasoning means a logical connection between claims,
such as:
- explaining why something happens
- connecting cause and effect
- explaining consequences
- drawing a conclusion from supporting points
- connecting premises to a conclusion
- explaining how one claim supports another

Do NOT assume that an argument contains reasoning merely
because it contains words such as "because" or "therefore".

Important restrictions:

- Do NOT judge whether the user's position is correct.
- Do NOT judge whether the user's position is morally right or wrong.
- Do NOT judge whether the topic itself is politically desirable.
- Do NOT judge whether the user is persuasive overall.
- Do NOT invent evidence that is not present.
- Do NOT fact-check external claims.
- Analyze only what is present in the user's arguments.
- Distinguish between actual evidence and unsupported claims.
- Distinguish between actual reasoning and simple assertions.
- Mention relevant rounds when describing findings.

User arguments:

{formatted_arguments}

Return ONLY valid JSON with exactly this structure:

{{
    "evidence_quality": "string",
    "reasoning_quality": "string",
    "evidence_points": ["string"],
    "missing_evidence": ["string"],
    "reasoning_points": ["string"],
    "reasoning_gaps": ["string"]
}}

Requirements:

- "evidence_quality" should briefly summarize the quality
  and use of evidence across the user's arguments.
- "reasoning_quality" should briefly summarize the quality
  of the logical reasoning across the user's arguments.
- "evidence_points" should identify specific arguments or
  rounds where meaningful evidence was used.
- "missing_evidence" should identify claims that would
  benefit from supporting evidence.
- "reasoning_points" should identify specific examples of
  logical reasoning in the user's arguments.
- "reasoning_gaps" should identify places where claims are
  asserted without a clear logical connection.
- Keep every point concise and evidence-based.
- Do not invent contradictions, evidence, or reasoning.
""".strip()