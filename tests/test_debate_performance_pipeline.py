from debate_arena.debate.debate_performance_pipeline import (
    DebatePerformancePipeline,
)
from debate_arena.debate.round_performance import RoundPerformance
from debate_arena.debate.semantic_performance_analysis import (
    SemanticPerformanceAnalysis,
)
from debate_arena.debate.consistency_analysis import ConsistencyAnalysis
from debate_arena.debate.cross_round_analysis import CrossRoundAnalysis
from debate_arena.debate.moment_analysis import MomentAnalysis
from debate_arena.debate.semantic_moment_analysis import (
    SemanticMomentAnalysis,
)
from debate_arena.debate.coaching_profile import CoachingProfile
from debate_arena.debate.coaching_profile_analyzer import (
    CoachingProfileAnalyzer,
)
from unittest.mock import Mock
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)
from debate_arena.debate.actionable_coaching_recommendation import (
    ActionableCoachingRecommendation,
)
from debate_arena.debate.practice_exercise import (
    PracticeExercise,
)
class FakeInterpretationCoordinator:
    def __init__(self):
        self.last_analysis = None

    def analyze(self, summary):
        result = SemanticPerformanceAnalysis(
            overall_interpretation="Test semantic interpretation.",
            strengths_interpretation="Strong areas were identified.",
            weaknesses_interpretation="Some areas can be improved.",
            coaching_interpretation="Continue developing argument structure.",
            key_insights=["Insight from fake semantic analysis."],
        )

        self.last_analysis = result
        return result

class FakeCrossRoundCoordinator:
    def __init__(self):
        self.last_analysis = None

    def analyze(self, round_performances):
        result = CrossRoundAnalysis(
            overall_trajectory="Performance improved across rounds.",
            improvement_patterns=[
                "Argument quality improved across rounds."
            ],
            decline_patterns=[],
            stable_patterns=[],
            recurring_patterns=[],
            cross_dimension_patterns=[
                "Clear communication accompanied stronger arguments."
            ],
            key_insights=[
                "Performance improved across the debate."
            ],
        )

        self.last_analysis = result
        return result

class FakeMomentAnalysisCoordinator:
    def __init__(self):
        self.last_analysis = None
        self.received_analysis = None

    def analyze(self, analysis):
        self.received_analysis = analysis

        result = SemanticMomentAnalysis(
            strongest_interpretation=(
                "The strongest moments were supported by "
                "clear performance across the supplied dimensions."
            ),
            weakest_interpretation=(
                "The weakest moments indicate areas "
                "where performance can be improved."
            ),
            key_insights=[
                "Strong moments should be preserved.",
                "Weak moments provide useful coaching opportunities.",
            ],
        )

        self.last_analysis = result
        return result


def create_round_performances():
    return [
        RoundPerformance(
            round=1,
            argument_quality="Moderate",
            communication_quality="Limited",
            evidence_usage="Limited",
            reasoning_quality="Moderate",
            responsiveness="Partially responsive",
        ),
        RoundPerformance(
            round=2,
            argument_quality="Strong",
            communication_quality="Moderate",
            evidence_usage="Moderate",
            reasoning_quality="Strong",
            responsiveness="Highly responsive",
        ),
        RoundPerformance(
            round=3,
            argument_quality="Excellent",
            communication_quality="Strong",
            evidence_usage="Strong",
            reasoning_quality="Excellent",
            responsiveness="Highly responsive",
        ),
    ]


def create_test_pipeline(
    interpretation_coordinator=None,
    cross_round_coordinator=None,
    moment_analysis_coordinator=None,
):
    return DebatePerformancePipeline(
        interpretation_coordinator=(
            interpretation_coordinator
            or FakeInterpretationCoordinator()
        ),
        cross_round_coordinator=(
            cross_round_coordinator
            or FakeCrossRoundCoordinator()
        ),
        moment_analysis_coordinator=(
            moment_analysis_coordinator
            or FakeMomentAnalysisCoordinator()
        ),
    )


def test_pipeline_returns_semantic_performance_analysis():
    pipeline = create_test_pipeline()

    round_performances = create_round_performances()

    result = pipeline.analyze(
        round_performances=round_performances
    )

    assert isinstance(
        result,
        SemanticPerformanceAnalysis,
    )


def test_pipeline_stores_performance():
    pipeline = create_test_pipeline()

    round_performances = create_round_performances()

    pipeline.analyze(
        round_performances=round_performances
    )

    assert pipeline.last_performance is not None


def test_pipeline_stores_summary():
    pipeline = create_test_pipeline()

    round_performances = create_round_performances()

    pipeline.analyze(
        round_performances=round_performances
    )

    assert pipeline.last_summary is not None


