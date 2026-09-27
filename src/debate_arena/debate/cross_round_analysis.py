from dataclasses import dataclass, field


@dataclass
class CrossRoundAnalysis:
    """
    Structured analysis of performance patterns across debate rounds.

    This model stores observations about how performance changed,
    remained stable, or repeated across rounds.

    It does not contain numerical scores.
    """

    overall_trajectory: str
    improvement_patterns: list[str] = field(default_factory=list)
    decline_patterns: list[str] = field(default_factory=list)
    stable_patterns: list[str] = field(default_factory=list)
    recurring_patterns: list[str] = field(default_factory=list)
    cross_dimension_patterns: list[str] = field(default_factory=list)
    key_insights: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.overall_trajectory.strip():
            raise ValueError("Overall trajectory cannot be empty.")

        self.overall_trajectory = self.overall_trajectory.strip()

        self.improvement_patterns = [
            pattern.strip()
            for pattern in self.improvement_patterns
            if pattern and pattern.strip()
        ]

        self.decline_patterns = [
            pattern.strip()
            for pattern in self.decline_patterns
            if pattern and pattern.strip()
        ]

        self.stable_patterns = [
            pattern.strip()
            for pattern in self.stable_patterns
            if pattern and pattern.strip()
        ]

        self.recurring_patterns = [
            pattern.strip()
            for pattern in self.recurring_patterns
            if pattern and pattern.strip()
        ]

        self.cross_dimension_patterns = [
            pattern.strip()
            for pattern in self.cross_dimension_patterns
            if pattern and pattern.strip()
        ]

        self.key_insights = [
            insight.strip()
            for insight in self.key_insights
            if insight and insight.strip()
        ]