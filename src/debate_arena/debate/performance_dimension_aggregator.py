from collections.abc import Sequence


class PerformanceDimensionAggregator:
    """
    Aggregates qualitative performance descriptions across
    multiple debate rounds.

    The aggregation is deterministic and does not use Gemini.
    """

    QUALITY_LEVELS = {
        "very weak": 0,
        "weak": 1,
        "limited": 2,
        "moderate": 3,
        "mostly consistent": 3,
        "partial": 3,
        "partially responsive": 3,
        "strong": 4,
        "highly responsive": 5,
        "highly consistent": 5,
        "excellent": 5,
    }

    def aggregate(
        self,
        values: Sequence[str],
        dimension_name: str,
    ) -> str:
        if values is None:
            raise ValueError(
                "Dimension values cannot be None."
            )

        if not dimension_name or not dimension_name.strip():
            raise ValueError(
                "Dimension name cannot be empty."
            )

        cleaned_values = [
            value.strip()
            for value in values
            if value and value.strip()
        ]

        if not cleaned_values:
            return (
                f"No {dimension_name.strip()} data available."
            )

        scores = [
            self._quality_score(value)
            for value in cleaned_values
        ]

        if len(cleaned_values) == 1:
            return cleaned_values[0]

        if all(score == scores[0] for score in scores):
            return (
                f"{dimension_name.strip().capitalize()} "
                f"remained consistently "
                f"{cleaned_values[-1].lower()}"
            )

        if scores[-1] > scores[0]:
            return (
                f"{dimension_name.strip().capitalize()} "
                "improved across the debate."
            )

        if scores[-1] < scores[0]:
            return (
                f"{dimension_name.strip().capitalize()} "
                "declined across the debate."
            )

        return (
            f"{dimension_name.strip().capitalize()} "
            "varied across the debate."
        )

    def aggregate_round_performances(
        self,
        round_performances,
    ) -> dict[str, str]:
        if round_performances is None:
            raise ValueError(
                "Round performances cannot be None."
            )

        if not round_performances:
            return {}

        dimensions = {
            "argument quality": [
                performance.argument_quality
                for performance in round_performances
            ],
            "communication quality": [
                performance.communication_quality
                for performance in round_performances
            ],
            "evidence usage": [
                performance.evidence_usage
                for performance in round_performances
            ],
            "reasoning quality": [
                performance.reasoning_quality
                for performance in round_performances
            ],
            "responsiveness": [
                performance.responsiveness
                for performance in round_performances
                if performance.responsiveness is not None
            ],
        }

        return {
            dimension: self._aggregate_round_dimension(
                values,
                dimension,
            )
            for dimension, values in dimensions.items()
        }

    def _aggregate_round_dimension(
        self,
        values: Sequence[str],
        dimension_name: str,
    ) -> str:
        """
        Aggregate production RoundPerformance descriptions.

        These descriptions are more specific than the generic
        quality vocabulary handled by aggregate().
        """

        cleaned_values = [
            value.strip()
            for value in values
            if value and value.strip()
        ]

        if not cleaned_values:
            return (
                f"No {dimension_name} data available."
            )

        if len(cleaned_values) == 1:
            return cleaned_values[0]

        scores = [
            self._round_performance_score(
                value,
                dimension_name,
            )
            for value in cleaned_values
        ]

        if all(score == scores[0] for score in scores):
            return self._build_consistency_summary(
                dimension_name=dimension_name,
                value=cleaned_values[-1],
            )

        if scores[-1] > scores[0]:
            return (
                f"{dimension_name.capitalize()} "
                "improved across the debate."
            )

        if scores[-1] < scores[0]:
            return (
                f"{dimension_name.capitalize()} "
                "declined across the debate."
            )

        return (
            f"{dimension_name.capitalize()} "
            "varied across the debate."
        )

    @staticmethod
    def _build_consistency_summary(
        dimension_name: str,
        value: str,
    ) -> str:
        """
        Convert a repeated production description into a
        natural qualitative consistency summary.

        RoundPerformance values are often complete sentences,
        so they should not be appended directly after
        "remained consistently".
        """

        normalized = value.strip().lower()

        if dimension_name == "argument quality":
            if "identifiable weaknesses" in normalized:
                descriptor = "weak"
            elif "clear claim supported by reasoning" in normalized:
                descriptor = "strong"
            elif "clear claim" in normalized:
                descriptor = "moderate"
            else:
                descriptor = "stable"

        elif dimension_name == "communication quality":
            if "fast pace" in normalized:
                descriptor = "limited"
            elif "moderate pace" in normalized:
                descriptor = "strong"
            elif "slow pace" in normalized:
                descriptor = "moderate"
            else:
                descriptor = "stable"

        elif dimension_name == "evidence usage":
            marker = "used "
            suffix = " identified piece(s) of evidence"

            if marker in normalized and suffix in normalized:
                try:
                    count_text = normalized.split(
                        marker,
                        1,
                    )[1].split(
                        suffix,
                        1,
                    )[0]

                    count = int(count_text)

                    if count == 0:
                        descriptor = "limited"
                    elif count == 1:
                        descriptor = "moderate"
                    else:
                        descriptor = "strong"

                except (ValueError, IndexError):
                    descriptor = "stable"
            else:
                descriptor = "stable"

        elif dimension_name == "reasoning quality":
            if "no explicit reasoning structure" in normalized:
                descriptor = "weak"
            elif "reasoning was identified" in normalized:
                descriptor = "strong"
            else:
                descriptor = "stable"

        elif dimension_name == "responsiveness":
            if "highly responsive" in normalized:
                descriptor = "highly responsive"
            elif "partially responsive" in normalized:
                descriptor = "moderately responsive"
            elif "minimally responsive" in normalized:
                descriptor = "limited"
            elif "not responsive" in normalized:
                descriptor = "weak"
            else:
                descriptor = "stable"

        else:
            descriptor = "stable"

        return (
            f"{dimension_name.capitalize()} "
            f"remained consistently "
            f"{descriptor} across the debate."
        )

    @staticmethod
    def _round_performance_score(
        value: str,
        dimension_name: str,
    ) -> int:
        """
        Convert a production RoundPerformance description
        into a deterministic comparison score.

        Supports both:
        1. Generic qualitative labels such as Strong, Weak,
           Moderate, Limited, and Excellent.
        2. Detailed production descriptions generated by
           the debate-performance analysis pipeline.
        """

        cleaned_value = value.strip().lower()

        # --------------------------------------------------
        # Generic qualitative labels
        # --------------------------------------------------
        #
        # These are important because RoundPerformance can
        # contain simple values such as "Strong" and "Weak".
        #
        generic_quality_scores = {
            "very weak": 0,
            "weak": 1,
            "limited": 2,
            "moderate": 3,
            "mostly consistent": 3,
            "partial": 3,
            "partially responsive": 3,
            "strong": 4,
            "highly responsive": 5,
            "highly consistent": 5,
            "excellent": 5,
        }

        if cleaned_value in generic_quality_scores:
            return generic_quality_scores[cleaned_value]

        # --------------------------------------------------
        # Argument quality
        # --------------------------------------------------

        if dimension_name == "argument quality":
            if "identifiable weaknesses" in cleaned_value:
                return 2

            if (
                "clear claim supported by reasoning"
                in cleaned_value
            ):
                return 4

            if "clear claim" in cleaned_value:
                return 3

            return 3

        # --------------------------------------------------
        # Communication quality
        # --------------------------------------------------

        if dimension_name == "communication quality":
            if "fast pace" in cleaned_value:
                return 2

            if "moderate pace" in cleaned_value:
                return 4

            if "slow pace" in cleaned_value:
                return 3

            return 3

        # --------------------------------------------------
        # Evidence usage
        # --------------------------------------------------

        if dimension_name == "evidence usage":
            marker = "used "
            suffix = " identified piece(s) of evidence"

            if marker in cleaned_value and suffix in cleaned_value:
                try:
                    count_text = (
                        cleaned_value
                        .split(
                            marker,
                            1,
                        )[1]
                        .split(
                            suffix,
                            1,
                        )[0]
                    )

                    return int(count_text)

                except (ValueError, IndexError):
                    return 3

            return 3

        # --------------------------------------------------
        # Reasoning quality
        # --------------------------------------------------

        if dimension_name == "reasoning quality":
            if (
                "no explicit reasoning structure"
                in cleaned_value
            ):
                return 2

            if "reasoning was identified" in cleaned_value:
                return 4

            return 3

        # --------------------------------------------------
        # Responsiveness
        # --------------------------------------------------

        if dimension_name == "responsiveness":
            if "highly responsive" in cleaned_value:
                return 5

            if "partially responsive" in cleaned_value:
                return 3

            return 3

        return 3

    @classmethod
    def _quality_score(
        cls,
        value: str,
    ) -> int:
        cleaned_value = value.strip().lower()

        for quality, score in cls.QUALITY_LEVELS.items():
            if quality in cleaned_value:
                return score

        return 3