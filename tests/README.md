# Tests Guide
This folder contains a **typed, fixture‑driven test harness** for validating a Copier template that generates a dbt project. Helpers in conftest.py centralize common expectations (package names, version ranges, dbt config) and expose **fixture‑as‑callable** assertions so individual tests stay concise and consistent.

## File layout
```
tests/
├─ conftest.py            # helpers, types, fixtures, centralised expectations
├─ test_template.py       # single parametrized test using the helpers
└─ README.md              # (this file)
```

## Running tests
From the repository root:
```
uv run pytest -q
```

## Key ideas

- **Single source of truth** for package **names** and **version ranges**:

  - `PKGS`, `PKG_VERSIONS`, and `PKG_ORDER` live in `conftest.py`
  - `_expected_packages(...)` reads those constants to build expectations
- **Typed test harness**:

  - `TypedDict` for YAML structures like `PackageSpec`, `VarsSpec`
  - `Protocol` for the Copier `Result` so we can type attribute access
- **Fixture‑as‑callable assertions**:

  - `assert_generation_ok`, `assert_answers`, `assert_packages_yaml`, `assert_dbt_project_yaml`
  - Call them inside your tests with keyword args to match scenarios

## Helper fixtures & builders
Below are concise descriptions (docstrings are embedded in source).
### `load_yaml`
Load and parse a YAML file, asserting it exists first.

**Signature**:
```
def load_yaml(path: Path) -> dict
```
**Use when**: Reading `packages.yml`, `dbt_project.yml`, etc.

### `assert_generation_ok`
Checks `copie.copy(...)` succeeded, raising a detailed assertion on failure (exit code, exception, stdout/stderr).

**Signature**:
```
@pytest.fixture
def assert_generation_ok() -> Callable[[CopierResult], None]
```
**Example**:
```
result = copie.copy(extra_answers=extra or {})assert_generation_ok(result)
```

### `assert_answers`
Validates defaults and boolean flags in `result.answers`.

**Signature**:
```
@pytest.fixture
def assert_answers() -> Callable[[AnswersResult], None]
```
**Example**:
```
assert_answers(
    result,
    with_utils=True,
    with_artifacts=True,
    with_expectations=False,
    with_automate_dv=False,
)
```

### `assert_packages_yaml`
Validates `packages.yml` against centrally defined expectations:

- If nothing is selected, expects `packages: null` (parsed as `None`)
- Otherwise matches full list (order + values)

**Signature**:
```
@pytest.fixture
def assert_packages_yaml() -> Callable[[Path], None]
```
**Example**:
```
assert_packages_yaml(
    result.project_dir,
    with_utils=True,
    with_artifacts=True,
    with_expectations=False,
    with_automate_dv=False,
)
```

### `assert_dbt_project_yaml`
Validates dbt_project.yml:

- `vars` present/absent based on `with_automate_dv`
- `models.dbt_artifacts["+schema"] == "dbt_artifacts"` when artifacts are enabled
- `on-run-end` hook present only when artifacts are enabled

**Signature**:
```
@pytest.fixture
def assert_dbt_project_yaml() -> Callable[[Path], None]
```
**Example**:
```
assert_dbt_project_yaml(
    result.project_dir,
    with_artifacts=True,
    with_automate_dv=False,
)
```

### `_expected_packages` & centralised constants

- `PKGS` – canonical package names keyed by short identifiers
- `PkgKey` – `Literal[...]` of allowed keys
- `PKG_VERSIONS` – versions keyed by `PkgKey`
- `PKG_ORDER` – stable rendering order
- `PackageSpec` – `TypedDict` describing one entry in `packages.yml`

`_expected_packages(...)` constructs the expected list by applying the flags:
```
def _expected_packages(
    *,
    with_utils: bool,
    with_artifacts: bool,
    with_expectations: bool,
    with_automate_dv: bool,
) -> Optional[list[PackageSpec]]
```

> [!TIP]
> To bump versions or change order, edit only the constants—tests update automatically.


### `_expected_vars`
Builds the expected `vars` block when Automate DV is enabled; returns `None` otherwise.
```
def _expected_vars(with_automate_dv: bool) -> Optional[VarsSpec]
```

### template_scenario
Parametrized fixture that feeds the test with scenarios:
```
@pytest.fixture(
    params=[
        ("defaults", {}, True,  True,  False, False),
        (
            "all_true",
            {"with_dbt_expectations": True, "with_automate_dv": True},
            True,
            True,
            True,
            True
        ),
        (
            "all_false",
            {"with_dbt_utils": False, "with_dbt_artifacts": False},
            False,
            False,
            False,
            False
        ),
    ]
)
def template_scenario(request):
    return request.param
```
Each tuple is:
```
(
    name,
    extra_answers,
    with_utils,
    with_artifacts,
    with_expectations,
    with_automate_dv
)
```

## Extending scenarios
Add another tuple to template_scenario:
```
(
    "expectations_only",
    {"with_dbt_expectations": True},
    True,   # utils default True
    True,   # artifacts default True
    True,   # expectations
    False,  # automate_dv
),
```
Then your single test automatically runs for the new scenario.

## Type checking
We use Python typing throughout:

- `TypedDict` for shape‑checked dicts (`PackageSpec`, `VarsSpec`, minimal YAML views)
- `Protocol` for the Copier Result object (duck‑typed)
- `Literal`/`Optional` for precise return types and flag‑driven behavior


## Maintenance checklist
When the template changes:

- **Package versions**: Update `PKG_VERSIONS` in `conftest.py`.
- **Package set or order**: Update `PKGS` / `PKG_ORDER`.
- **New feature toggle**:

  - Add param to `template_scenario` tuples
  - Update `_expected_packages(...)` and/or `_expected_vars(...)` if it affects outputs
  - Extend `assert_*` helpers if new files/sections should be asserted

- **dbt vars shape changed**: Update `VarsSpec` and `_expected_vars(...)`.
- **Add scenarios**: Append tuples to `template_scenario`.

> [!TIP]
> Keep all source‑of‑truth values (names, versions, order) centralised—tests will remain small and robust.
