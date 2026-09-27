import json

from debate_arena.debate.debate_performance import DebatePerformance
from debate_arena.debate.performance_summary import PerformanceSummary


def build_advanced_debate_analysis_prompt(
    performance: DebatePerformance,
    summary: PerformanceSummary,
) -> str:
    """
    Build the Gemini prompt for advanced semantic interpretation.

    Gemini receives already-computed performance information and is
    responsible only for interpreting meaningful patterns.
    """

    if performance is None:
        raise ValueError("Debate performance cannot be None.")

    if summary is None:
        raise ValueError("Performance summary cannot be None.")

    performance_data = {
        "round_performances": [
            {
                "round": item.round,
                "argument_quality": item.argument_quality,
                "communication_quality": item.communication_quality,
                "evidence_usage": item.evidence_usage,
                "reasoning_quality": item.reasoning_quality,
                "responsiveness": item.responsiveness,
            }
            for item in performance.round_performances
        ],
        "argument_quality": performance.argument_quality,
        "communication_quality": performance.communication_quality,
        "responsiveness": performance.responsiveness,
        "consistency": performance.consistency,
        "evidence_usage": performance.evidence_usage,
        "reasoning_quality": performance.reasoning_quality,
        "strongest_moments": performance.strongest_moments,
        "weakest_moments": performance.weakest_moments,
        "coaching_priorities": performance.coaching_priorities,
    }

    summary_data = {
        "overall_summary": summary.overall_summary,
        "dimension_summaries": summary.dimension_summaries,
        "strongest_moments": summary.strongest_moments,
        "weakest_moments": summary.weakest_moments,
        "coaching_priorities": summary.coaching_priorities,
    }

    return f"""
You are an advanced debate-performance interpretation assistant.

Your task is to interpret the structured debate-performance information
provided below.

The performance metrics and qualitative labels have already been computed
by deterministic Python analysis. Do NOT recalculate them.

Your job is to identify meaningful patterns and relationships across the
provided information.

Analyze:

1. Cross-dimension patterns
   - Identify meaningful relationships between dimensions such as:
     reasoning, evidence usage, responsiveness, communication, consistency,
     and argument quality.
   - Do not merely repeat the dimension labels.
   - Only identify relationships supported by the supplied data.

2. Round patterns
   - Identify meaningful changes, repeated patterns, or stable characteristics
     across the available rounds.
   - Do not invent changes that are not supported by the round data.

3. Strengths interpretation
   - Explain the strongest observable performance patterns.

4. Weaknesses interpretation
   - Explain recurring or meaningful areas for improvement.

5. Coaching interpretation
   - Translate the observed patterns into practical debate-training advice.
   - Recommendations must be grounded in the supplied performance information.

6. Key insights
   - Produce concise, useful observations that summarize the most important
     patterns.

IMPORTANT RULES:

- Do NOT introduce numerical scores.
- Do NOT recalculate metrics.
- Do NOT invent evidence, examples, statistics, or events.
- Do NOT fact-check the debate.
- Do NOT determine whether the user's position is factually or morally correct.
- Do NOT judge political positions.
- Do NOT make claims about personality, intelligence, mental state, or character.
- Do NOT make unsupported causal claims.
- Do NOT assume information that is not present in the supplied data.
- Do NOT contradict the supplied deterministic analysis without clear evidence
  in the provided data.
- Keep interpretations focused on observable debate performance.
- Every insight must be grounded in the supplied information.
- If the supplied information is insufficient for a conclusion, say so rather
  than guessing.

Return ONLY valid JSON using exactly this structure:

{{
  "overall_interpretation": "string",
  "cross_dimension_patterns": ["string"],
  "round_patterns": ["string"],
  "strengths_interpretation": "string",
  "weaknesses_interpretation": "string",
  "coaching_interpretation": "string",
  "key_insights": ["string"]
}}

DEBATE PERFORMANCE DATA:
{json.dumps(performance_data, indent=2)}

PERFORMANCE SUMMARY:
{json.dumps(summary_data, indent=2)}
""".strip()