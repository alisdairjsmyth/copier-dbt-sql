# tests/test_kebab_project_name.py
from __future__ import annotations

import re
from pathlib import Path
import pytest
import tomllib


def to_kebab(value: str) -> str:
    """
    Convert a human-friendly project name to kebab-case:

    - Lowercase
    - Replace spaces and underscores with hyphens
    - Remove any char that's not [a-z0-9-]
    - Collapse consecutive hyphens
    - Strip leading/trailing hyphens
    """
    s = value.lower()
    s = re.sub(r"[ _]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


def _load_pyproject(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return tomllib.loads(text)


@pytest.mark.parametrize(
    "human_name, expected_kebab",
    [
        ("my_project", "my-project"),
        ("project", "project"),
        ("Already-Kebab", "already-kebab"),
        ("Mixed__Case", "mixed-case"),
        ("A__b___C____d_____E", "a-b-c-d-e"),
    ],
)
def test_kebab_name_in_generated_toml(copie, human_name: str, expected_kebab: str):
    """
    GIVEN a Copier template
    WHEN we `copie.copy` with a particular `project_name`
    THEN the generated project's distribution name in TOML is the kebab-case of that `project_name`.

    This test inspects Copier OUTPUT (the generated project directory), not the template itself.
    """
    # 1) Generate a project from the template with the specified project_name
    result = copie.copy(extra_answers={"project_name": human_name})
    assert result.exit_code == 0, f"Copier failed: {result.exception}"
    root: Path = result.project_dir

    # 2) Locate the TOML written by the template.

    pyproject = root / "pyproject.toml"
    assert pyproject.exists(), (
        "Expected pyproject.toml to be generated, but it was not found"
    )

    # 3) Read [project].name
    data = _load_pyproject(pyproject)
    project_table = data.get("project")
    assert isinstance(project_table, dict), f"Missing [project] table in {pyproject}"
    toml_name = project_table.get("name")
    assert isinstance(toml_name, str) and toml_name, (
        f"Missing or invalid [project].name in {pyproject}"
    )

    # 4) Assert it equals the kebab-case of the Copier answer
    assert toml_name == expected_kebab, (
        f"Expected [project].name '{expected_kebab}' from project_name='{human_name}', got '{toml_name}'"
    )

    assert to_kebab(human_name) == expected_kebab
