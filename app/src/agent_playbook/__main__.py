"""Run default WF-01 directly through the source/installed application."""

from agent_playbook.cli.commands import present_workflow

if __name__ == "__main__":
    raise SystemExit(present_workflow())
