from debate_arena.debate.strategy import DebateStrategy


def test_debate_strategies_exist() -> None:
    assert DebateStrategy.DIRECT_COUNTER.value == "direct_counter"
    assert DebateStrategy.EVIDENCE_CHALLENGE.value == "evidence_challenge"
    assert DebateStrategy.ASSUMPTION_CHALLENGE.value == "assumption_challenge"
    assert DebateStrategy.COUNTEREXAMPLE.value == "counterexample"
    assert DebateStrategy.CONCESSION_REBUTTAL.value == "concession_rebuttal"
    assert DebateStrategy.ALTERNATIVE_SOLUTION.value == "alternative_solution"
    assert DebateStrategy.CONSISTENCY_CHALLENGE.value == "consistency_challenge"