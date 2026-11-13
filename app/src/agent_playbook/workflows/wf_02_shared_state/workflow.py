"""WF-02 application contract around its CrewAI flow."""

from typing import Mapping

from pydantic import ValidationError

from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.models import CrewAISettings
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowInputError
from agent_playbook.workflows.wf_02_shared_state.config import SharedStateConfig
from agent_playbook.workflows.wf_02_shared_state.flow import SharedStateFlow
from agent_playbook.workflows.wf_02_shared_state.state import NumberInput, NumberState


class SharedStateWorkflow(Workflow[int]):
    def __init__(
        self, *, settings: CrewAISettings, config: Mapping[str, object]
    ) -> None:
        super().__init__(settings=settings, config=config)
        try:
            self._defaults = SharedStateConfig.model_validate(config).defaults
        except ValidationError as error:
            fields = "; ".join(
                ".".join(str(part) for part in item["loc"])
                for item in error.errors(
                    include_input=False, include_context=False, include_url=False
                )
            )
            raise ConfigurationError(
                f"Invalid shared_state config fields: {fields}."
            ) from None

    def _prepare(self, data: Mapping[str, object]) -> None:
        try:
            numbers = NumberInput.model_validate(
                {**self._defaults.model_dump(), **data}
            )
        except ValidationError as error:
            fields = "; ".join(
                ".".join(str(part) for part in item["loc"])
                for item in error.errors(
                    include_input=False, include_context=False, include_url=False
                )
            )
            raise WorkflowInputError(
                f"Invalid wf-02 input fields: {fields}."
            ) from error
        self._flow = SharedStateFlow(
            initial_state=NumberState(
                initial=numbers.initial,
                increment=numbers.increment,
                multiplier=numbers.multiplier,
            ),
            tracing=self._settings.tracing_enabled,
            suppress_flow_events=not self._settings.show_framework_events,
        )

    def _execute(self) -> object:
        return self._flow.kickoff()

    def _validate_output(self, output: object) -> int:
        if not isinstance(output, int) or isinstance(output, bool):
            raise TypeError("wf-02 output must be an integer.")
        return output

    def _serialize_output(self) -> str:
        return str(self.result)
