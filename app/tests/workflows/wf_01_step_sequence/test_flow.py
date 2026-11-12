from unittest.mock import patch

import pytest

from agent_playbook.workflows.wf_01_step_sequence import steps
from agent_playbook.workflows.wf_01_step_sequence.flow import StepSequenceFlow


def test_real_kickoff_and_order(capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        StepSequenceFlow(tracing=False, suppress_flow_events=True).kickoff()
        == "[Hello, workflow!]"
    )
    assert capsys.readouterr().out.splitlines() == [
        f"[WF-01] {step} {event}"
        for step in ("produce", "decorate", "finish")
        for event in ("started", "finished")
    ]


def test_failure_skips_finish(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(
        steps, "decorate_message", side_effect=RuntimeError("exercise failure")
    ):
        with pytest.raises(RuntimeError, match="exercise failure"):
            StepSequenceFlow(tracing=False, suppress_flow_events=True).kickoff()
    output = capsys.readouterr().out
    assert "[WF-01] produce finished" in output
    assert "[WF-01] decorate started" in output
    assert "[WF-01] decorate finished" not in output
    assert "[WF-01] finish started" not in output
