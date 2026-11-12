from agent_playbook.workflows.wf_01_step_sequence.steps import (
    decorate_message,
    make_message,
)


def test_message_and_decoration() -> None:
    assert make_message() == "Hello, workflow!"
    assert decorate_message(make_message()) == "[Hello, workflow!]"
    assert decorate_message("") == "[]"
