from dataclasses import dataclass, field


@dataclass
class CoachingProfile:
    """
    Structured coaching profile derived from a completed debate.

    This model organizes existing debate-performance findings
    into information that later coaching features can consume.

    It does not perform analysis and does not call Gemini.
    """

    strengths: list[str] = field(default_factory=list)
    improvement_areas: list[str] = field(default_factory=list)
    coaching_priorities: list[str] = field(default_factory=list)
    strongest_moments: list[str] = field(default_factory=list)
    weakest_moments: list[str] = field(default_factory=list)
    overall_coaching_summary: str = ""

    def __post_init__(self) -> None:
        self.strengths = self._clean_list(self.strengths)
        self.improvement_areas = self._clean_list(
            self.improvement_areas
        )
        self.coaching_priorities = self._clean_list(
            self.coaching_priorities
        )
        self.strongest_moments = self._clean_list(
            self.strongest_moments
        )
        self.weakest_moments = self._clean_list(
            self.weakest_moments
        )
        self.overall_coaching_summary = (
            self.overall_coaching_summary.strip()
        )

    @staticmethod
    def _clean_list(values: list[str]) -> list[str]:
        return [
            value.strip()
            for value in values
            if value and value.strip()
        ]