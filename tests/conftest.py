# tests/conftest.py
from __future__ import annotations

import pytest
import yaml
from pathlib import Path


# ---------------- small utilities ----------------


def _load_yaml(path: Path) -> dict:
    assert path.exists(), f"Expected file not found: {path}"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _expected_packages(
    *,
    with_utils: bool,
    with_artifacts: bool,
    with_expectations: bool,
    with_automate_dv: bool,
):
    pkgs = []
    if with_artifacts:
        pkgs.append(
            {
                "package": "brooklyn-data/dbt_artifacts",
                "version": [">=2.10.0", "<2.11.0"],
            }
        )
    if with_automate_dv:
        pkgs.append(
            {"package": "Datavault-UK/automate_dv", "version": [">=0.11.4", "<0.12.0"]}
        )
    if with_utils:
        pkgs.append({"package": "dbt-labs/dbt_utils", "version": [">=1.3.3", "<1.4.0"]})
    if with_expectations:
        pkgs.append(
            {
                "package": "metaplane/dbt_expectations",
                "version": [">=0.10.10", "<0.11.0"],
            }
        )
    return pkgs or None


def _expected_vars(with_automate_dv: bool):
    if not with_automate_dv:
        return None
    return {
        "hash": "SHA",
        "concat_string": "||",
        "null_placeholder_string": "^^",
        "hash_content_casing": "UPPER",
        "enable_native_hashes": True,
    }


# ---------------- fixtures returning callables ----------------


@pytest.fixture
def assert_generation_ok():
    def _assert(result) -> None:
        if result.exit_code != 0 or result.exception is not None:
            stdout = getattr(result, "stdout", "")
            stderr = getattr(result, "stderr", "")
            raise AssertionError(
                "Copier generation failed\n"
                f"exit_code={result.exit_code}\n"
                f"exception={result.exception}\n"
                f"stdout:\n{stdout}\n"
                f"stderr:\n{stderr}\n"
            )
        assert result.project_dir.is_dir()

    return _assert


@pytest.fixture
def assert_answers():
    def _assert(
        result, *, with_utils, with_artifacts, with_expectations, with_automate_dv
    ):
        ans = result.answers
        assert ans["project_name"] == "dbt_project"
        assert ans["data_product_schema"] == "default"
        assert bool(ans["with_dbt_utils"]) is bool(with_utils)
        assert bool(ans["with_dbt_artifacts"]) is bool(with_artifacts)
        assert bool(ans["with_dbt_expectations"]) is bool(with_expectations)
        assert bool(ans["with_automate_dv"]) is bool(with_automate_dv)

    return _assert


@pytest.fixture
def assert_packages_yaml():
    def _assert(
        project_dir: Path,
        *,
        with_utils,
        with_artifacts,
        with_expectations,
        with_automate_dv,
    ):
        data = _load_yaml(project_dir / "packages.yml")
        expected = _expected_packages(
            with_utils=with_utils,
            with_artifacts=with_artifacts,
            with_expectations=with_expectations,
            with_automate_dv=with_automate_dv,
        )
        if expected is None:
            assert data.get("packages") is None
        else:
            assert data.get("packages") == expected

    return _assert


@pytest.fixture
def assert_dbt_project_yaml():
    def _assert(project_dir: Path, *, with_artifacts, with_automate_dv):
        data = _load_yaml(project_dir / "dbt_project.yml")

        vars_expected = _expected_vars(with_automate_dv)
        if vars_expected is None:
            assert "vars" not in data
        else:
            assert data.get("vars") == vars_expected

        models = data.get("models", {})
        if with_artifacts:
            assert "dbt_artifacts" in models
            assert models["dbt_artifacts"]["+schema"] == "dbt_artifacts"
            assert "on-run-end" in data
            assert data["on-run-end"] == ["{{ dbt_artifacts.upload_results(results) }}"]
        else:
            assert "dbt_artifacts" not in models
            assert "on-run-end" not in data

    return _assert


# ---------------- scenario fixture (parametrized) ----------------


@pytest.fixture(
    params=[
        ("defaults", {}, True, True, False, False),
        (
            "all_true",
            {"with_dbt_expectations": True, "with_automate_dv": True},
            True,
            True,
            True,
            True,
        ),
        (
            "all_false",
            {"with_dbt_utils": False, "with_dbt_artifacts": False},
            False,
            False,
            False,
            False,
        ),
        (
            "inverse_options",
            {
                "with_dbt_utils": False,
                "with_dbt_artifacts": False,
                "with_dbt_expectations": True,
                "with_automate_dv": True,
            },
            False,
            False,
            True,
            True,
        ),
    ],
    ids=lambda p: p[0] if isinstance(p, tuple) else str(p),
)
def template_scenario(request):
    """
    Provides:
      name, extra_answers, with_utils, with_artifacts, with_expectations, with_automate_dv
    """
    return request.param
