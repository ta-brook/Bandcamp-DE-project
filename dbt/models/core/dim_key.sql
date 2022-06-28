{{ config(materialized = 'table') }}

WITH stg_bandcamp_data AS 
(
  SELECT
    *
  FROM 
    {{ ref('stg_bandcamp_data') }}
)

SELECT
    id,
    buy_datetime AS ts
FROM
    stg_bandcamp_data

{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}