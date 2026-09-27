from dataclasses import dataclass, field


@dataclass
class MomentAnalysis:
    """
    Structured analysis of the strongest and weakest moments
    observed during a debate.

    The model stores qualitative observations only.
    It does not contain numerical performance scores.
    """

    strongest_moments: list[str] = field(default_factory=list)
    weakest_moments: list[str] = field(default_factory=list)
    key_insights: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.strongest_moments = [
            moment.strip()
            for moment in self.strongest_moments
            if moment and moment.strip()
        ]

        self.weakest_moments = [
            moment.strip()
            for moment in self.weakest_moments
            if moment and moment.strip()
        ]

        self.key_insights = [
            insight.strip()
            for insight in self.key_insights
            if insight and insight.strip()
        ]