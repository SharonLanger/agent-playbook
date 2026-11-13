"""WF-01 application contract around its CrewAI flow."""

from typing import Mapping

from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.models import CrewAISettings
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowInputError
from agent_playbook.workflows.wf_01_step_sequence.flow import StepSequenceFlow


class StepSequenceWorkflow(Workflow[str]):
    def __init__(
        self, *, settings: CrewAISettings, config: Mapping[str, object]
    ) -> None:
        super().__init__(settings=settings, config=config)
        if config:
            raise ConfigurationError("step_sequence config must be empty.")

    def _prepare(self, data: Mapping[str, object]) -> None:
        if data:
            raise WorkflowInputError(
                "wf-01 accepts no input fields; use {} or omit --input."
            )
        self._flow = StepSequenceFlow(
            tracing=self._settings.tracing_enabled,
            suppress_flow_events=not self._settings.show_framework_events,
        )

    def _execute(self) -> object:
        return self._flow.kickoff()

    def _validate_output(self, output: object) -> str:
        if not isinstance(output, str):
            raise TypeError("wf-01 output must be a string.")
        return output

    def _serialize_output(self) -> str:
        return self.result
