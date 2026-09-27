from debate_arena.debate.argument import Argument

from debate_arena.debate.argument_analyzer import (
    ArgumentAnalysis,
    ArgumentAnalyzer,
)

from debate_arena.debate.debate_analyzer import (
    DebateAnalysis,
    DebateAnalyzer,
)

from debate_arena.debate.debate_report import DebateReport

from debate_arena.debate.prompts import build_rebuttal_prompt

from debate_arena.debate.state import DebateState

from debate_arena.debate.strategy import DebateStrategy

from debate_arena.debate.strategy_selector import StrategySelector

from debate_arena.llm.client import LLMClient

from debate_arena.debate.round_performance import RoundPerformance

from debate_arena.debate.round_performance_analyzer import (
    RoundPerformanceAnalyzer,
)

from debate_arena.debate.debate_performance_pipeline import (
    DebatePerformancePipeline,
)

from debate_arena.debate.coaching_session_report import (
    CoachingSessionReport,
)

from debate_arena.debate.adaptive_mini_debate import (
    AdaptiveMiniDebate,
)

from debate_arena.debate.adaptive_mini_debate_analyzer import (
    AdaptiveMiniDebateAnalyzer,
)


class DebateEngine:

    def __init__(
        self,
        state: DebateState,
        llm: LLMClient | None = None,
        strategy_selector: StrategySelector | None = None,
        tts=None,
        argument_analyzer: ArgumentAnalyzer | None = None,
        debate_analyzer: DebateAnalyzer | None = None,
        round_performance_analyzer: RoundPerformanceAnalyzer | None = None,
        performance_pipeline: DebatePerformancePipeline | None = None,
    ):
        self.state = state

        self.llm = llm or LLMClient()

        self.strategy_selector = strategy_selector

        self.tts = tts

        self.argument_analyzer = (
            argument_analyzer
            or ArgumentAnalyzer(
                llm_client=self.llm
            )
        )

        self.debate_analyzer = (
            debate_analyzer
            or DebateAnalyzer(
                llm_client=self.llm
            )
        )

        self.round_performance_analyzer = (
            round_performance_analyzer
            or RoundPerformanceAnalyzer(
                argument_analyzer=self.argument_analyzer
            )
        )

        self.performance_pipeline = (
            performance_pipeline
            or DebatePerformancePipeline(
                llm_client=self.llm,
            )
        )

        # M9.9.5 — Adaptive follow-up mini-debate.
        self.adaptive_mini_debate_analyzer = (
            AdaptiveMiniDebateAnalyzer()
        )

        self.last_adaptive_mini_debate: (
            AdaptiveMiniDebate | None
        ) = None

        # M9.9.6 — Complete coaching session report.
        self.last_coaching_session_report: (
            CoachingSessionReport | None
        ) = None

        self.last_strategy: DebateStrategy | None = None

        self.last_argument_analysis: (
            ArgumentAnalysis | None
        ) = None

        self.last_debate_analysis: (
            DebateAnalysis | None
        ) = None

        self.last_debate_report: (
            DebateReport | None
        ) = None

        self.round_performances: list[
            RoundPerformance
        ] = []

    def is_user_turn(self) -> bool:
        return self.state.current_turn == "user"

    def is_ai_turn(self) -> bool:
        return self.state.current_turn == "ai"

    def submit_user_argument(
        self,
        argument: str,
    ) -> None:
        if not argument or not argument.strip():
            raise ValueError(
                "Argument cannot be empty."
            )

        if self.state.is_finished():
            raise RuntimeError(
                "Debate has finished."
            )

        if not self.is_user_turn():
            raise RuntimeError(
                "It is not the user's turn."
            )

        cleaned_argument = argument.strip()

        analysis = self.argument_analyzer.analyze(
            cleaned_argument
        )

        self.last_argument_analysis = analysis

        user_argument = Argument(
            speaker="user",
            text=cleaned_argument,
            round=self.state.current_round,
            turn=len(
                self.state.user_arguments
            ) + 1,
        )

        self.state.add_user_argument(
            user_argument
        )

        self.state.current_turn = "ai"

    def submit_ai_argument(
        self,
        argument: str,
    ) -> None:
        if not argument or not argument.strip():
            raise ValueError(
                "Argument cannot be empty."
            )

        if self.state.is_finished():
            raise RuntimeError(
                "Debate has finished."
            )

        if not self.is_ai_turn():
            raise RuntimeError(
                "It is not the AI's turn."
            )

        cleaned_argument = argument.strip()

        ai_argument = Argument(
            speaker="ai",
            text=cleaned_argument,
            round=self.state.current_round,
            turn=len(
                self.state.ai_arguments
            ) + 1,
        )

        self.state.add_ai_argument(
            ai_argument
        )

        self.state.current_turn = "user"

    def start_new_round(self) -> None:
        if self.state.is_finished():
            raise RuntimeError(
                "Debate has finished."
            )

        if len(self.state.user_arguments) == 0:
            raise RuntimeError(
                "Cannot start a new round before the user "
                "has submitted an argument."
            )

        if len(self.state.ai_arguments) < len(
            self.state.user_arguments
        ):
            raise RuntimeError(
                "Cannot start a new round before the AI "
                "has responded."
            )

        self.state.advance_round()

        self.state.current_turn = "user"

    def complete_round(self) -> None:
        if self.state.is_finished():
            return

        self.start_new_round()

    def end_debate(self) -> None:
        """
        End the debate early and mark the current state as finished.

        The existing state model treats a debate as finished when
        ``current_round`` moves beyond ``max_rounds``. We reuse that
        rule here so normal completion and manual completion share the
        same report-generation path.
        """
        if self.state.is_finished():
            return

        if not self.state.user_arguments:
            raise RuntimeError(
                "Cannot end the debate before the user has submitted an argument."
            )

        self.state.current_round = (
            self.state.max_rounds + 1
        )
        self.state.current_turn = "user"

    def generate_ai_rebuttal(self) -> str:
        if self.state.is_finished():
            raise RuntimeError(
                "Debate has finished."
            )

        if not self.is_ai_turn():
            raise RuntimeError(
                "It is not the AI's turn."
            )

        if not self.state.user_arguments:
            raise RuntimeError(
                "No user argument is available."
            )

        latest_argument = (
            self.state.user_arguments[-1].text
        )

        context = self.state.get_context()

        if self.strategy_selector is not None:
            selected_strategy = (
                self.strategy_selector.select(
                    context=context,
                    latest_argument=latest_argument,
                    analysis=self.last_argument_analysis,
                )
            )

        elif self.last_strategy is not None:
            selected_strategy = self.last_strategy

        else:
            selected_strategy = (
                DebateStrategy.DIRECT_COUNTER
            )

        self.last_strategy = selected_strategy

        prompt = build_rebuttal_prompt(
            context=context,
            latest_argument=latest_argument,
            strategy=selected_strategy.value,
        )

        response = (
            self.llm.generate_debate_response(
                prompt
            )
        )

        if self.strategy_selector is None:
            if response.strategy is not None:
                selected_strategy = response.strategy

                self.last_strategy = (
                    response.strategy
                )

        rebuttal = response.rebuttal

        if not rebuttal or not rebuttal.strip():
            raise RuntimeError(
                "LLM returned an empty rebuttal."
            )

        return rebuttal.strip()

    def generate_and_submit_ai_rebuttal(
        self,
    ) -> str:
        rebuttal = (
            self.generate_ai_rebuttal()
        )

        self.submit_ai_argument(
            rebuttal
        )

        return rebuttal

    def speak_ai_rebuttal(
        self,
        rebuttal: str,
    ) -> None:
        if self.tts is None:
            return

        if not rebuttal or not rebuttal.strip():
            return

        self.tts.speak(
            rebuttal
        )

    def generate_debate_report(
        self,
    ) -> DebateReport:
        """
        Generate and cache the final structured report
        for a completed debate.

        The report combines:

        - deterministic debate analysis
        - round-by-round performance analysis
        - semantic performance interpretation
        - semantic moment interpretation
        - adaptive coaching
        - complete coaching session report
        """

        if not self.state.is_finished():
            raise RuntimeError(
                "Cannot generate a debate report before "
                "the debate has finished."
            )

        # Return the existing report if one has already
        # been generated for this completed debate.
        if self.last_debate_report is not None:
            return self.last_debate_report

        # --------------------------------------------------
        # 1. Generate the existing debate analysis
        # --------------------------------------------------

        analysis = (
            self.debate_analyzer.analyze(
                self.state
            )
        )

        self.last_debate_analysis = analysis

        rounds_completed = min(
            len(self.state.user_arguments),
            len(self.state.ai_arguments),
        )

        # --------------------------------------------------
        # 2. Run the M9.5–M9.9 performance pipeline
        # --------------------------------------------------

        semantic_performance = None

        semantic_moments = None

        adaptive_mini_debate = None

        coaching_session_report = None

        if self.round_performances:

            performance_analysis = (
                self.performance_pipeline.analyze(
                    self.round_performances
                )
            )

            semantic_performance = (
                performance_analysis
            )

            semantic_moments = (
                self.performance_pipeline.last_moment_analysis
            )

            # M9.9.5 — Get the personalized
            # improvement priorities generated
            # by the coaching pipeline.
            improvement_priorities = getattr(
                self.performance_pipeline,
                "last_improvement_priorities",
                None,
            )

            # Build one focused adaptive mini-debate
            # around the highest-priority improvement area.
            if improvement_priorities:
                adaptive_mini_debate = (
                    self.adaptive_mini_debate_analyzer.analyze(
                        priority=improvement_priorities[0],
                        topic=self.state.topic,
                    )
                )

            # M9.9.6 — Retrieve the complete coaching
            # session report produced by the pipeline.
            coaching_session_report = getattr(
                self.performance_pipeline,
                "last_coaching_session_report",
                None,
            )

        # Cache the adaptive mini-debate.
        self.last_adaptive_mini_debate = (
            adaptive_mini_debate
        )

        # Cache the complete coaching session report.
        self.last_coaching_session_report = (
            coaching_session_report
        )

        # --------------------------------------------------
        # 3. Build the final report
        # --------------------------------------------------

        report = DebateReport(
            topic=self.state.topic,

            user_position=(
                self.state.user_position
            ),

            ai_position=(
                self.state.ai_position
            ),

            rounds_completed=rounds_completed,

            summary=analysis.summary,

            strongest_argument=(
                analysis.strongest_argument
            ),

            weakest_argument=(
                analysis.weakest_argument
            ),

            strengths=list(
                analysis.strengths
            ),

            weaknesses=list(
                analysis.weaknesses
            ),

            evidence_usage=(
                analysis.evidence_usage
            ),

            consistency=(
                analysis.consistency
            ),

            responsiveness=(
                analysis.responsiveness
            ),

            recommendations=list(
                analysis.recommendations
            ),

            semantic_performance=(
                semantic_performance
            ),

            semantic_moments=(
                semantic_moments
            ),

            # M9.9.5 — Adaptive follow-up
            # mini-debate.
            adaptive_mini_debate=(
                adaptive_mini_debate
            ),

            # M9.9.6 — Complete coaching
            # session report.
            coaching_session_report=(
                coaching_session_report
            ),
        )

        # --------------------------------------------------
        # 4. Cache the completed report
        # --------------------------------------------------

        self.last_debate_report = report

        return report

    def get_state(
        self,
    ) -> DebateState:
        return self.state

    def get_history(
        self,
    ) -> list[Argument]:
        return self.state.get_history()

    def get_context(
        self,
    ) -> str:
        return self.state.get_context()

    def is_finished(
        self,
    ) -> bool:
        return self.state.is_finished()

    def get_current_round(
        self,
    ) -> int:
        return self.state.current_round

    def get_current_turn(
        self,
    ) -> str:
        return self.state.current_turn

    def get_last_strategy(
        self,
    ) -> DebateStrategy | None:
        return self.last_strategy

    def get_last_argument_analysis(
        self,
    ) -> ArgumentAnalysis | None:
        return self.last_argument_analysis

    def get_last_debate_analysis(
        self,
    ) -> DebateAnalysis | None:
        return self.last_debate_analysis

    def get_last_debate_report(
        self,
    ) -> DebateReport | None:
        return self.last_debate_report