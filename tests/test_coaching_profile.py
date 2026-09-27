from debate_arena.debate.coaching_profile import CoachingProfile


def test_coaching_profile_defaults_are_empty():
    profile = CoachingProfile()

    assert profile.strengths == []
    assert profile.improvement_areas == []
    assert profile.coaching_priorities == []
    assert profile.strongest_moments == []
    assert profile.weakest_moments == []
    assert profile.overall_coaching_summary == ""


def test_coaching_profile_stores_values():
    profile = CoachingProfile(
        strengths=["Clear reasoning."],
        improvement_areas=["Evidence usage."],
        coaching_priorities=["Use stronger evidence."],
        strongest_moments=["Round 2 rebuttal."],
        weakest_moments=["Round 1 claim."],
        overall_coaching_summary="Focus on evidence.",
    )

    assert profile.strengths == ["Clear reasoning."]
    assert profile.improvement_areas == ["Evidence usage."]
    assert profile.coaching_priorities == [
        "Use stronger evidence."
    ]
    assert profile.strongest_moments == [
        "Round 2 rebuttal."
    ]
    assert profile.weakest_moments == [
        "Round 1 claim."
    ]
    assert profile.overall_coaching_summary == (
        "Focus on evidence."
    )


def test_coaching_profile_cleans_whitespace_and_empty_values():
    profile = CoachingProfile(
        strengths=[
            "  Clear reasoning.  ",
            "",
            "   ",
        ],
        improvement_areas=[
            "  Evidence usage. ",
            "",
        ],
        coaching_priorities=[
            " Use examples. ",
            " ",
        ],
        strongest_moments=[
            " Round 2. ",
            "",
        ],
        weakest_moments=[
            " Round 1. ",
            "   ",
        ],
        overall_coaching_summary="  Improve evidence.  ",
    )

    assert profile.strengths == [
        "Clear reasoning."
    ]
    assert profile.improvement_areas == [
        "Evidence usage."
    ]
    assert profile.coaching_priorities == [
        "Use examples."
    ]
    assert profile.strongest_moments == [
        "Round 2."
    ]
    assert profile.weakest_moments == [
        "Round 1."
    ]
    assert profile.overall_coaching_summary == (
        "Improve evidence."
    )