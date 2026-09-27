from dataclasses import dataclass, field


@dataclass
class FillerMetrics:
    """
    Stores objective filler-word measurements for one speech sample.
    """

    total_filler_count: int = 0
    filler_counts: dict[str, int] = field(default_factory=dict)
    total_word_count: int = 0
    filler_rate: float = 0.0

    def __post_init__(self) -> None:
        if self.total_filler_count < 0:
            raise ValueError(
                "Total filler count cannot be negative."
            )

        if self.total_word_count < 0:
            raise ValueError(
                "Total word count cannot be negative."
            )

        if self.filler_rate < 0:
            raise ValueError(
                "Filler rate cannot be negative."
            )

        for filler, count in self.filler_counts.items():
            if not filler or not filler.strip():
                raise ValueError(
                    "Filler word cannot be empty."
                )

            if count < 0:
                raise ValueError(
                    "Filler count cannot be negative."
                )

        calculated_total = sum(self.filler_counts.values())

        if self.total_filler_count != calculated_total:
            raise ValueError(
                "Total filler count must match filler counts."
            )

        if self.total_filler_count > self.total_word_count:
            raise ValueError(
                "Total filler count cannot exceed total word count."
            )

        expected_rate = (
            self.total_filler_count / self.total_word_count
            if self.total_word_count > 0
            else 0.0
        )

        if abs(self.filler_rate - expected_rate) > 1e-9:
            raise ValueError(
                "Filler rate must match filler count and word count."
            )

        self.filler_counts = {
            filler.strip().lower(): count
            for filler, count in self.filler_counts.items()
        }