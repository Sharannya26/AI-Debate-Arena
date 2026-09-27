from debate_arena.debate.actionable_coaching_recommendation import (
    ActionableCoachingRecommendation,
)
from debate_arena.debate.actionable_coaching_recommendation_analyzer import (
    ActionableCoachingRecommendationAnalyzer,
)
from debate_arena.debate.coaching_priority_analyzer import (
    CoachingPriorityAnalyzer,
)
from debate_arena.debate.coaching_profile import CoachingProfile
from debate_arena.debate.coaching_profile_analyzer import (
    CoachingProfileAnalyzer,
)
from debate_arena.debate.coaching_session_report import (
    CoachingSessionReport,
)
from debate_arena.debate.consistency_analysis import ConsistencyAnalysis
from debate_arena.debate.debate_performance import DebatePerformance
from debate_arena.debate.debate_performance_analyzer import (
    DebatePerformanceAnalyzer,
)
from debate_arena.debate.moment_analyzer import MomentAnalyzer
from debate_arena.debate.performance_dimension_aggregator import (
    PerformanceDimensionAggregator,
)
from debate_arena.debate.performance_interpretation_coordinator import (
    PerformanceInterpretationCoordinator,
)
from debate_arena.debate.performance_summary import PerformanceSummary
from debate_arena.debate.performance_summary_analyzer import (
    PerformanceSummaryAnalyzer,
)
from debate_arena.debate.round_performance import RoundPerformance
from debate_arena.debate.round_performance_aggregator import (
    RoundPerformanceAggregator,
)
from debate_arena.debate.semantic_performance_analysis import (
    SemanticPerformanceAnalysis,
)
from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis
from debate_arena.debate.cross_round_analysis_coordinator import (
    CrossRoundAnalysisCoordinator,
)
from debate_arena.debate.moment_analysis_coordinator import (
    MomentAnalysisCoordinator,
)
from debate_arena.debate.semantic_performance_analyzer import (
    SemanticPerformanceAnalyzer,
)
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)
from debate_arena.debate.personalized_improvement_priority_analyzer import (
    PersonalizedImprovementPriorityAnalyzer,
)
from debate_arena.debate.practice_exercise import PracticeExercise
from debate_arena.debate.practice_exercise_analyzer import (
    PracticeExerciseAnalyzer,
)


