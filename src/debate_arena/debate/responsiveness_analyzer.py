import re

from debate_arena.debate.argument import Argument
from debate_arena.debate.responsiveness_analysis import (
    ResponsivenessAnalysis,
)


class ResponsivenessAnalyzer:
    """
    Determines how directly a user's argument responds to the
    AI's previous argument.

    This first version uses deterministic lexical overlap.
    Deeper semantic interpretation can be added with Gemini later.
    """

    # Common words that do not provide much information when
    # comparing two debate arguments.
    STOP_WORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "because",
        "but",
        "by",
        "can",
        "could",
        "do",
        "for",
        "from",
        "has",
        "have",
        "in",
        "is",
        "it",
        "its",
        "may",
        "more",
        "of",
        "on",
        "or",
        "should",
        "that",
        "the",
        "their",
        "there",
        "this",
        "to",
        "was",
        "were",
        "will",
        "with",
        "would",
        "you",
        "your",
    }

    def analyze(
        self,
        previous_ai_argument: Argument,
        user_argument: Argument,
    ) -> ResponsivenessAnalysis:
        """
        Analyze how much the user's argument responds to the
        previous AI argument.
        """

        if previous_ai_argument is None:
            raise ValueError(
                "Previous AI argument cannot be None."
            )

        if user_argument is None:
            raise ValueError(
                "User argument cannot be None."
            )

        if previous_ai_argument.speaker != "ai":
            raise ValueError(
                "Previous argument must be from the AI."
            )

        if user_argument.speaker != "user":
            raise ValueError(
                "User argument must be from the user."
            )

        ai_keywords = self._extract_keywords(
            previous_ai_argument.text
        )
        user_keywords = self._extract_keywords(
            user_argument.text
        )

        addressed = sorted(
            ai_keywords.intersection(user_keywords)
        )

        ignored = sorted(
            ai_keywords.difference(user_keywords)
        )

        responsiveness = self._classify_responsiveness(
            ai_keywords=ai_keywords,
            user_keywords=user_keywords,
        )

        return ResponsivenessAnalysis(
            responsiveness=responsiveness,
            addressed_points=addressed,
            ignored_points=ignored,
        )

    @classmethod
    def _extract_keywords(cls, text: str) -> set[str]:
        """
        Extract meaningful lowercase words from an argument.
        """

        words = re.findall(
            r"\b[a-zA-Z]+\b",
            text.lower(),
        )

        return {
            word
            for word in words
            if word not in cls.STOP_WORDS
        }

    @staticmethod
    def _classify_responsiveness(
        ai_keywords: set[str],
        user_keywords: set[str],
    ) -> str:
        """
        Classify responsiveness based on keyword overlap.

        This is intentionally simple and deterministic.
        """

        if not ai_keywords:
            return "Unable to determine responsiveness."

        overlap = ai_keywords.intersection(user_keywords)
        overlap_ratio = len(overlap) / len(ai_keywords)

        if overlap_ratio >= 0.50:
            return "Highly responsive."

        if overlap_ratio >= 0.25:
            return "Partially responsive."

        if overlap:
            return "Minimally responsive."

        return "Not directly responsive."