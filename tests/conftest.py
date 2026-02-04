# tests/conftest.py
from __future__ import annotations

import pytest
import yaml
from pathlib import Path
from typing import Any, Callable, Literal, Optional, Protocol, TypedDict


# --- Single source of truth for package identifiers ---
PKGS: dict[str, str] = {
    "ARTIFACTS": "brooklyn-data/dbt_artifacts",
    "AUTOMATE_DV": "Datavault-UK/automate_dv",
    "UTILS": "dbt-labs/dbt_utils",
    "EXPECTATIONS": "metaplane/dbt_expectations",
}

# Constrain the valid keys at type-check time
PkgKey = Literal["ARTIFACTS", "AUTOMATE_DV", "UTILS", "EXPECTATIONS"]

# Version ranges centralised and keyed by PKGS keys (not raw strings)
PKG_VERSIONS: dict[PkgKey, tuple[str, str]] = {
    "ARTIFACTS": (">=2.10.0", "<2.11.0"),
    "AUTOMATE_DV": (">=0.11.4", "<0.12.0"),
    "UTILS": (">=1.3.3", "<1.4.0"),
    "EXPECTATIONS": (">=0.10.10", "<0.11.0"),
}

PKG_ORDER: list[PkgKey] = ["ARTIFACTS", "AUTOMATE_DV", "UTILS", "EXPECTATIONS"]


# ---------------- small utilities ----------------


def _load_yaml(path: Path) -> dict:
    """
    Load a YAML file and return the parsed Python structure.

    - Asserts that the file exists to fail fast with a helpful error message.
    - Uses `yaml.safe_load`, so the return value is typically a `dict` (or `list`).

    Parameters
    ----------
    path : Path
        Full path to the YAML file.

    Returns
    -------
    dict
        Parsed YAML content.

    Raises
    ------
    AssertionError
        If the file does not exist.
    """
    assert path.exists(), f"Expected file not found: {path}"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class PackageSpec(TypedDict):
    """
    Expected entry in `packages.yml`.

    Keys
    ----
    package : str
        Fully-qualified dbt package name (e.g. "dbt-labs/dbt_utils")
    version : list[str]
        Two-element list expressing a range, e.g. [">=1.3.3", "<1.4.0"]
    """

    package: str
    version: list[str]


def _expected_packages(
    *,
    with_utils: bool,
    with_artifacts: bool,
    with_expectations: bool,
    with_automate_dv: bool,
) -> Optional[list[PackageSpec]]:
    """
    Build the expected `packages.yml` content based on feature flags.

    - Uses central constants (`PKGS`, `PKG_VERSIONS`, `PKG_ORDER`) so strings and versions
      are defined once.
    - Returns `None` when no packages should be present (the template renders `packages: null`).

    Parameters
    ----------
    with_utils : bool
        Whether dbt-utils should be included.
    with_artifacts : bool
        Whether dbt-artifacts should be included.
    with_expectations : bool
        Whether dbt-expectations should be included.
    with_automate_dv : bool
        Whether automate_dv should be included.

    Returns
    -------
    Optional[list[PackageSpec]]
        The list of `{package, version}` dictionaries in a stable order, or `None`
        if no packages are expected.
    """
    include_keys: list[PkgKey] = []

    if with_artifacts:
        include_keys.append("ARTIFACTS")
    if with_automate_dv:
        include_keys.append("AUTOMATE_DV")
    if with_utils:
        include_keys.append("UTILS")
    if with_expectations:
        include_keys.append("EXPECTATIONS")

    # Sanity guard: ensure we have versions for everything we’re including
    missing = [k for k in include_keys if k not in PKG_VERSIONS]
    assert not missing, f"Missing PKG_VERSIONS entries for: {missing}"

    packages: list[PackageSpec] = [
        {
            "package": PKGS[key],  # Pkg name from single source of truth
            "version": list(PKG_VERSIONS[key]),  # e.g. [">=2.10.0", "<2.11.0"]
        }
        for key in PKG_ORDER
        if key in include_keys
    ]
    return packages or None


class VarsSpec(TypedDict):
    """
    Expected shape of the `vars` block in dbt_project.yml when Automate DV is enabled.
    """

    project_version: str
    hash: str
    concat_string: str
    null_placeholder_string: str
    hash_content_casing: str
    enable_native_hashes: bool


def _expected_vars(with_automate_dv: bool) -> Optional[VarsSpec]:
    """
    Build the expected `vars` block for dbt_project.yml.

    - When Automate DV is disabled, returns the `vars` keys that should be absent.
    - When enabled, returns the full VarsSpec with the exact keys/values the template should render.

    Parameters
    ----------
    with_automate_dv : bool
        Whether Automate DV is enabled.

    Returns
    -------
    Optional[VarsSpec]
        The vars mapping present.
    """
    if not with_automate_dv:
        return VarsSpec(project_version="0.0.0")
    else:
        return VarsSpec(
            project_version="0.0.0",
            hash="SHA",
            concat_string="||",
            null_placeholder_string="^^",
            hash_content_casing="UPPER",
            enable_native_hashes=True,
        )


