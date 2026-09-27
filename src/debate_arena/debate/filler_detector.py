import re

from debate_arena.debate.filler_metrics import FillerMetrics
from debate_arena.debate.speech_sample import SpeechSample


class FillerWordDetector:
    """
    Detects common filler words and phrases in a speech sample.

    Detection is deterministic and handled entirely by Python.
    """

    DEFAULT_FILLERS = (
        "um",
        "uh",
        "er",
        "hmm",
        "like",
        "you know",
        "actually",
        "basically",
    )

    def __init__(
        self,
        fillers: tuple[str, ...] | None = None,
    ) -> None:
        self.fillers = fillers or self.DEFAULT_FILLERS

    def analyze(self, sample: SpeechSample) -> FillerMetrics:
        """
        Detect filler words and phrases in a speech sample.
        """
        if sample is None:
            raise ValueError("Speech sample cannot be None.")

        text = sample.text.strip().lower()

        total_word_count = len(text.split())

        filler_counts: dict[str, int] = {}

        for filler in self.fillers:
            pattern = self._build_pattern(filler)

            matches = re.findall(pattern, text)

            if matches:
                filler_counts[filler] = len(matches)

        total_filler_count = sum(filler_counts.values())

        filler_rate = (
            total_filler_count / total_word_count
            if total_word_count > 0
            else 0.0
        )

        return FillerMetrics(
            total_filler_count=total_filler_count,
            filler_counts=filler_counts,
            total_word_count=total_word_count,
            filler_rate=filler_rate,
        )

    @staticmethod
    def _build_pattern(filler: str) -> str:
        """
        Build a word-boundary regex for a filler phrase.
        """
        escaped = re.escape(filler.strip())

        return rf"\b{escaped}\b"