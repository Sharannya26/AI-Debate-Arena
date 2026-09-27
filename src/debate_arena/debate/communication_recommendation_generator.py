from debate_arena.debate.communication_analysis import (
    CommunicationAnalysis,
)
from debate_arena.debate.communication_feedback import (
    CommunicationFeedback,
)
from debate_arena.debate.communication_improvement_target import (
    CommunicationImprovementTarget,
)
from debate_arena.debate.personalized_communication_feedback import (
    PersonalizedCommunicationFeedback,
)
from debate_arena.debate.speaking_pace import SpeakingPace


class CommunicationRecommendationGenerator:
    """
    Generates personalized communication recommendations.

    Objective communication measurements are calculated by Python,
    while qualitative interpretation comes from Gemini.

    This class combines both sources to produce concrete,
    actionable communication coaching.
    """

    def generate(
        self,
        analysis: CommunicationAnalysis,
        feedback: CommunicationFeedback,
    ) -> PersonalizedCommunicationFeedback:
        """
        Generate personalized communication coaching.
        """

        if analysis is None:
            raise ValueError(
                "Communication analysis cannot be None."
            )

        if feedback is None:
            raise ValueError(
                "Communication feedback cannot be None."
            )

        primary_focus = self._select_primary_focus(
            analysis,
            feedback,
        )

        improvement_goal = self._build_improvement_goal(
            primary_focus
        )

        action_plan = self._build_action_plan(
            primary_focus,
            analysis,
        )

        return PersonalizedCommunicationFeedback(
            primary_focus=primary_focus,
            improvement_goal=improvement_goal,
            action_plan=action_plan,
        )

    @staticmethod
    def _select_primary_focus(
        analysis: CommunicationAnalysis,
        feedback: CommunicationFeedback,
    ) -> CommunicationImprovementTarget:
        """
        Select the most relevant communication area to improve.

        Objective measurements take priority because they are
        deterministic. Gemini weaknesses are used as a secondary
        signal when the objective measurements do not identify
        an obvious focus.
        """

        if analysis.filler_rate > 0.05:
            return CommunicationImprovementTarget.FILLER_WORDS

        if analysis.speaking_pace == SpeakingPace.FAST:
            return CommunicationImprovementTarget.SPEAKING_PACE

        if analysis.speaking_pace == SpeakingPace.SLOW:
            return CommunicationImprovementTarget.SPEAKING_PACE

        if analysis.average_words_per_sentence > 25:
            return CommunicationImprovementTarget.SENTENCE_LENGTH

        if feedback.weaknesses:
            return CommunicationImprovementTarget.ARGUMENT_DELIVERY

        return CommunicationImprovementTarget.OVERALL_CLARITY

    @staticmethod
    def _build_improvement_goal(
        primary_focus: CommunicationImprovementTarget,
    ) -> str:
        """
        Build a clear improvement goal for the selected focus.
        """

        goals = {
            CommunicationImprovementTarget.FILLER_WORDS: (
                "Reduce filler-word usage and replace fillers "
                "with intentional pauses."
            ),
            CommunicationImprovementTarget.SPEAKING_PACE: (
                "Maintain a controlled speaking pace so that "
                "arguments are easier to follow."
            ),
            CommunicationImprovementTarget.SENTENCE_LENGTH: (
                "Use shorter sentences to communicate "
                "arguments more clearly."
            ),
            CommunicationImprovementTarget.ARGUMENT_DELIVERY: (
                "Make arguments more direct, structured, "
                "and responsive during the debate."
            ),
            CommunicationImprovementTarget.OVERALL_CLARITY: (
                "Improve overall clarity and precision when "
                "communicating arguments."
            ),
        }

        return goals[primary_focus]

    @staticmethod
    def _build_action_plan(
        primary_focus: CommunicationImprovementTarget,
        analysis: CommunicationAnalysis,
    ) -> list[str]:
        """
        Build concrete actions for the selected communication focus.
        """

        if (
            primary_focus
            == CommunicationImprovementTarget.FILLER_WORDS
        ):
            actions = [
                "Pause briefly before answering instead of using filler words.",
                "Replace repeated filler words with intentional silence.",
                "Before each debate response, identify the main point you want to make.",
            ]

            if analysis.filler_rate > 0.10:
                actions.append(
                    "Practice answering short questions while deliberately "
                    "avoiding filler words."
                )

            return actions

        if (
            primary_focus
            == CommunicationImprovementTarget.SPEAKING_PACE
        ):
            if analysis.speaking_pace == SpeakingPace.FAST:
                return [
                    "Pause briefly after each major claim.",
                    "Slow down slightly when introducing important evidence.",
                    "Use short pauses between separate arguments.",
                ]

            return [
                "Maintain a steady speaking rhythm.",
                "Avoid excessively long pauses between ideas.",
                "Use deliberate pauses to separate major arguments.",
            ]

        if (
            primary_focus
            == CommunicationImprovementTarget.SENTENCE_LENGTH
        ):
            return [
                "Break long sentences into shorter statements.",
                "Express one main idea per sentence.",
                "Pause briefly when moving from one argument to another.",
            ]

        if (
            primary_focus
            == CommunicationImprovementTarget.ARGUMENT_DELIVERY
        ):
            return [
                "State your main claim before explaining your reasoning.",
                "Respond directly to the strongest point made by the opponent.",
                "End each argument with a clear takeaway.",
            ]

        return [
            "State your main claim clearly before explaining it.",
            "Use concise sentences when presenting arguments.",
            "Pause briefly between major ideas.",
        ]