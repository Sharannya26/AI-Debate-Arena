from enum import Enum


class DebateStrategy(str, Enum):
    """Strategies the AI can use when responding to an argument."""

    DIRECT_COUNTER = "direct_counter"
    EVIDENCE_CHALLENGE = "evidence_challenge"
    ASSUMPTION_CHALLENGE = "assumption_challenge"
    COUNTEREXAMPLE = "counterexample"
    CONCESSION_REBUTTAL = "concession_rebuttal"
    ALTERNATIVE_SOLUTION = "alternative_solution"
    CONSISTENCY_CHALLENGE = "consistency_challenge"