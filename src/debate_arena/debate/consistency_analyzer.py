import re

from debate_arena.debate.argument import Argument
from debate_arena.debate.consistency_analysis import (
    ConsistencyAnalysis,
)


class ConsistencyAnalyzer:
    """
    Determines whether the user's arguments remain consistent
    across multiple debate rounds.

    This first version uses deterministic keyword overlap.
    Deeper semantic contradiction detection can be added
    with Gemini later.
    """

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
        user_arguments: list[Argument],
    ) -> ConsistencyAnalysis:
        """
        Analyze consistency across the user's arguments.

        At least two user arguments are required because
        consistency is a cross-round property.
        """

        if user_arguments is None:
            raise ValueError("User arguments cannot be None.")

        if len(user_arguments) < 2:
            return ConsistencyAnalysis(
                consistency=(
                    "Not enough arguments to determine consistency."
                )
            )

        for argument in user_arguments:
            if argument is None:
                raise ValueError(
                    "User arguments cannot contain None."
                )

            if argument.speaker != "user":
                raise ValueError(
                    "All arguments must be from the user."
                )

        keyword_sets = [
            self._extract_keywords(argument.text)
            for argument in user_arguments
        ]

        consistent_points: list[str] = []
        inconsistent_points: list[str] = []

        for index in range(1, len(keyword_sets)):
            previous_keywords = keyword_sets[index - 1]
            current_keywords = keyword_sets[index]

            overlap = previous_keywords.intersection(
                current_keywords
            )

            if overlap:
                consistent_points.append(
                    (
                        f"Round {user_arguments[index - 1].round} "
                        f"and Round {user_arguments[index].round} "
                        "share related ideas: "
                        f"{', '.join(sorted(overlap))}."
                    )
                )
            else:
                inconsistent_points.append(
                    (
                        f"Round {user_arguments[index - 1].round} "
                        f"and Round {user_arguments[index].round} "
                        "do not share identifiable keywords."
                    )
                )

        consistency = self._classify_consistency(
            keyword_sets
        )

        return ConsistencyAnalysis(
            consistency=consistency,
            consistent_points=consistent_points,
            inconsistent_points=inconsistent_points,
        )

    @classmethod
    def _extract_keywords(
        cls,
        text: str,
    ) -> set[str]:
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
    def _classify_consistency(
        keyword_sets: list[set[str]],
    ) -> str:
        if len(keyword_sets) < 2:
            return "Not enough arguments to determine consistency."

        comparisons = len(keyword_sets) - 1
        consistent_comparisons = 0

        for index in range(1, len(keyword_sets)):
            previous_keywords = keyword_sets[index - 1]
            current_keywords = keyword_sets[index]

            if previous_keywords.intersection(
                current_keywords
            ):
                consistent_comparisons += 1

        ratio = (
            consistent_comparisons / comparisons
        )

        if ratio >= 0.75:
            return "Highly consistent."

        if ratio >= 0.50:
            return "Mostly consistent."

        if ratio > 0:
            return "Partially consistent."

        return "No consistent keywords identified."