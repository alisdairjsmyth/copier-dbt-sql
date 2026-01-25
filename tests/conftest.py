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
    assert path.exists(), f"Expected file not found: {path}"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class PackageSpec(TypedDict):
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
    Build the expected 'packages' list (or None) for packages.yml.

    Returns:
        None when no packages are expected (i.e., template renders `packages: null`),
        otherwise a list of {package, version} dicts in a stable order.
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
    hash: str
    concat_string: str
    null_placeholder_string: str
    hash_content_casing: str
    enable_native_hashes: bool


def _expected_vars(with_automate_dv: bool) -> Optional[VarsSpec]:
    if not with_automate_dv:
        return None
    return VarsSpec(
        hash="SHA",
        concat_string="||",
        null_placeholder_string="^^",
        hash_content_casing="UPPER",
        enable_native_hashes=True,
    )


# ---------------- fixtures returning callables ----------------


# Describe the Result object returned by pytest-copie
class AnswersSpec(TypedDict):
    project_name: str
    data_product_schema: str
    with_dbt_utils: bool
    with_dbt_artifacts: bool
    with_dbt_expectations: bool
    with_automate_dv: bool


class CopierResult(Protocol):
    answers: AnswersSpec
    exit_code: int
    exception: Optional[BaseException]
    project_dir: object  # pathlib.Path-like (we only need .is_dir())
    stdout: str | bytes | None
    stderr: str | bytes | None


@pytest.fixture
def assert_generation_ok() -> Callable[[CopierResult], None]:
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
    packages: Optional[list[PackageSpec]]  # None when template renders `packages: null`


@pytest.fixture
def assert_packages_yaml() -> Callable[[Path], None]:
    """
    Fixture returning a callable that validates packages.yml
    against centrally-defined expectations.
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
    dbt_artifacts: dict[str, Any]  # using dict to avoid '+schema' identifier issues


class DbtProjectYml(TypedDict, total=False):
    vars: VarsSpec
    models: ModelsConfig
    # More keys can be added if required: name, version, profile, etc.


@pytest.fixture
def assert_dbt_project_yaml() -> Callable[[Path], None]:
    """
    Fixture returning a callable that validates dbt_project.yml
    for vars, models->dbt_artifacts, and on-run-end.
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
        if vars_expected is None:
            assert "vars" not in data_raw, (
                f"Expected no 'vars' block, got: {data_raw.get('vars')!r}"
            )
        else:
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
