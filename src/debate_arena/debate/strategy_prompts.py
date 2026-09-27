from debate_arena.debate.strategy import DebateStrategy


def build_strategy_prompt(
    context: str,
    latest_argument: str,
    analysis: dict | None = None,
) -> str:
    """Build a prompt for selecting the best debate strategy."""

    strategies = "\n".join(
        f"- {strategy.value}"
        for strategy in DebateStrategy
    )

    analysis_text = "No structured argument analysis available."

    if analysis:
        assumptions = analysis.get("assumptions", [])
        evidence = analysis.get("evidence", [])
        weaknesses = analysis.get("weaknesses", [])

        analysis_text = f"""
Claim:
{analysis.get("claim", "")}

Reasoning:
{analysis.get("reasoning", "")}

Assumptions:
{", ".join(assumptions) if assumptions else "None identified"}

Evidence:
{", ".join(evidence) if evidence else "None identified"}

Weaknesses:
{", ".join(weaknesses) if weaknesses else "None identified"}

Argument type:
{analysis.get("argument_type", "general")}
""".strip()

    return f"""
You are the strategic decision-maker for an AI debate opponent.

Your task is to choose the single most effective strategy for
responding to the user's latest argument.

Available strategies:

{strategies}

Rules:

- Choose exactly ONE strategy.
- Base the choice primarily on the structured argument analysis.
- Use the full debate context to understand the broader discussion.
- Focus on the latest user argument.
- Prefer a strategy that directly exploits the most relevant
  weakness, assumption, evidence gap, or reasoning issue.
- Do not invent evidence or facts.
- Do not provide an explanation.
- Return ONLY the strategy name.
- Use the exact strategy value from the list.

Structured argument analysis:

{analysis_text}

Full debate context:

{context}

Latest user argument:

{latest_argument}

Selected strategy:
""".strip()