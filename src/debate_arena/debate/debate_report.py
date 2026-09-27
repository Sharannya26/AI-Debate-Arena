from dataclasses import dataclass, field

from debate_arena.debate.adaptive_mini_debate import (
    AdaptiveMiniDebate,
)
from debate_arena.debate.coaching_session_report import (
    CoachingSessionReport,
)
from debate_arena.debate.semantic_performance_analysis import (
    SemanticPerformanceAnalysis,
)
from debate_arena.debate.semantic_moment_analysis import (
    SemanticMomentAnalysis,
)


@dataclass
class DebateReport:
    """Final structured report for a completed debate."""

    topic: str

    user_position: str

    ai_position: str

    rounds_completed: int

    summary: str

    strongest_argument: str = ""

    weakest_argument: str = ""

    strengths: list[str] = field(
        default_factory=list
    )

    weaknesses: list[str] = field(
        default_factory=list
    )

    evidence_usage: str = ""

    consistency: str = ""

    responsiveness: str = ""

    recommendations: list[str] = field(
        default_factory=list
    )

    semantic_performance: (
        SemanticPerformanceAnalysis | None
    ) = None

    semantic_moments: (
        SemanticMomentAnalysis | None
    ) = None

    # M9.9.5 — Adaptive follow-up mini-debate.
    adaptive_mini_debate: (
        AdaptiveMiniDebate | None
    ) = None

    # M9.9.6 — Complete coaching session report.
    coaching_session_report: (
        CoachingSessionReport | None
    ) = None