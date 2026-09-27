from dataclasses import dataclass, field


@dataclass
class AdaptiveMiniDebate:
    """
    Represents a short adaptive practice debate
    focused on one specific improvement priority.

    This model stores the state of the mini-debate.
    It does not perform analysis and does not call Gemini.
    """

    topic: str
    focus_area: str
    user_prompt: str
    ai_prompt: str = ""
    current_turn: str = "user"
    round_number: int = 1
    max_rounds: int = 2
    user_responses: list[str] = field(default_factory=list)
    ai_responses: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.topic = self.topic.strip()
        self.focus_area = self.focus_area.strip()
        self.user_prompt = self.user_prompt.strip()
        self.ai_prompt = self.ai_prompt.strip()
        self.current_turn = self.current_turn.strip().lower()

        self.user_responses = [
            response.strip()
            for response in self.user_responses
            if response and response.strip()
        ]

        self.ai_responses = [
            response.strip()
            for response in self.ai_responses
            if response and response.strip()
        ]

        if not self.topic:
            raise ValueError(
                "Mini-debate topic cannot be empty."
            )

        if not self.focus_area:
            raise ValueError(
                "Mini-debate focus area cannot be empty."
            )

        if not self.user_prompt:
            raise ValueError(
                "Mini-debate user prompt cannot be empty."
            )

        if self.current_turn not in {"user", "ai"}:
            raise ValueError(
                "Mini-debate current turn must be 'user' or 'ai'."
            )

        if self.round_number < 1:
            raise ValueError(
                "Mini-debate round number must be at least 1."
            )

        if self.max_rounds < 1:
            raise ValueError(
                "Mini-debate max rounds must be at least 1."
            )

    def add_user_response(self, response: str) -> None:
        response = response.strip()

        if not response:
            raise ValueError(
                "Mini-debate user response cannot be empty."
            )

        self.user_responses.append(response)
        self.current_turn = "ai"

    def add_ai_response(self, response: str) -> None:
        response = response.strip()

        if not response:
            raise ValueError(
                "Mini-debate AI response cannot be empty."
            )

        self.ai_responses.append(response)
        self.current_turn = "user"

    def advance_round(self) -> None:
        self.round_number += 1

    def is_finished(self) -> bool:
        return self.round_number > self.max_rounds