def test_pipeline_stores_interpretation():
    pipeline = create_test_pipeline()

    round_performances = create_round_performances()

    pipeline.analyze(
        round_performances=round_performances
    )

    assert pipeline.last_interpretation is not None


def test_pipeline_uses_consistency_analysis():
    pipeline = create_test_pipeline()

    round_performances = create_round_performances()

    consistency_analysis = ConsistencyAnalysis(
        consistency="Mostly consistent.",
        consistent_points=[
            "Maintained the same position across rounds."
        ],
        inconsistent_points=[],
    )

    pipeline.analyze(
        round_performances=round_performances,
        consistency_analysis=consistency_analysis,
    )

    assert pipeline.last_performance.consistency == (
        "Mostly consistent."
    )


def test_pipeline_handles_missing_consistency_analysis():
    pipeline = create_test_pipeline()

    round_performances = create_round_performances()

    result = pipeline.analyze(
        round_performances=round_performances
    )

    assert result is not None
    assert pipeline.last_performance is not None


def test_pipeline_orders_rounds_before_analysis():
    pipeline = create_test_pipeline()

    round_performances = [
        RoundPerformance(
            round=3,
            argument_quality="Strong",
            communication_quality="Strong",
            evidence_usage="Strong",
            reasoning_quality="Strong",
            responsiveness="Highly responsive",
        ),
        RoundPerformance(
            round=1,
            argument_quality="Limited",
            communication_quality="Limited",
            evidence_usage="Limited",
            reasoning_quality="Limited",
            responsiveness="Partially responsive",
        ),
        RoundPerformance(
            round=2,
            argument_quality="Moderate",
            communication_quality="Moderate",
            evidence_usage="Moderate",
            reasoning_quality="Moderate",
            responsiveness="Partially responsive",
        ),
    ]

    pipeline.analyze(
        round_performances=round_performances
    )

    ordered_rounds = pipeline.last_performance.round_performances

    assert [item.round for item in ordered_rounds] == [
        1,
        2,
        3,
    ]


def test_pipeline_generates_cross_round_analysis():
    pipeline = create_test_pipeline()

    round_performances = create_round_performances()

    pipeline.analyze(
        round_performances=round_performances
    )

    assert pipeline.last_cross_round_analysis is not None


def test_pipeline_cross_round_analysis_is_correct_type():
    pipeline = create_test_pipeline()

    round_performances = create_round_performances()

    pipeline.analyze(
        round_performances=round_performances
    )

    assert isinstance(
        pipeline.last_cross_round_analysis,
        CrossRoundAnalysis,
    )


def test_pipeline_rejects_none_round_performances():
    pipeline = create_test_pipeline()

    try:
        pipeline.analyze(
            round_performances=None
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Round performances cannot be None."
        )


def test_pipeline_rejects_empty_round_performances():
    pipeline = create_test_pipeline()

    try:
        pipeline.analyze(
            round_performances=[]
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "At least one round performance is required."
        )


def test_pipeline_integrates_semantic_moment_analysis():
    moment_coordinator = FakeMomentAnalysisCoordinator()

    pipeline = create_test_pipeline(
        moment_analysis_coordinator=moment_coordinator
    )

    round_performances = create_round_performances()

    result = pipeline.analyze(
        round_performances=round_performances
    )

    assert result is not None

    assert moment_coordinator.last_analysis is not None

    assert isinstance(
        moment_coordinator.last_analysis,
        SemanticMomentAnalysis,
    )

    assert pipeline.last_moment_analysis is not None

    assert isinstance(
        pipeline.last_moment_analysis,
        SemanticMomentAnalysis,
    )


def test_pipeline_passes_structured_moment_analysis_to_coordinator():
    moment_coordinator = FakeMomentAnalysisCoordinator()

    pipeline = create_test_pipeline(
        moment_analysis_coordinator=moment_coordinator
    )

    round_performances = create_round_performances()

    pipeline.analyze(
        round_performances=round_performances
    )

    moment_analysis = moment_coordinator.received_analysis

    assert moment_analysis is not None

    assert isinstance(
        moment_analysis,
        MomentAnalysis,
    )

    assert moment_analysis.strongest_moments

    assert moment_analysis.weakest_moments

