"""WF-03 application contract around its CrewAI flow."""

from typing import Mapping

from pydantic import ValidationError

from agent_playbook.config.diagnostics import validation_fields
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.models import CrewAISettings
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowInputError
from agent_playbook.workflows.wf_03_conditional_route.config import (
    ConditionalRouteConfig,
)
from agent_playbook.workflows.wf_03_conditional_route.state import Decision


class ConditionalRouteWorkflow(Workflow[Decision]):
    def __init__(
        self, *, settings: CrewAISettings, config: Mapping[str, object]
    ) -> None:
        super().__init__(settings=settings, config=config)
        try:
            self._defaults = ConditionalRouteConfig.model_validate(config).defaults
        except ValidationError as error:
            raise ConfigurationError(
                f"Invalid settings: {validation_fields(error)}."
            ) from None

    def _prepare(self, data: Mapping[str, object]) -> None:
        from agent_playbook.workflows.wf_03_conditional_route.state import (
            ScoreInput,
            ScoreState,
        )

        try:
            score = ScoreInput.model_validate({**self._defaults.model_dump(), **data})
        except ValidationError as error:
            raise WorkflowInputError(
                f"Invalid input: {validation_fields(error)}."
            ) from error
        from agent_playbook.workflows.wf_03_conditional_route.flow import (
            ConditionalRouteFlow,
        )

        self._flow = ConditionalRouteFlow(
            initial_state=ScoreState(score=score.score),
            tracing=self._settings.tracing_enabled,
            suppress_flow_events=not self._settings.show_framework_events,
        )

    def _execute(self) -> object:
        return self._flow.kickoff()

    def _validate_output(self, output: object) -> Decision:
        if output != "pass" and output != "needs_work":
            raise TypeError("wf-03 output must be pass or needs_work.")
        return "pass" if output == "pass" else "needs_work"

    def _serialize_output(self) -> str:
        return self.result
