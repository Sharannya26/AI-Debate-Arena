from debate_arena.debate.debate_report import DebateReport


def test_debate_report_stores_complete_report_data():
    report = DebateReport(
        topic="Should social media be banned for students?",
        user_position="Against",
        ai_position="For",
        rounds_completed=3,
        summary=(
            "The user maintained a consistent position "
            "throughout the debate."
        ),
        strongest_argument=(
            "Students can learn responsible social media usage."
        ),
        weakest_argument=(
            "Social media provides educational opportunities."
        ),
        strengths=[
            "Clear position",
            "Consistent reasoning",
        ],
        weaknesses=[
            "Limited evidence",
        ],
        evidence_usage=(
            "The user relied mainly on reasoning "
            "rather than concrete evidence."
        ),
        consistency=(
            "The user's position remained consistent."
        ),
        responsiveness=(
            "The user addressed the opposing arguments."
        ),
        recommendations=[
            "Use concrete evidence to support major claims.",
            "Address opposing arguments more directly.",
        ],
    )

    assert report.topic == (
        "Should social media be banned for students?"
    )

    assert report.user_position == "Against"
    assert report.ai_position == "For"
    assert report.rounds_completed == 3

    assert report.summary == (
        "The user maintained a consistent position "
        "throughout the debate."
    )

    assert report.strongest_argument == (
        "Students can learn responsible social media usage."
    )

    assert report.weakest_argument == (
        "Social media provides educational opportunities."
    )

    assert report.strengths == [
        "Clear position",
        "Consistent reasoning",
    ]

    assert report.weaknesses == [
        "Limited evidence",
    ]

    assert report.recommendations == [
        "Use concrete evidence to support major claims.",
        "Address opposing arguments more directly.",
    ]


def test_debate_report_defaults_optional_fields():
    report = DebateReport(
        topic="Test topic",
        user_position="Against",
        ai_position="For",
        rounds_completed=1,
        summary="Test summary.",
    )

    assert report.strongest_argument == ""
    assert report.weakest_argument == ""

    assert report.strengths == []
    assert report.weaknesses == []

    assert report.evidence_usage == ""
    assert report.consistency == ""
    assert report.responsiveness == ""

    assert report.recommendations == []


def test_debate_report_lists_are_independent():
    report_one = DebateReport(
        topic="Topic",
        user_position="Against",
        ai_position="For",
        rounds_completed=1,
        summary="Summary.",
    )

    report_two = DebateReport(
        topic="Topic",
        user_position="Against",
        ai_position="For",
        rounds_completed=1,
        summary="Summary.",
    )

    report_one.strengths.append(
        "Clear reasoning"
    )

    report_one.recommendations.append(
        "Use stronger evidence"
    )

    assert report_one.strengths == [
        "Clear reasoning"
    ]

    assert report_two.strengths == []

    assert report_one.recommendations == [
        "Use stronger evidence"
    ]

    assert report_two.recommendations == []


def test_debate_report_can_represent_zero_completed_rounds():
    report = DebateReport(
        topic="Test topic",
        user_position="Against",
        ai_position="For",
        rounds_completed=0,
        summary="No debate rounds were completed.",
    )

    assert report.rounds_completed == 0