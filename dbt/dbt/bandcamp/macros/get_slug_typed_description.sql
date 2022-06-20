{#
    This macro returns the description of the slug_type
#}

{% macro get_slug_type_description(slug_type) -%}

    case {{ slug_type }}
        when 'a' then 'All albums'
        when 'p' then 'Merch'
        when 't ' then 'Tracks'
    end

{%- endmacro %}