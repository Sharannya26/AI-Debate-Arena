import json

from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis


def build_cross_round_analysis_prompt(
    analysis: CrossRoundAnalysis,
) -> str:
    """
    Build the Gemini prompt for semantic interpretation of
    deterministic cross-round performance findings.

    Gemini interprets the supplied findings. It does not recalculate
    metrics or invent additional observations.
    """
    if analysis is None:
        raise ValueError("Cross-round analysis cannot be None.")

    analysis_data = {
        "overall_trajectory": analysis.overall_trajectory,
        "improvement_patterns": analysis.improvement_patterns,
        "decline_patterns": analysis.decline_patterns,
        "stable_patterns": analysis.stable_patterns,
        "recurring_patterns": analysis.recurring_patterns,
        "cross_dimension_patterns": analysis.cross_dimension_patterns,
        "key_insights": analysis.key_insights,
    }

    return f"""
You are an advanced debate-performance interpretation assistant.

Your task is to interpret structured cross-round performance findings
from a debate.

The cross-round findings have already been computed by deterministic
Python analysis.

DO NOT recalculate them.

Your job is to explain the meaning of the supplied patterns across
the available debate rounds.

Analyze:

1. Overall trajectory
   - Explain the overall performance trajectory using only the supplied
     information.

2. Improvement patterns
   - Interpret dimensions that improved across rounds.
   - Do not invent additional improvements.

3. Decline patterns
   - Interpret dimensions that declined across rounds.
   - Do not invent additional declines.

4. Stable patterns
   - Explain dimensions that remained stable.

5. Recurring patterns
   - Identify meaningful recurring characteristics that appeared
     across multiple rounds.

6. Cross-dimension patterns
   - Explain meaningful relationships between the supplied dimensions.
   - Only identify relationships supported by the supplied information.

7. Key insights
   - Produce concise insights that summarize the most important
     cross-round observations.

IMPORTANT RULES:

- Do NOT introduce numerical scores.
- Do NOT recalculate any metrics.
- Do NOT invent evidence, examples, statistics, events, or arguments.
- Do NOT fact-check the debate.
- Do NOT determine whether the user's position is factually correct.
- Do NOT determine whether the user's position is morally correct.
- Do NOT judge political positions.
- Do NOT make claims about personality, intelligence, mental state,
  character, or competence.
- Do NOT make unsupported causal claims.
- Do NOT assume information that is not present.
- Do NOT invent changes between rounds.
- Do NOT contradict the supplied deterministic findings without clear
  evidence in the supplied information.
- Focus only on observable debate-performance patterns.
- If the supplied information is insufficient for an interpretation,
  explicitly say that the information is insufficient rather than guessing.
- Every interpretation must be grounded in the supplied data.

Return ONLY valid JSON using exactly this structure:

{{
  "overall_interpretation": "string",
  "improvement_interpretation": "string",
  "decline_interpretation": "string",
  "stability_interpretation": "string",
  "recurring_interpretation": "string",
  "cross_dimension_interpretation": "string",
  "key_insights": ["string"]
}}

CROSS-ROUND PERFORMANCE FINDINGS:

{json.dumps(analysis_data, indent=2)}
""".strip()