def test_pipeline_builds_and_stores_coaching_profile():
    coaching_profile_analyzer = Mock()

    coaching_profile = CoachingProfile(
        strengths=["Argument quality improved."],
        improvement_areas=["Evidence usage declined."],
        coaching_priorities=[
            "Use stronger supporting evidence."
        ],
        strongest_moments=["Strong rebuttal."],
        weakest_moments=["Unsupported claim."],
        overall_coaching_summary=(
            "Focus on evidence usage."
        ),
    )

    coaching_profile_analyzer.analyze.return_value = (
        coaching_profile
    )

    pipeline = DebatePerformancePipeline(
        coaching_profile_analyzer=(
            coaching_profile_analyzer
        ),
        interpretation_coordinator=FakeInterpretationCoordinator(),
        cross_round_coordinator=FakeCrossRoundCoordinator(),
        moment_analysis_coordinator=FakeMomentAnalysisCoordinator(),
    )

    result = pipeline.analyze(
        [
            RoundPerformance(
                round=1,
                argument_quality="Strong",
                communication_quality="Clear",
                evidence_usage="Limited",
                reasoning_quality="Strong",
                responsiveness="Responsive",
            )
        ]
    )

    assert result is not None
    assert pipeline.last_coaching_profile == (
        coaching_profile
    )

    coaching_profile_analyzer.analyze.assert_called_once_with(
        pipeline.last_summary
    )


def test_pipeline_exposes_coaching_profile_without_changing_semantic_result():
    coaching_profile_analyzer = Mock()

    coaching_profile = CoachingProfile(
        strengths=["Clear reasoning."],
        improvement_areas=[],
        coaching_priorities=[],
        strongest_moments=[],
        weakest_moments=[],
        overall_coaching_summary=(
            "Maintain the identified strengths."
        ),
    )

    coaching_profile_analyzer.analyze.return_value = (
        coaching_profile
    )

    pipeline = DebatePerformancePipeline(
        coaching_profile_analyzer=(
            coaching_profile_analyzer
        ),
        interpretation_coordinator=FakeInterpretationCoordinator(),
        cross_round_coordinator=FakeCrossRoundCoordinator(),
        moment_analysis_coordinator=FakeMomentAnalysisCoordinator(),
    )

    result = pipeline.analyze(
        [
            RoundPerformance(
                round=1,
                argument_quality="Strong",
                communication_quality="Clear",
                evidence_usage="Good",
                reasoning_quality="Strong",
                responsiveness="Responsive",
            )
        ]
    )

    assert result.overall_interpretation == (
        "Test semantic interpretation."
    )

    assert pipeline.last_coaching_profile is (
        coaching_profile
    )

def test_pipeline_builds_and_stores_improvement_priorities():
    improvement_priority_analyzer = Mock()

    improvement_priority = PersonalizedImprovementPriority(
        priority="Improve evidence usage",
        reason="Evidence usage needs improvement.",
        focus_area="Support claims with concrete evidence.",
        supporting_evidence=[
            "Evidence usage declined across rounds.",
        ],
    )

    improvement_priority_analyzer.analyze.return_value = [
        improvement_priority
    ]

    pipeline = DebatePerformancePipeline(
        personalized_improvement_priority_analyzer=(
            improvement_priority_analyzer
        ),
        interpretation_coordinator=(
            FakeInterpretationCoordinator()
        ),
        cross_round_coordinator=(
            FakeCrossRoundCoordinator()
        ),
        moment_analysis_coordinator=(
            FakeMomentAnalysisCoordinator()
        ),
    )

    result = pipeline.analyze(
        [
            RoundPerformance(
                round=1,
                argument_quality="Strong",
                communication_quality="Clear",
                evidence_usage="Limited",
                reasoning_quality="Strong",
                responsiveness="Responsive",
            )
        ]
    )

    assert result is not None

    assert pipeline.last_improvement_priorities == [
        improvement_priority
    ]

    improvement_priority_analyzer.analyze.assert_called_once_with(
        pipeline.last_coaching_profile
    )


def test_pipeline_exposes_improvement_priorities_without_changing_semantic_result():
    improvement_priority_analyzer = Mock()

    improvement_priority = PersonalizedImprovementPriority(
        priority="Improve reasoning quality",
        reason="Reasoning needs improvement.",
        focus_area="Make logical connections clearer.",
        supporting_evidence=[
            "Logical connections varied across rounds.",
        ],
    )

    improvement_priority_analyzer.analyze.return_value = [
        improvement_priority
    ]

    pipeline = DebatePerformancePipeline(
        personalized_improvement_priority_analyzer=(
            improvement_priority_analyzer
        ),
        interpretation_coordinator=(
            FakeInterpretationCoordinator()
        ),
        cross_round_coordinator=(
            FakeCrossRoundCoordinator()
        ),
        moment_analysis_coordinator=(
            FakeMomentAnalysisCoordinator()
        ),
    )

    result = pipeline.analyze(
        [
            RoundPerformance(
                round=1,
                argument_quality="Strong",
                communication_quality="Clear",
                evidence_usage="Good",
                reasoning_quality="Strong",
                responsiveness="Responsive",
            )
        ]
    )

    assert result.overall_interpretation == (
        "Test semantic interpretation."
    )

    assert pipeline.last_improvement_priorities == [
        improvement_priority
    ]

