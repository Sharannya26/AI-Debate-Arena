from dataclasses import dataclass

from debate_arena.debate.strategy import DebateStrategy


@dataclass
class DebateResponse:
    """Structured result produced by the debate reasoning model."""

    strategy: DebateStrategy
    rebuttal: str