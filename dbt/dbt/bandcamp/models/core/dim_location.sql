{{ config(materialized = 'table') }}

WITH bandcamplocation AS 
(
  SELECT
    *
  FROM 
    {{ ref('stg_bandcamp_data') }}
)

WITH regionalcode AS
(
    SELECT
        *
    FROM
        {{ ref('country_regional_code') }}
)

SELECT
    bl.id AS id
    bl.buyer_country AS country,
    bl.buyer_country_code AS country_code,
    COALESCE(`rl.region`, 'NA') AS region,
    COALESCE(`rl.sub-region`, 'NA') AS sub_region,

FROM
  bandcamplocation AS bl

JOIN regionalcode AS rl
    ON  `bl.buyer_country_code` = `rl.alpha-2`

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}