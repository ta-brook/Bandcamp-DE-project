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
  seller_price,
  amount_paid,
  currency,
  amount_paid_usd
FROM
  stg_bandcamp_data

{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