# ---------------- fixtures returning callables ----------------


# Describe the Result object returned by pytest-copie
class AnswersSpec(TypedDict):
    """
    Expected shape of `result.answers` saved by Copier.
    """

    project_name: str
    data_product_schema: str
    with_dbt_utils: bool
    with_dbt_artifacts: bool
    with_dbt_expectations: bool
    with_automate_dv: bool


class CopierResult(Protocol):
    """
    Minimal protocol for the result object returned by pytest-copie.

    This lets type checkers validate attribute access without importing a concrete class.
    Expand the protocol if you use more attributes in other helpers.
    """

    answers: AnswersSpec
    exit_code: int
    exception: Optional[BaseException]
    project_dir: object  # pathlib.Path-like (we only need .is_dir())
    stdout: str | bytes | None
    stderr: str | bytes | None


@pytest.fixture
def assert_generation_ok() -> Callable[[CopierResult], None]:
    """
    Return a callable that asserts a Copier generation succeeded.

    The callable validates that:
      - exit_code == 0
      - exception is None
      - project_dir exists

    On failure, it raises an AssertionError containing exit_code, exception,
    and any captured stdout/stderr to speed up debugging in CI.
    """

    def _assert(result: CopierResult) -> None:
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
def assert_answers() -> Callable[[CopierResult], None]:
    """
    Return a callable that asserts `result.answers` match expected defaults and flags.

    Parameters (to the returned callable)
    -------------------------------------
    result : CopierResult
        Copier result containing an `answers` mapping.
    with_utils, with_artifacts, with_expectations, with_automate_dv : bool
        Scenario flags the answers must agree with.
    """

    def _assert(
        result: CopierResult,
        *,
        with_utils: bool,
        with_artifacts: bool,
        with_expectations: bool,
        with_automate_dv: bool,
    ) -> None:
        ans = result.answers

        # Hard-coded defaults
        assert ans["project_name"] == "dbt_project"
        assert ans["data_product_schema"] == "default"

        # Feature flags
        assert bool(ans["with_dbt_utils"]) is bool(with_utils)
        assert bool(ans["with_dbt_artifacts"]) is bool(with_artifacts)
        assert bool(ans["with_dbt_expectations"]) is bool(with_expectations)
        assert bool(ans["with_automate_dv"]) is bool(with_automate_dv)

    return _assert


class PackagesYml(TypedDict, total=False):
    """
    Minimal typed view of packages.yml for the fields we assert on.
    """

    packages: Optional[list[PackageSpec]]  # None when template renders `packages: null`


@pytest.fixture
def assert_packages_yaml() -> Callable[[Path], None]:
    """
    Return a callable that validates `packages.yml` against central expectations.

    Behavior
    --------
    - If no packages are expected, asserts the parsed value is `None`
      (your template renders `packages: null`).
    - Otherwise, validates that the full list (including order) matches the
      output of `_expected_packages(...)`.
    - Optionally guards against unknown package names (template drift).
    """

    def _assert(
        project_dir: Path,
        *,
        with_utils: bool,
        with_artifacts: bool,
        with_expectations: bool,
        with_automate_dv: bool,
    ) -> None:
        data_raw = _load_yaml(project_dir / "packages.yml")

        expected = _expected_packages(
            with_utils=with_utils,
            with_artifacts=with_artifacts,
            with_expectations=with_expectations,
            with_automate_dv=with_automate_dv,
        )

        # When no packages are selected, the template writes `packages: null`
        actual = data_raw.get("packages")

        if expected is None:
            assert actual is None, f"Expected packages: null, got: {actual!r}"
            return

        # drift guard: ensure template did not introduce unknown package names
        actual_names = [p.get("package") for p in (actual or [])]
        known_names = set(PKGS.values())
        unknown = [name for name in actual_names if name not in known_names]
        assert not unknown, f"Unexpected package(s) in template: {unknown}"

        assert actual == expected, (
            f"packages.yml mismatch:\nACTUAL:   {actual}\nEXPECTED: {expected}"
        )

    return _assert


class ModelsConfig(TypedDict, total=False):
    """
    Minimal typed view for `models` section of dbt_project.yml.

    We keep `dbt_artifacts` as a generic mapping to allow keys like `+schema`
    that are not valid Python identifiers (accessed dynamically at runtime).
    """

    dbt_artifacts: dict[str, Any]  # using dict to avoid '+schema' identifier issues


class DbtProjectYml(TypedDict, total=False):
    """
    Minimal typed view of dbt_project.yml for the fields we assert on.
    """

    vars: VarsSpec
    models: ModelsConfig
    # More keys can be added if required: name, version, profile, etc.


