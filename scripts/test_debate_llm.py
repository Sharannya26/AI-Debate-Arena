from debate_arena.debate.engine import DebateEngine
from debate_arena.debate.state import DebateState


def main() -> None:
    state = DebateState(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        max_rounds=3,
    )

    engine = DebateEngine(state)

    # -------------------------
    # ROUND 1
    # -------------------------

    engine.submit_user_argument(
        "Social media should not be banned because students can use it "
        "to collaborate, communicate, and access educational resources."
    )

    print("\n========== ROUND 1 ==========")
    print("USER:")
    print(state.user_arguments[-1].text)

    rebuttal = engine.generate_ai_rebuttal()

    print("\nAI:")
    print(rebuttal)

    engine.submit_ai_argument(rebuttal)

    # -------------------------
    # ROUND 2
    # -------------------------

    engine.start_new_round()

    engine.submit_user_argument(
        "Those risks can be reduced through screen-time limits and "
        "digital literacy education instead of banning social media."
    )

    print("\n========== ROUND 2 ==========")
    print("USER:")
    print(state.user_arguments[-1].text)

    rebuttal = engine.generate_ai_rebuttal()

    print("\nAI:")
    print(rebuttal)

    engine.submit_ai_argument(rebuttal)

    # -------------------------
    # SHOW CONTEXT
    # -------------------------

    print("\n========== DEBATE CONTEXT ==========")
    print(state.get_context())


if __name__ == "__main__":
    main()