"""Expected Pyright failures are isolated from the normal strict type gate."""

import subprocess
import sys
from pathlib import Path

from agent_playbook.application.workflow_registry import workflow_registry
from agent_playbook.workflows.contracts import Workflow
from tests.application.test_followup_boundaries import SETTINGS, Review, RichWorkflow


def concrete_type_contract() -> tuple[int, ...]:
    known: Workflow[Review] = RichWorkflow(settings=SETTINGS, config={})
    known.prepare({})
    known.validate_output(known.execute())
    registry: dict[str, type[Workflow[object]]] = {"rich": RichWorkflow}
    registry.update(workflow_registry())
    return known.result.details


def test_negative_contract_diagnostics(tmp_path: Path) -> None:
    source = tmp_path / "negative_contract.py"
    source.write_text("""# pyright: strict
from typing import Mapping
from agent_playbook.workflows.contracts import Workflow
class Bad(Workflow[int]):
    def prepare(self, data: Mapping[str, object]) -> None: ...
    def _prepare(self, data: Mapping[str, object]) -> None: ...
    def _execute(self) -> object: return 1
    def _validate_output(self, output: object) -> str: return "x"
    def _serialize_output(self) -> str: return "x"
def bad_assignment(workflow: Workflow[int]) -> None:
    result: str = workflow.result
""")
    python = Path(sys.executable)
    result = subprocess.run(
        [str(python), "-m", "pyright", "--pythonpath", str(python), str(source)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode != 0
    assert "cannot override final method" in result.stdout
    assert 'Method "_validate_output" overrides' in result.stdout
    assert "reportAssignmentType" in result.stdout
