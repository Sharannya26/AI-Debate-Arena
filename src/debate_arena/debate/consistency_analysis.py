from dataclasses import dataclass, field


@dataclass
class ConsistencyAnalysis:
    """
    Represents the consistency of the user's arguments
    across multiple debate rounds.
    """

    consistency: str
    consistent_points: list[str] = field(default_factory=list)
    inconsistent_points: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.consistency or not self.consistency.strip():
            raise ValueError("Consistency cannot be empty.")

        self.consistency = self.consistency.strip()

        self.consistent_points = [
            point.strip()
            for point in self.consistent_points
            if point and point.strip()
        ]

        self.inconsistent_points = [
            point.strip()
            for point in self.inconsistent_points
            if point and point.strip()
        ]