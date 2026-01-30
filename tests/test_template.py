# tests/test_template.py
from __future__ import annotations


def test_template_configurations(
    copie,
    template_scenario,
    assert_generation_ok,
    assert_answers,
    assert_packages_yaml,
    assert_dbt_project_yaml,
):
    (
        name,
        extra_answers,
        with_utils,
        with_artifacts,
        with_expectations,
        with_automate_dv,
    ) = template_scenario

    # IMPORTANT: pass {} (not None) to avoid Copier validation error on user_defaults
    result = copie.copy(extra_answers=extra_answers or {})

    assert_generation_ok(result)

    assert_answers(
        result,
        with_utils=with_utils,
        with_artifacts=with_artifacts,
        with_expectations=with_expectations,
        with_automate_dv=with_automate_dv,
    )

    assert_packages_yaml(
        result.project_dir,
        with_utils=with_utils,
        with_artifacts=with_artifacts,
        with_expectations=with_expectations,
        with_automate_dv=with_automate_dv,
    )

    assert_dbt_project_yaml(
        result.project_dir,
        with_artifacts=with_artifacts,
        with_automate_dv=with_automate_dv,
    )
