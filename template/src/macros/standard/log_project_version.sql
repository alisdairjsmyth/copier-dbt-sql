{% macro log_project_version() -%}

    {%- set project_version = var("project_version") -%}

    {{
        log(
            "========================================================================",
            info=true,
        )
    }}
    {{ log(project_name ~ " version: " ~ project_version, info=true) }}
    {{
        log(
            "========================================================================",
            info=true,
        )
    }}

{%- endmacro %}