def test_pipeline_builds_and_stores_coaching_recommendations():
    pipeline = DebatePerformancePipeline(
        interpretation_coordinator=FakeInterpretationCoordinator(),
        cross_round_coordinator=FakeCrossRoundCoordinator(),
        moment_analysis_coordinator=FakeMomentAnalysisCoordinator(),
    )

    round_performances = [
        RoundPerformance(
            round=1,
            argument_quality="Strong",
            communication_quality="Strong",
            evidence_usage="Strong",
            reasoning_quality="Strong",
            responsiveness="Strong",
        ),
        RoundPerformance(
            round=2,
            argument_quality="Strong",
            communication_quality="Strong",
            evidence_usage="Weak",
            reasoning_quality="Strong",
            responsiveness="Strong",
        ),
    ]

    pipeline.analyze(round_performances)

    assert pipeline.last_coaching_recommendations is not None
    assert pipeline.last_coaching_recommendations

    recommendation = (
        pipeline.last_coaching_recommendations[0]
    )

    assert isinstance(
        recommendation,
        ActionableCoachingRecommendation,
    )

    assert recommendation.recommendation
    assert recommendation.reason
    assert recommendation.action
    assert recommendation.related_priority


def test_pipeline_exposes_coaching_recommendations_without_changing_semantic_result():
    pipeline = DebatePerformancePipeline(
        interpretation_coordinator=FakeInterpretationCoordinator(),
        cross_round_coordinator=FakeCrossRoundCoordinator(),
        moment_analysis_coordinator=FakeMomentAnalysisCoordinator(),
    )

    round_performances = [
        RoundPerformance(
            round=1,
            argument_quality="Strong",
            communication_quality="Strong",
            evidence_usage="Strong",
            reasoning_quality="Strong",
            responsiveness="Strong",
        ),
        RoundPerformance(
            round=2,
            argument_quality="Strong",
            communication_quality="Strong",
            evidence_usage="Weak",
            reasoning_quality="Strong",
            responsiveness="Strong",
        ),
    ]

    result = pipeline.analyze(round_performances)

    assert result is pipeline.last_interpretation
    assert result.overall_interpretation

    assert pipeline.last_coaching_recommendations is not None
    assert len(
        pipeline.last_coaching_recommendations
    ) >= 1

def test_pipeline_generates_practice_exercises():
    pipeline = DebatePerformancePipeline(
        interpretation_coordinator=FakeInterpretationCoordinator(),
        cross_round_coordinator=FakeCrossRoundCoordinator(),
        moment_analysis_coordinator=FakeMomentAnalysisCoordinator(),
    )

    round_performances = [
        RoundPerformance(
            round=1,
            argument_quality="Strong",
            communication_quality="Strong",
            responsiveness="Strong",
            evidence_usage="Strong",
            reasoning_quality="Strong",
        ),
        RoundPerformance(
            round=2,
            argument_quality="Strong",
            communication_quality="Strong",
            responsiveness="Strong",
            evidence_usage="Weak",
            reasoning_quality="Strong",
        ),
    ]

    pipeline.analyze(round_performances)

    assert pipeline.last_practice_exercises is not None
    assert len(pipeline.last_practice_exercises) >= 1

    assert all(
        isinstance(
            exercise,
            PracticeExercise,
        )
        for exercise in pipeline.last_practice_exercises
    )


def test_pipeline_practice_exercises_are_related_to_improvement_priorities():
    pipeline = DebatePerformancePipeline(
        interpretation_coordinator=FakeInterpretationCoordinator(),
        cross_round_coordinator=FakeCrossRoundCoordinator(),
        moment_analysis_coordinator=FakeMomentAnalysisCoordinator(),
    )

    round_performances = [
        RoundPerformance(
            round=1,
            argument_quality="Strong",
            communication_quality="Strong",
            responsiveness="Strong",
            evidence_usage="Strong",
            reasoning_quality="Strong",
        ),
        RoundPerformance(
            round=2,
            argument_quality="Strong",
            communication_quality="Strong",
            responsiveness="Strong",
            evidence_usage="Weak",
            reasoning_quality="Strong",
        ),
    ]

    pipeline.analyze(round_performances)

    priorities = pipeline.last_improvement_priorities
    exercises = pipeline.last_practice_exercises

    assert priorities is not None
    assert exercises is not None
    assert len(exercises) == len(priorities)

    priority_titles = {
        priority.priority
        for priority in priorities
    }

    assert all(
        exercise.related_priority in priority_titles
        for exercise in exercises
    )