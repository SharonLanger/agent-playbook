"""Load the workflow package before importing framework examples."""

from importlib import import_module

import_module("agent_playbook.workflows")
