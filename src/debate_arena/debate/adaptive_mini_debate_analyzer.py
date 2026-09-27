from debate_arena.debate.adaptive_mini_debate import (
    AdaptiveMiniDebate,
)
from debate_arena.debate.personalized_improvement_priority import (
    PersonalizedImprovementPriority,
)


class AdaptiveMiniDebateAnalyzer:
    """
    Converts a personalized improvement priority into
    a short adaptive mini-debate.

    This analyzer is deterministic and does not call Gemini.
    """

    MINI_DEBATE_GUIDANCE = {
        "argument quality": {
            "user_prompt": (
                "Make one clear claim, give one reason "
                "supporting it, and finish with one "
                "concrete example."
            ),
            "ai_prompt": (
                "Challenge the user's claim and ask "
                "whether their reason and example "
                "actually support the conclusion."
            ),
        },
        "communication quality": {
            "user_prompt": (
                "Explain one important point in no more "
                "than two clear sentences."
            ),
            "ai_prompt": (
                "Challenge the user with a follow-up "
                "question that requires a concise response."
            ),
        },
        "evidence usage": {
            "user_prompt": (
                "Make one claim and support it with "
                 "one piece of concrete evidence, such as "
                "one concrete fact, example, or statistic."
            ),
            "ai_prompt": (
                "Question the evidence and ask the user "
                "to explain why it supports their claim."
            ),
        },
        "reasoning quality": {
            "user_prompt": (
                "State one claim, provide supporting "
                "evidence, and explain why the evidence "
                "supports your conclusion."
            ),
            "ai_prompt": (
                "Challenge the logical connection between "
                "the user's evidence and conclusion."
            ),
        },
        "responsiveness": {
            "user_prompt": (
                "Respond directly to the opponent's "
                "main claim before introducing your "
                "own argument."
            ),
            "ai_prompt": (
                "Present a short opposing argument and "
                "challenge the user to address its main "
                "claim directly."
            ),
        },
    }

    def analyze(
        self,
        priority: PersonalizedImprovementPriority,
        topic: str,
    ) -> AdaptiveMiniDebate:
        if priority is None:
            raise ValueError(
                "Improvement priority cannot be None."
            )

        if not topic or not topic.strip():
            raise ValueError(
                "Mini-debate topic cannot be empty."
            )

        topic = topic.strip()

        focus_area = priority.focus_area.strip().lower()

        dimension = self._extract_dimension(
            focus_area=focus_area,
            priority=priority.priority,
        )

        guidance = self.MINI_DEBATE_GUIDANCE.get(
            dimension
        )

        if guidance is None:
            return AdaptiveMiniDebate(
                topic=topic,
                focus_area=priority.focus_area,
                user_prompt=(
                    "Practice this improvement priority "
                    "by making one clear argument."
                ),
                ai_prompt=(
                    "Challenge the user's argument and "
                    "ask them to strengthen their response."
                ),
            )

        return AdaptiveMiniDebate(
            topic=topic,
            focus_area=priority.focus_area,
            user_prompt=guidance["user_prompt"],
            ai_prompt=guidance["ai_prompt"],
        )

    @staticmethod
    def _extract_dimension(
        focus_area: str,
        priority: str,
    ) -> str:
        known_dimensions = (
            "argument quality",
            "communication quality",
            "evidence usage",
            "reasoning quality",
            "responsiveness",
        )

        for dimension in known_dimensions:
            if dimension in focus_area:
                return dimension

        normalized_priority = priority.strip().lower()

        for dimension in known_dimensions:
            if dimension in normalized_priority:
                return dimension

        return ""