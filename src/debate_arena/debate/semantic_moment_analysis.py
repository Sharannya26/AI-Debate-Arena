from dataclasses import dataclass, field


@dataclass
class SemanticMomentAnalysis:
    """
    Semantic interpretation of the strongest and weakest
    moments identified during a debate.

    This model contains qualitative interpretations only.
    It does not contain numerical scores.
    """

    strongest_interpretation: str
    weakest_interpretation: str
    key_insights: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.strongest_interpretation.strip():
            raise ValueError(
                "Strongest interpretation cannot be empty."
            )

        if not self.weakest_interpretation.strip():
            raise ValueError(
                "Weakest interpretation cannot be empty."
            )

        self.strongest_interpretation = (
            self.strongest_interpretation.strip()
        )

        self.weakest_interpretation = (
            self.weakest_interpretation.strip()
        )

        self.key_insights = [
            insight.strip()
            for insight in self.key_insights
            if insight and insight.strip()
        ]