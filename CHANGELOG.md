## 0.4.0 (2026-01-06)

### Feat

- use environment variables
- add environment isolation in development

### Fix

- include changelog in github release

## [0.15.1](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.15.0...v0.15.1) (2026-01-15)


### 🐛 Bug Fixes

* avoid testing for dbt_artifacts if custom_schema_name is none ([b1e18df](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/b1e18dfbc0dad9e73fc61fa20869efdf33eb3217))

## [0.15.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.14.1...v0.15.0) (2026-01-15)


### 🚀 New Features

* use dbt-databricks 1.11 ([11c021c](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/11c021cbabf726b23c5524f7003237c22275437b)), closes [#38](https://github.com/alisdairjsmyth/copier-dbt-sql/issues/38)


### 🐛 Bug Fixes

* introduce profile_template.yml for dbt init ([19cbbe6](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/19cbbe66738fe72116c15061c6354e0327851d49)), closes [#35](https://github.com/alisdairjsmyth/copier-dbt-sql/issues/35)
* modify release-please release type to maintain dbt_project.yml formatting ([e8fb197](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/e8fb1971ce3fe394710869bbf001da8a16154c45)), closes [#29](https://github.com/alisdairjsmyth/copier-dbt-sql/issues/29)
* use data product specific profile ([d59dc08](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/d59dc08448d46749cb8e4d3a10cefe635769270f))

## [0.14.1](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.14.0...v0.14.1) (2026-01-14)


### 🐛 Bug Fixes

* change config-type to config-file ([89eb4a1](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/89eb4a1ccc52e9bbbcf480dc11ab434b7dd470f6))

## [0.14.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.13.1...v0.14.0) (2026-01-14)


### 🚀 New Features

* maintain semver within dbt_project.yml ([c2d13ef](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/c2d13efbca942453f2db10801c5d48313034bd71))


### 🐛 Bug Fixes

* add config-file to release-please action within template ([85c4abc](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/85c4abc059a8ed43dd6747527e6411dd65663aa3))
* add conventional-commit badge to template ([a707d41](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/a707d41fb3e27c5898bead4e5f238b0fb6c53363))
* lint dbt_project.yml within template ([8608b52](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/8608b5288125cddb5f7a8a6ffa835f1ef63264f2))

## [0.13.1](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.13.0...v0.13.1) (2026-01-13)


### Bug Fixes

* resolve task key in line with databricks naming constraint ([b0cdb5c](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/b0cdb5c20354d3ffdfdbe1d114ce82a68df12d71))

## [0.13.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.12.5...v0.13.0) (2026-01-13)


### Features

* add support for serverless budget policies ([585dac3](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/585dac3e14387f47518bb11f1ecfb3d4615c7102)), closes [#25](https://github.com/alisdairjsmyth/copier-dbt-sql/issues/25) [#25](https://github.com/alisdairjsmyth/copier-dbt-sql/issues/25)
* extend deployment to use environment variables for budget_policy_id ([7bc6613](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/7bc6613063bd48627440a247328e65297b89af28))


### Bug Fixes

* add group and access configuration to dbt project ([7864571](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/78645716d3ef2b92a5f5ff3b25b3619c8b95bf65))
* exclude dbt_arifacts from build execution ([2384e98](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/2384e982110b216da12857abf7f1f153bb6bceee))
* include automate dv hashing configuration ([55c7b17](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/55c7b1727a207b4f422116d1312e61a7f10164e4))
* perist docs for relations and columns ([bda4944](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/bda4944dd9c4fd6140a13b169130f554e1ef5dd5))

## [0.12.5](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.12.4...v0.12.5) (2026-01-12)


### Bug Fixes

* update copier envops to use square brackets ([db81f60](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/db81f60e334b04aa561b3210776984ed4b0eda77))

## [0.12.4](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.12.3...v0.12.4) (2026-01-12)


### Bug Fixes

* bump python version ([d3353ba](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/d3353ba68e9607a02b53731abdc608eb933fe5b6))
* update copier envops to use square brackets ([e99cc29](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/e99cc29f8e202150ab60ddb75e025ce4c5a9fb86))
* use rebase ([e29994d](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/e29994de75ba5a340bd3ca481d7b21728ab526a9))

## [0.12.3](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.12.2...v0.12.3) (2026-01-12)


### Bug Fixes

* change template dependencies to align with serverless definition ([bc06322](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/bc0632272a1e761e29c61d74026aab96f1b1e7fc))

## [0.12.2](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.12.1...v0.12.2) (2026-01-12)


### Bug Fixes

* resolve conflict between copier variable start string and bash notation used within template ([db1e2a5](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/db1e2a534a0abb9f20cd9c271b9794006cd541db))

## [0.12.1](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.12.0...v0.12.1) (2026-01-11)


### Bug Fixes

* fix pre-commit names ([b31bc5a](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/b31bc5a36a2ef621b71b32f39746a270f933c5e4))

## [0.12.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.11.0...v0.12.0) (2026-01-11)


### Features

* add pull request template ([07139c3](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/07139c39211df5b07953aab0bbfd230bc26ebe94))
* style pre-commit hook names ([eab051a](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/eab051aa289f8dc63afa392f47448c851f95a615))


### Bug Fixes

* add vs code file association for sql files ([f4efd80](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/f4efd808a752965a5c393d9da7b672f91073fe14))

## [0.11.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.10.0...v0.11.0) (2026-01-11)


### Features

* add generate_schema_name override ([c3361d9](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/c3361d9692603823fd6e69148fb619c143a3097c))
* adjust generate_schema_name strategy ([a1582da](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/a1582da066ada6655e15e0117f2f3d063bc58e5d))

## [0.10.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.9.0...v0.10.0) (2026-01-11)


### Features

* add just recipes to template ([5f8c162](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/5f8c1622458c91d0f41ce6b9e5bebdaba36a3d37))


### Bug Fixes

* specify schema for dbt_artifacts ([c2c5f8f](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/c2c5f8fe07bf8359c4ed038561b1f72fdb7d70ff))

## [0.9.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.8.0...v0.9.0) (2026-01-10)


### Features

* add copier update workflow ([f41d7aa](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/f41d7aa871f4c12d8893b7f66355df140700a945))

## [0.8.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.7.2...v0.8.0) (2026-01-10)


### Features

* force new version ([3d7d396](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/3d7d39623917024dbfbd4552e301cf158b5dc9c8))

## [0.7.2](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.7.1...v0.7.2) (2026-01-10)


### Bug Fixes

* deploy based on release tag ([3e35b56](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/3e35b565b643644e336ecb44fd2cf138fca86831))
* remove bundle uuid from template ([8561ab3](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/8561ab35c793ab357c00a1023947c5ad29c4b393))

## [0.7.1](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.7.0...v0.7.1) (2026-01-10)


### Bug Fixes

* add deploy job to release-please workflow ([6d1b0f9](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/6d1b0f9f01e8db90c4de267b9390344c65b0ca1e))
* add readme to template ([4811f2b](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/4811f2bb469efc85a082253fc46e655b0a7140a8))
* use native substitutions in databricks.yml ([3b83b1b](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/3b83b1b63efa582dbcfb4c0c40a9b3286f1f4edb))

## [0.7.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.6.7...v0.7.0) (2026-01-09)


### Features

* include uv.lock in release ([9000e35](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/9000e35c906e827a6d8ebf92443a814b20a68801))


### Bug Fixes

* include uv.lock in release ([3a7c956](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/3a7c9566c920798f03f10003f8f7e5e92b9b8e1f))

## [0.6.7](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.6.6...v0.6.7) (2026-01-09)


### Bug Fixes

* include uv.lock in release ([866f7d3](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/866f7d39efea3b899cacc98d2bf76e0f8951b06c))

## [0.6.6](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.6.5...v0.6.6) (2026-01-09)


### Bug Fixes

* add warehouse_name variable ([8ce1aed](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/8ce1aed1513b080767c04c354167ed80af64a9d4))

## [0.6.5](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.6.4...v0.6.5) (2026-01-09)


### Bug Fixes

* correct variable list ([345cfd0](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/345cfd05685710e31d29118ac577fbe2506c03b5))

## [0.6.4](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.6.3...v0.6.4) (2026-01-09)


### Bug Fixes

* correct dev workspace definition ([a7c4761](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/a7c4761af704a93f4b6f7eb1924640bc8a50a25c))

## [0.6.3](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.6.2...v0.6.3) (2026-01-08)


### Bug Fixes

* serverless environment version is string ([426a2bf](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/426a2bfe66177a4bf93399cff76b51760e44ac66))

## [0.6.2](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.6.1...v0.6.2) (2026-01-08)


### Bug Fixes

* add databricks-connect dependency ([38fb45c](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/38fb45c502eb11bee4e57fef890d17e88f886ab6))
* remove __builtins__.pyi from template ([50b06c6](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/50b06c68975f9ed51fbfed16e7206a5f33c303b3))
* update dbt_databricks_dependency ([bfe5af8](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/bfe5af80b4af88c819d0bd91125042d3c0051d84))

## [0.6.1](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.6.0...v0.6.1) (2026-01-08)


### Bug Fixes

* add release-please config to template ([7878552](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/787855205016f284395592a6ac05fcc00f96d07e))

## [0.6.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/v0.5.0...v0.6.0) (2026-01-08)


### Features

* add release-please workflow to template ([5076ea4](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/5076ea49ce6990b77002a60761c8610965af25f7))

## [0.5.0](https://github.com/alisdairjsmyth/copier-dbt-sql/compare/0.4.0...v0.5.0) (2026-01-07)


### Features

* default require_explicit_package_overrides_for_builtin_materializations ([ffeff2c](https://github.com/alisdairjsmyth/copier-dbt-sql/commit/ffeff2c47db4495f913f5e2b8241d7a7bb9f637d))

## 0.3.10 (2026-01-06)

### Fix

- include code block
- update copy command

## 0.3.9 (2026-01-06)

### Fix

- restructure template
- update subdirectory

## 0.3.8 (2026-01-06)

### Fix

- update subdirectory

## 0.3.7 (2026-01-06)

### Fix

- change tag_format

## v0.3.6 (2026-01-06)

### Fix

- add commitizen configuration to template

## v0.3.5 (2026-01-06)

### Fix

- pin package dependencies to minor versions

## v0.3.4 (2026-01-05)

### Fix

- remove python-certifi-win32 dependency from template

## v0.3.3 (2026-01-05)

### Fix

- correct envops

## v0.3.2 (2026-01-05)

### Fix

- avoid jinja conflict
- add on-run-end for dbt_artifacts package
- correct defaultInterpreterPath

## v0.3.1 (2026-01-05)

### Fix

- add commitizen dependency to template

## v0.3.0 (2026-01-05)

### Feat

- add github workflows

### Fix

- correct default interpreter path

## v0.2.0 (2026-01-05)

### Feat

- add github actions extension

### Fix

- correct message after copy

## v0.1.2 (2026-01-05)

### Fix

- add credits

## v0.1.1 (2026-01-05)

### Fix

- add copier badge

## v0.1.0 (2026-01-05)

### Feat

- initial commit
