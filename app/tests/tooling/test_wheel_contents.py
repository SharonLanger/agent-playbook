"""Distribution checks reject missing console contracts and checkout files."""

import zipfile
from pathlib import Path

import pytest

from tooling.release import verify_wheel_contents


@pytest.mark.parametrize("defect", [None, "entry", "runtime", "checkout"])
def test_distribution_contract(tmp_path: Path, defect: str | None) -> None:
    wheel = tmp_path / "sample.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr(
            "sample.dist-info/entry_points.txt",
            "[console_scripts]\nagent-playbook = "
            + ("bad:main" if defect == "entry" else "agent_playbook.cli:main")
            + "\n",
        )
        archive.writestr("agent_playbook/__init__.py", "")
        archive.writestr("agent_playbook/cli/__init__.py", "")
        if defect != "runtime":
            archive.writestr("agent_playbook/_build_info.py", 'SOURCE_COMMIT = "abc"')
        if defect == "checkout":
            archive.writestr("examples/private.py", "")
    if defect is None:
        verify_wheel_contents(wheel)
    else:
        with pytest.raises(RuntimeError):
            verify_wheel_contents(wheel)
