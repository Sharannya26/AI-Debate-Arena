from dataclasses import dataclass, field


@dataclass
class ResponsivenessAnalysis:
    """
    Represents how directly the user's argument responds
    to the AI's previous argument.
    """

    responsiveness: str
    addressed_points: list[str] = field(default_factory=list)
    ignored_points: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.responsiveness.strip():
            raise ValueError("Responsiveness cannot be empty.")

        self.responsiveness = self.responsiveness.strip()

        self.addressed_points = [
            point.strip()
            for point in self.addressed_points
            if point and point.strip()
        ]

        self.ignored_points = [
            point.strip()
            for point in self.ignored_points
            if point and point.strip()
        ]