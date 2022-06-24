{{ config(materialized = 'table') }}

WITH stg_bandcamp_data AS 
(
  SELECT
    *
  FROM 
    {{ ref('stg_bandcamp_data') }}
),

regional_code AS
(
  SELECT
      *
  FROM
      {{ ref('country_regional_code') }}
)

SELECT
  stg_data.id AS id,
  stg_data.buyer_country AS country,
  stg_data.buyer_country_code AS country_code,
  COALESCE(rg_code.region, 'NA') AS region,
  COALESCE(rg_code.sub_region, 'NA') AS sub_region
FROM
  stg_bandcamp_data AS stg_data
LEFT JOIN regional_code AS rg_code
  ON  stg_data.buyer_country_code = rg_code.alpha_2

{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}