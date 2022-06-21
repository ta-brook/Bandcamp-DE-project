{#
    This macro returns the updated version of the buyer_country
#}

{% macro update_country_name(buyer_country) -%}

     REPLACE(REPLACE(REPLACE({{ buyer_country }}, 'Republic of Korea','Korea'),'Palestinian Territory', 'Palestine'),'Libyan Arab Jamahiriya', 'Libya')


{%- endmacro %}