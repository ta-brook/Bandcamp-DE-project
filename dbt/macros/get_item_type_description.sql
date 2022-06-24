{#
    This macro returns the description of the item_type
#}

{% macro get_item_type_description(item_type) -%}

    case {{ item_type }}
        when 'a' then 'Digital albums'
        when 'p' then 'Physical items'
        when 't' then 'Digital tracks'
    end

{%- endmacro %}