import json

from debate_arena.debate.moment_analysis import MomentAnalysis


def build_moment_analysis_prompt(
    analysis: MomentAnalysis,
) -> str:
    """
    Build the Gemini prompt for semantic interpretation of
    deterministic strongest and weakest debate moments.

    Gemini interprets the supplied findings. It does not
    recalculate metrics or invent observations.
    """

    if analysis is None:
        raise ValueError(
            "Moment analysis cannot be None."
        )

    analysis_data = {
        "strongest_moments": analysis.strongest_moments,
        "weakest_moments": analysis.weakest_moments,
        "key_insights": analysis.key_insights,
    }

    return f"""
You are an advanced debate-performance interpretation assistant.

Your task is to interpret structured strongest and weakest moments
identified from a debate.

The strongest and weakest moments have already been identified by
deterministic Python analysis.

DO NOT recalculate the findings.

Your job is to explain the meaning of the supplied moments using
only the information provided.

Analyze:

1. Strongest moments
   - Explain what makes the supplied strongest moments notable.
   - Refer only to the dimensions and observations present in the data.
   - Do not invent additional strengths.

2. Weakest moments
   - Explain what makes the supplied weakest moments notable.
   - Identify practical areas for improvement based only on the supplied data.
   - Do not invent additional weaknesses.

3. Key insights
   - Produce concise and useful observations that summarize the
     most important patterns in the supplied moments.
   - Insights should help the user understand what to preserve
     and what to improve in future debates.

IMPORTANT RULES:

- Do NOT introduce numerical scores.
- Do NOT recalculate any metrics.
- Do NOT invent arguments, examples, evidence, statistics, events,
  or debate content.
- Do NOT fact-check the debate.
- Do NOT determine whether the user's position is factually correct.
- Do NOT determine whether the user's position is morally correct.
- Do NOT judge political positions.
- Do NOT make claims about personality, intelligence, mental state,
  character, or competence.
- Do NOT make unsupported causal claims.
- Do NOT assume information that is not present.
- Do NOT contradict the supplied deterministic findings without
  clear evidence in the supplied information.
- Focus only on observable debate-performance patterns.
- Every interpretation must be grounded in the supplied data.
- If the supplied information is insufficient for an interpretation,
  explicitly say that the information is insufficient rather than guessing.
- Keep the interpretation concise and useful for a post-debate coaching report.

Return ONLY valid JSON using exactly this structure:

{{
  "strongest_interpretation": "string",
  "weakest_interpretation": "string",
  "key_insights": ["string"]
}}

STRONGEST AND WEAKEST MOMENT FINDINGS:

{json.dumps(analysis_data, indent=2)}
""".strip()