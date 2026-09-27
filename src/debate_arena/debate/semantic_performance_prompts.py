from debate_arena.debate.performance_summary import (
    PerformanceSummary,
)


def build_semantic_performance_prompt(
    summary: PerformanceSummary,
) -> str:
    if summary is None:
        raise ValueError(
            "Performance summary cannot be None."
        )

    dimension_text = "\n".join(
        f"- {dimension}: {value}"
        for dimension, value
        in summary.dimension_summaries.items()
    )

    strongest_text = "\n".join(
        f"- {moment}"
        for moment in summary.strongest_moments
    )

    weakest_text = "\n".join(
        f"- {moment}"
        for moment in summary.weakest_moments
    )

    coaching_text = "\n".join(
        f"- {priority}"
        for priority in summary.coaching_priorities
    )

    return f"""
You are analyzing a user's performance in an AI debate.

Your task is to provide a semantic interpretation of
already-computed debate performance information.

Do NOT invent new evidence.

Do NOT fact-check the debate topic.

Do NOT judge whether the user's position is:
- politically correct or incorrect
- morally right or wrong
- socially desirable or undesirable

Do NOT make assumptions about the user's personality,
intelligence, or mental state.

Focus ONLY on the user's debate performance.

Interpret the relationships between:
- performance dimensions
- strongest moments
- weakest moments
- coaching priorities

Explain what the combination of these signals suggests
about the user's debate performance.

Performance summary:

Overall summary:
{summary.overall_summary}

Dimension summaries:
{dimension_text or "No dimension summaries available."}

Strongest moments:
{strongest_text or "No strongest moments identified."}

Weakest moments:
{weakest_text or "No weakest moments identified."}

Coaching priorities:
{coaching_text or "No coaching priorities identified."}

Return ONLY valid JSON with exactly this structure:

{{
    "overall_interpretation": "string",
    "strengths_interpretation": "string",
    "weaknesses_interpretation": "string",
    "coaching_interpretation": "string",
    "key_insights": ["string"]
}}

Requirements:

- Keep the interpretation concise and evidence-based.
- Base every insight on the supplied performance data.
- Connect related dimensions when appropriate.
- Explain meaningful patterns across the debate.
- Do not invent specific arguments or events.
- Do NOT introduce numerical scores.
- Do not claim that one performance dimension causes another.
- Keep "key_insights" focused on the most useful observations.
""".strip()