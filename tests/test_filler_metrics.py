import pytest

from debate_arena.debate.filler_metrics import FillerMetrics


def test_filler_metrics_stores_data():
    metrics = FillerMetrics(
        total_filler_count=3,
        filler_counts={
            "um": 1,
            "uh": 1,
            "like": 1,
        },
        total_word_count=30,
        filler_rate=0.1,
    )

    assert metrics.total_filler_count == 3
    assert metrics.filler_counts == {
        "um": 1,
        "uh": 1,
        "like": 1,
    }
    assert metrics.total_word_count == 30
    assert metrics.filler_rate == 0.1


def test_filler_metrics_defaults_to_zero():
    metrics = FillerMetrics()

    assert metrics.total_filler_count == 0
    assert metrics.filler_counts == {}
    assert metrics.total_word_count == 0
    assert metrics.filler_rate == 0.0


def test_filler_metrics_rejects_negative_total():
    with pytest.raises(
        ValueError,
        match="Total filler count cannot be negative",
    ):
        FillerMetrics(total_filler_count=-1)


def test_filler_metrics_rejects_negative_filler_count():
    with pytest.raises(
        ValueError,
        match="Filler count cannot be negative",
    ):
        FillerMetrics(
            total_filler_count=0,
            filler_counts={"um": -1},
        )


def test_filler_metrics_rejects_empty_filler_word():
    with pytest.raises(
        ValueError,
        match="Filler word cannot be empty",
    ):
        FillerMetrics(
            total_filler_count=1,
            filler_counts={"   ": 1},
        )


def test_filler_metrics_rejects_incorrect_total():
    with pytest.raises(
        ValueError,
        match="Total filler count must match filler counts",
    ):
        FillerMetrics(
            total_filler_count=5,
            filler_counts={"um": 2},
        )


def test_filler_metrics_normalizes_filler_words():
    metrics = FillerMetrics(
        total_filler_count=3,
        filler_counts={
            " UM ": 1,
            "Uh": 1,
            "LIKE": 1,
        },
        total_word_count=30,
        filler_rate=0.1,
    )

    assert metrics.filler_counts == {
        "um": 1,
        "uh": 1,
        "like": 1,
    }


def test_filler_metrics_calculates_expected_rate():
    metrics = FillerMetrics(
        total_filler_count=4,
        filler_counts={
            "um": 2,
            "like": 2,
        },
        total_word_count=50,
        filler_rate=0.08,
    )

    assert metrics.filler_rate == 0.08


def test_filler_metrics_rejects_negative_word_count():
    with pytest.raises(
        ValueError,
        match="Total word count cannot be negative",
    ):
        FillerMetrics(
            total_filler_count=0,
            total_word_count=-1,
        )


def test_filler_metrics_rejects_negative_filler_rate():
    with pytest.raises(
        ValueError,
        match="Filler rate cannot be negative",
    ):
        FillerMetrics(
            total_filler_count=0,
            total_word_count=10,
            filler_rate=-0.1,
        )


def test_filler_metrics_rejects_filler_count_above_word_count():
    with pytest.raises(
        ValueError,
        match="Total filler count cannot exceed total word count",
    ):
        FillerMetrics(
            total_filler_count=6,
            filler_counts={"um": 6},
            total_word_count=5,
            filler_rate=1.2,
        )


def test_filler_metrics_rejects_incorrect_rate():
    with pytest.raises(
        ValueError,
        match="Filler rate must match filler count and word count",
    ):
        FillerMetrics(
            total_filler_count=4,
            filler_counts={"um": 4},
            total_word_count=50,
            filler_rate=0.2,
        )


def test_filler_metrics_handles_zero_words():
    metrics = FillerMetrics(
        total_filler_count=0,
        filler_counts={},
        total_word_count=0,
        filler_rate=0.0,
    )

    assert metrics.filler_rate == 0.0