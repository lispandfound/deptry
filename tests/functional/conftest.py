from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

import pytest
import xdist

from tests.functional.utils import DEPTRY_WHEEL_DIRECTORY
from tests.utils import PDMVenvFactory, PipVenvFactory, PoetryVenvFactory


def pytest_sessionstart(session: pytest.Session) -> None:
    # When running the tests on multiple workers with pytest-xdist, the hook will be run several times:
    # - once from "master" node, when test suite starts
    # - X times (where X is the number of workers), when tests start in each worker
    # We only want to run the hook once, so we explicitly skip the hook if running on a pytest-xdist worker.
    if xdist.is_xdist_worker(session):
        return None

    deptry_wheel_path = Path(DEPTRY_WHEEL_DIRECTORY)

    print(f"Building `deptry` wheel in {deptry_wheel_path} to use it on functional tests...")  # noqa: T201

    subprocess.run(
        shlex.split(f"pdm build --no-sdist --dest {deptry_wheel_path}", posix=sys.platform != "win32"),
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.fixture(scope="session")
def pdm_venv_factory(tmp_path_factory: pytest.TempPathFactory) -> PDMVenvFactory:
    return PDMVenvFactory(tmp_path_factory.getbasetemp() / "venvs")


@pytest.fixture(scope="session")
def poetry_venv_factory(tmp_path_factory: pytest.TempPathFactory) -> PoetryVenvFactory:
    return PoetryVenvFactory(tmp_path_factory.getbasetemp() / "venvs")


@pytest.fixture(scope="session")
def pip_venv_factory(tmp_path_factory: pytest.TempPathFactory) -> PipVenvFactory:
    return PipVenvFactory(tmp_path_factory.getbasetemp() / "venvs")
