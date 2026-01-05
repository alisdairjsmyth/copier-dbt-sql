# copier-dbt-sql
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

This is an experimental [copier](https://github.com/copier-org/copier) template for [dbt](https://getdbt.com) projects deployed to [Databricks](https://www.databricks.com/) within a [Databricks Asset Bundle](https://docs.databricks.com/en/dev-tools/bundles/index.html). It's useful for scaffolding out a basic project structure and configuration with modern tooling quickly.

It is based on the Databricks Asset Bundle [dbt-sql](https://github.com/databricks/cli/tree/main/libs/template/templates/dbt-sql). It leverages dbt-core for local development and relies on Databricks Asset Bundles for deployment (either manually or with CI/CD). In production, dbt is executed using Lakeflow Jobs.

* Learn more about the dbt and its standard project structure here: https://docs.getdbt.com/docs/build/projects.
* Learn more about Databricks Asset Bundles here: https://docs.databricks.com/en/dev-tools/bundles/index.html

## Prerequisites
To use this template, you will need:
* [Python 3.11](https://www.python.org/downloads/windows/)
* [uv](https://docs.astral.sh/uv/) - `py -m pip install uv`
* git
* [Databricks CLI](https://github.com/databricks/cli)

The template includes [Visual Studio Code](https://code.visualstudio.com/) configuration and [GitHub Actions](https://github.com/features/actions) workflows.

## Features
- Structured in line with dbt-sql Databricks Asset Bundle [template](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/templates#default-bundle-templates)
- dbt project organised per dbt Lab's *How we structure dbt project* [guidance](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)
- Formatting of SQL with `sqlfmt`
- Linting of SQL with `SQLFluff`
- Python packaging using `pyproject.toml`
- Modern Python tooling from astral.sh: `ruff` and `uv` for formatting, linting, and dependency management
- Pre-commit hooks for automated linting, formatting, and fixes on commit
- VS Code configuration supporting toolchain
- Selection of recommended dbt packages:
  - `dbt-utils`
  - `dbt-artifacts`
- [Conventional Commits](https://www.conventionalcommits.org/) to automate [Sematic Versioning](https://semver.org/) and [Keep A Changelog](https://keepachangelog.com/) with [Commitizen](https://github.com/commitizen-tools/commitizen)
- CI/CD configuration using GitHub Actions
- Dependabot configuration

## Using
> [!TIP]
> You should first [install uv](https://docs.astral.sh/uv/getting-started/installation/) to be able to run the commands below.

### Create a new dbt project
To create a new project with this template, run:
```sh
uvx copier copy gh:alisdairjsmyth/copier-dbt-sql .
```

### Update the dbt project
To update the project to the latest template version, run:
```sh
uvx copier update
```

## Credit
This project has been developed with reference to the following projects:
- Databricks Asset Bundle [dbt-sql](https://github.com/databricks/cli/tree/main/libs/template/templates/dbt-sql) published by Databricks
- The Copier template [superlinear-ai/substrate](https://github.com/superlinear-ai/substrate)
- The Copier template [gwenwindflower/copier-dbt](https://github.com/gwenwindflower/copier-dbt)
