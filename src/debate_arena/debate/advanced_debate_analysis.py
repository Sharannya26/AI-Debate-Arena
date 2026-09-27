from dataclasses import dataclass, field


@dataclass
class AdvancedDebateAnalysis:
    """
    Structured semantic interpretation of debate performance.

    This model contains interpretations derived from already-computed
    performance data. It does not contain raw metrics or numerical scores.
    """

    overall_interpretation: str

    cross_dimension_patterns: list[str] = field(default_factory=list)
    round_patterns: list[str] = field(default_factory=list)

    strengths_interpretation: str = ""
    weaknesses_interpretation: str = ""
    coaching_interpretation: str = ""

    key_insights: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.overall_interpretation.strip():
            raise ValueError("Overall interpretation cannot be empty.")

        self.overall_interpretation = self.overall_interpretation.strip()

        self.cross_dimension_patterns = [
            pattern.strip()
            for pattern in self.cross_dimension_patterns
            if pattern and pattern.strip()
        ]

        self.round_patterns = [
            pattern.strip()
            for pattern in self.round_patterns
            if pattern and pattern.strip()
        ]

        self.strengths_interpretation = (
            self.strengths_interpretation.strip()
        )

        self.weaknesses_interpretation = (
            self.weaknesses_interpretation.strip()
        )

        self.coaching_interpretation = (
            self.coaching_interpretation.strip()
        )

        self.key_insights = [
            insight.strip()
            for insight in self.key_insights
            if insight and insight.strip()
        ]