class DebatePerformancePipeline:
    """
    Orchestrates the complete post-debate performance pipeline.

    Round-level performance is derived from RoundPerformance objects.
    Debate-level consistency is supplied by the existing M9.3
    consistency analysis rather than being recalculated here.

    Semantic interpretation is delegated to the injected
    PerformanceInterpretationCoordinator.

    CoachingProfile is derived deterministically from the
    PerformanceSummary and does not call Gemini.

    Personalized improvement priorities are derived
    deterministically from the CoachingProfile and do not
    call Gemini.

    Actionable coaching recommendations are derived
    deterministically from personalized improvement priorities
    and do not call Gemini.

    Practice exercises are derived deterministically from
    personalized improvement priorities and do not call Gemini.

    CoachingSessionReport packages the complete coaching
    session into one reusable structured report.
    """

    def __init__(
        self,
        performance_analyzer=None,
        round_aggregator=None,
        dimension_aggregator=None,
        moment_analyzer=None,
        coaching_analyzer=None,
        coaching_profile_analyzer=None,
        personalized_improvement_priority_analyzer=None,
        actionable_coaching_recommendation_analyzer=None,
        practice_exercise_analyzer=None,
        summary_analyzer=None,
        interpretation_coordinator=None,
        cross_round_coordinator=None,
        moment_analysis_coordinator=None,
        llm_client=None,
    ):
        self.performance_analyzer = (
            performance_analyzer
            or DebatePerformanceAnalyzer()
        )

        self.round_aggregator = (
            round_aggregator
            or RoundPerformanceAggregator()
        )

        self.dimension_aggregator = (
            dimension_aggregator
            or PerformanceDimensionAggregator()
        )

        self.moment_analyzer = (
            moment_analyzer
            or MomentAnalyzer()
        )

        self.coaching_analyzer = (
            coaching_analyzer
            or CoachingPriorityAnalyzer()
        )

        self.coaching_profile_analyzer = (
            coaching_profile_analyzer
            or CoachingProfileAnalyzer()
        )

        self.personalized_improvement_priority_analyzer = (
            personalized_improvement_priority_analyzer
            or PersonalizedImprovementPriorityAnalyzer()
        )

        # M9.9.3 — Actionable coaching recommendations.
        self.actionable_coaching_recommendation_analyzer = (
            actionable_coaching_recommendation_analyzer
            or ActionableCoachingRecommendationAnalyzer()
        )

        # M9.9.4 — Practice exercises.
        self.practice_exercise_analyzer = (
            practice_exercise_analyzer
            or PracticeExerciseAnalyzer()
        )

        self.summary_analyzer = (
            summary_analyzer
            or PerformanceSummaryAnalyzer()
        )

        self.interpretation_coordinator = (
            interpretation_coordinator
            or PerformanceInterpretationCoordinator(
                semantic_analyzer=SemanticPerformanceAnalyzer(
                    llm_client=llm_client
                )
            )
        )

        self.cross_round_coordinator = (
            cross_round_coordinator
            or CrossRoundAnalysisCoordinator(
                llm_client=llm_client
            )
        )

        self.moment_analysis_coordinator = (
            moment_analysis_coordinator
            or MomentAnalysisCoordinator(
                llm_client=llm_client
            )
        )

        self.last_performance: DebatePerformance | None = None

        self.last_summary: PerformanceSummary | None = None

        self.last_interpretation = None

        self.last_cross_round_analysis: (
            CrossRoundAnalysis | None
        ) = None

        self.last_moment_analysis: (
            object | None
        ) = None

        self.last_coaching_profile: (
            CoachingProfile | None
        ) = None

        self.last_improvement_priorities: (
            list[PersonalizedImprovementPriority]
            | None
        ) = None

        # M9.9.3 — Cached actionable recommendations.
        self.last_coaching_recommendations: (
            list[ActionableCoachingRecommendation]
            | None
        ) = None

        # M9.9.4 — Cached practice exercises.
        self.last_practice_exercises: (
            list[PracticeExercise]
            | None
        ) = None

        # M9.9.6 — Cached complete coaching session report.
        self.last_coaching_session_report: (
            CoachingSessionReport | None
        ) = None

    def analyze(
        self,
        round_performances: list[RoundPerformance],
        consistency_analysis: ConsistencyAnalysis | None = None,
    ) -> SemanticPerformanceAnalysis:
        """
        Run the complete post-debate performance analysis pipeline.

        Args:
            round_performances:
                Round-level performance records.

            consistency_analysis:
                Existing debate-level consistency analysis from M9.3.
                It is optional so the pipeline can still operate when
                consistency has not yet been calculated.

        Returns:
            SemanticPerformanceAnalysis produced by the semantic
            interpretation layer.
        """

        if round_performances is None:
            raise ValueError(
                "Round performances cannot be None."
            )

        ordered_rounds = (
            self.round_aggregator.aggregate(
                round_performances
            )
        )

        if not ordered_rounds:
            raise ValueError(
                "At least one round performance is required."
            )

        dimension_summaries = (
            self.dimension_aggregator.aggregate_round_performances(
                ordered_rounds
            )
        )

        strongest_moments, weakest_moments = (
            self.moment_analyzer.analyze(
                ordered_rounds
            )
        )

        moment_analysis = (
            self.moment_analyzer.analyze_structured(
                ordered_rounds
            )
        )

        coaching_priorities = (
            self.coaching_analyzer.analyze(
                ordered_rounds
            )
        )

        consistency = ""

        if consistency_analysis is not None:
            consistency = (
                consistency_analysis.consistency
            )

        performance = (
            self.performance_analyzer.analyze(
                round_performances=ordered_rounds,
                argument_quality=(
                    dimension_summaries[
                        "argument quality"
                    ]
                ),
                communication_quality=(
                    dimension_summaries[
                        "communication quality"
                    ]
                ),
                responsiveness=(
                    dimension_summaries[
                        "responsiveness"
                    ]
                ),
                consistency=consistency,
                evidence_usage=(
                    dimension_summaries[
                        "evidence usage"
                    ]
                ),
                reasoning_quality=(
                    dimension_summaries[
                        "reasoning quality"
                    ]
                ),
                strongest_moments=strongest_moments,
                weakest_moments=weakest_moments,
                coaching_priorities=(
                    coaching_priorities
                ),
            )
        )

        summary = (
            self.summary_analyzer.analyze(
                performance,
                dimension_summaries=(
                    dimension_summaries
                ),
            )
        )

        # M9.9.1 — Build the deterministic
        # structured coaching profile.
        coaching_profile = (
            self.coaching_profile_analyzer.analyze(
                summary
            )
        )

        # M9.9.2 — Build deterministic
        # personalized improvement priorities.
        improvement_priorities = (
            self.personalized_improvement_priority_analyzer.analyze(
                coaching_profile
            )
        )

        # M9.9.3 — Build deterministic
        # actionable coaching recommendations.
        coaching_recommendations = (
            self.actionable_coaching_recommendation_analyzer.analyze(
                improvement_priorities
            )
        )

        # M9.9.4 — Build deterministic
        # practice exercises.
        practice_exercises = (
            self.practice_exercise_analyzer.analyze(
                improvement_priorities
            )
        )

        # M9.9.6 — Package all coaching artifacts
        # into one structured coaching session report.
        coaching_session_report = CoachingSessionReport(
            coaching_profile=coaching_profile,
            improvement_priorities=(
                improvement_priorities
            ),
            recommendations=(
                coaching_recommendations
            ),
            practice_exercises=(
                practice_exercises
            ),
            session_summary=(
                coaching_profile.overall_coaching_summary
            ),
        )

        interpretation = (
            self.interpretation_coordinator.analyze(
                summary
            )
        )

        cross_round_analysis = (
            self.cross_round_coordinator.analyze(
                ordered_rounds
            )
        )

        semantic_moment_analysis = (
            self.moment_analysis_coordinator.analyze(
                moment_analysis
            )
        )

        self.last_performance = performance

        self.last_summary = summary

        self.last_interpretation = interpretation

        self.last_cross_round_analysis = (
            cross_round_analysis
        )

        self.last_moment_analysis = (
            semantic_moment_analysis
        )

        self.last_coaching_profile = (
            coaching_profile
        )

        self.last_improvement_priorities = (
            improvement_priorities
        )

        self.last_coaching_recommendations = (
            coaching_recommendations
        )

        self.last_practice_exercises = (
            practice_exercises
        )

        self.last_coaching_session_report = (
            coaching_session_report
        )

        return interpretation