@pytest.fixture
def assert_dbt_project_yaml() -> Callable[[Path], None]:
    """
    Return a callable that validates `dbt_project.yml` for vars, the
    `models.dbt_artifacts` block, and the `on-run-end` hook.

    Behavior
    --------
    - Compares to `_expected_vars(...)`.
    - If artifacts are enabled, asserts the `models.dbt_artifacts` mapping exists
      and has `+schema: dbt_artifacts`; otherwise asserts it is absent.
    - If artifacts are enabled, asserts the `on-run-end` hook uploads dbt artifacts;
      otherwise asserts the key is absent.
    """

    def _assert(
        project_dir: Path,
        *,
        with_artifacts: bool,
        with_automate_dv: bool,
    ) -> None:
        data_raw = _load_yaml(project_dir / "dbt_project.yml")
        # Optional narrow typing:
        # project: DbtProjectYml = typing.cast(DbtProjectYml, data_raw)

        # ---- vars block ----
        vars_expected = _expected_vars(with_automate_dv)
        assert data_raw.get("vars") == vars_expected, (
            f"'vars' mismatch.\nACTUAL:   {data_raw.get('vars')}\nEXPECTED: {vars_expected}"
        )

        # ---- models -> dbt_artifacts ----
        models = data_raw.get("models", {})
        if with_artifacts:
            assert isinstance(models, dict), (
                f"'models' should be a mapping; got: {type(models).__name__}"
            )
            assert "dbt_artifacts" in models, (
                f"Expected 'models.dbt_artifacts' block, got: {list(models.keys())}"
            )
            artifacts_cfg = models["dbt_artifacts"]
            assert isinstance(artifacts_cfg, dict), (
                f"'models.dbt_artifacts' should be a mapping; got: {type(artifacts_cfg).__name__}"
            )
            # dbt uses '+schema' key in YAML; compare exactly as rendered
            assert artifacts_cfg.get("+schema") == "dbt_artifacts", (
                f"Expected models.dbt_artifacts['+schema'] == 'dbt_artifacts', got: {artifacts_cfg.get('+schema')!r}"
            )
        else:
            # If artifacts are disabled, the block shouldn’t exist
            assert "dbt_artifacts" not in models, (
                "'models.dbt_artifacts' should not be present"
            )

        # ---- models -> automate_dv ----
        project_models_cfg = models["dbt_project"]
        if with_automate_dv:
            assert isinstance(project_models_cfg, dict), (
                f"'models.dbt_project' should be a mapping; got: {type(project_models_cfg).__name__}"
            )
            assert "raw_vault" in project_models_cfg, (
                f"Expected 'models.dbt_project.raw_vault' block, got: {list(project_models_cfg.keys())}"
            )
            assert "stage" in project_models_cfg, (
                f"Expected 'models.dbt_project.stage' block, got: {list(project_models_cfg.keys())}"
            )
        else:
            # If automate_dv is disabled, these blocks shouldn’t exist
            assert "raw_vault" not in project_models_cfg, (
                "'models.dbt_project.raw_vault' should not be present"
            )
            assert "stage" not in project_models_cfg, (
                "'models.dbt_project.stage' should not be present"
            )

        # ---- on-run-end hook ----
        if with_artifacts:
            expected_hook = ["{{ dbt_artifacts.upload_results(results) }}"]
            assert data_raw.get("on-run-end") == expected_hook, (
                f"'on-run-end' mismatch.\nACTUAL:   {data_raw.get('on-run-end')}\nEXPECTED: {expected_hook}"
            )
        else:
            assert "on-run-end" not in data_raw, (
                "Unexpected 'on-run-end' when artifacts are disabled"
            )

    return _assert


@pytest.fixture
def assert_model_folders() -> Callable[[Path], None]:
    def _assert(
        project_dir: Path,
        *,
        with_automate_dv: bool,
    ) -> None:
        models_dir = project_dir / "src" / "models"
        raw_vault_dir = models_dir / "raw_vault"
        stage_dir = models_dir / "stage"

        if with_automate_dv:
            assert raw_vault_dir.exists(), f"Expected to find: {raw_vault_dir}"
            assert raw_vault_dir.is_dir(), f"Expected a directory: {raw_vault_dir}"
            assert stage_dir.exists(), f"Expected to find: {stage_dir}"
            assert stage_dir.is_dir(), f"Expected a directory: {stage_dir}"
        else:
            assert not raw_vault_dir.exists(), (
                f"Did not expect to find: {raw_vault_dir}"
            )
            assert not stage_dir.exists(), f"Did not expect to find: {stage_dir}"

            # And no sub-directories should exist within src/models
            if models_dir.exists():
                unexpected_dirs = [p for p in models_dir.iterdir() if p.is_dir()]
                assert not unexpected_dirs, (
                    "Did not expect any subdirectories in "
                    f"{models_dir}, but found: "
                    f"{', '.join(str(p) for p in unexpected_dirs)}"
                )

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
    Parametrized scenario provider.

    Yields
    ------
    tuple
        (name, extra_answers, with_utils, with_artifacts, with_expectations, with_automate_dv)

    Notes
    -----
    - When you call `copie.copy`, pass `extra_answers or {}` to avoid sending None
      (Copier expects a dict for user defaults).
    - Add more tuples here to extend feature coverage.
    """
    return request.param
