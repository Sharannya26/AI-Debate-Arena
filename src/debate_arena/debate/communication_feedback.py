from dataclasses import dataclass


@dataclass
class CommunicationFeedback:
    """
    Qualitative interpretation of a speaker's communication performance.

    The underlying objective measurements are calculated separately by
    Python. Gemini is responsible only for interpreting those measurements
    and producing useful feedback.
    """

    clarity: str
    conciseness: str
    delivery: str
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]

    def __post_init__(self) -> None:
        if not self.clarity.strip():
            raise ValueError("Clarity feedback cannot be empty.")

        if not self.conciseness.strip():
            raise ValueError("Conciseness feedback cannot be empty.")

        if not self.delivery.strip():
            raise ValueError("Delivery feedback cannot be empty.")

        if not self.strengths:
            raise ValueError("At least one communication strength is required.")

        if not self.weaknesses:
            raise ValueError("At least one communication weakness is required.")

        if not self.recommendations:
            raise ValueError(
                "At least one communication recommendation is required."
            )

        self.strengths = [
            strength.strip()
            for strength in self.strengths
            if strength.strip()
        ]

        self.weaknesses = [
            weakness.strip()
            for weakness in self.weaknesses
            if weakness.strip()
        ]

        self.recommendations = [
            recommendation.strip()
            for recommendation in self.recommendations
            if recommendation.strip()
        ]

        if not self.strengths:
            raise ValueError("At least one communication strength is required.")

        if not self.weaknesses:
            raise ValueError("At least one communication weakness is required.")

        if not self.recommendations:
            raise ValueError(
                "At least one communication recommendation is required."
            )