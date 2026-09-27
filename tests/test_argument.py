from debate_arena.debate.argument import Argument


def test_argument_can_be_created():
    argument = Argument(
        speaker="user",
        text="Social media has educational benefits.",
        round=1,
        turn=1,
    )

    assert argument.speaker == "user"
    assert argument.text == "Social media has educational benefits."
    assert argument.round == 1
    assert argument.turn == 1