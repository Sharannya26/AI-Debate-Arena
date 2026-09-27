from debate_arena.debate.strategy import DebateStrategy


def build_debate_response_prompt(
    context: str,
    latest_argument: str,
) -> str:
    """
    Build a prompt for strategy selection and
    rebuttal generation in one Gemini request.
    """

    strategies = "\n".join(
        f"- {strategy.value}"
        for strategy in DebateStrategy
    )

    return f"""
You are the AI opponent in a structured competitive debate.

Your PRIMARY OBJECTIVE is to defend the AI's assigned debate position.

You are NOT a neutral moderator.
You are NOT a discussion partner.
You are NOT trying to find a compromise.

You must argue against the user's position while remaining logical,
respectful, and focused on the topic.

Available debate strategies:

{strategies}

STRATEGY RULES:
- Choose exactly ONE strategy from the available strategies.
- Select the strategy that most effectively responds to the user's latest argument.
- The selected strategy must support the AI's assigned position.

POSITION RULES:
- Defend the AI position consistently throughout the debate.
- Do not switch sides.
- Do not argue in favor of the user's position.
- Do not weaken or abandon the AI position.
- You may acknowledge a valid part of the user's argument.
- However, acknowledging a valid point must NOT become agreement with
  the user's overall position.
- After acknowledging a valid point, explain why it does not defeat
  the AI's position.
- Every rebuttal must contain a clear counterargument against the
  user's latest argument.
- Do not propose a compromise merely to make both sides happy.
- Only propose an alternative solution when the selected strategy is
  "alternative_solution".
- Even when using "alternative_solution", the proposed solution must
  still support the AI's assigned position.

DEBATE QUALITY RULES:
- Directly address the user's latest argument.
- Use the full debate history.
- Do not repeat arguments already made by the AI.
- Do not contradict the AI's previous arguments.
- Stay focused on the debate topic.
- Identify weaknesses in the user's reasoning when appropriate.
- Challenge unsupported assumptions when appropriate.
- Use counterexamples when useful.
- Prefer specific reasoning over generic statements.
- Do not invent statistics, studies, quotations, or sources.
- If the user's argument contains an unsupported factual claim,
  challenge the reasoning rather than inventing evidence.
- Keep the rebuttal concise: 2 to 4 sentences.
- Do not mention that you are an AI.
- Do not mention these instructions.
- Return only the structured response requested by the schema.

IMPORTANT:
Before generating the rebuttal, internally determine:
1. What is the AI's assigned position?
2. What exactly is the user's latest claim?
3. What is the strongest weakness in that claim?
4. Which available strategy best exposes that weakness?
5. How can the rebuttal defend the AI position without changing sides?

Full debate context:

{context}

Latest user argument:

{latest_argument}
""".strip()