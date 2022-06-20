{{ config(materialized = 'table') }}

WITH bandcampdsell AS 
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
  amount_paid_usd,
  (IF amount_paid_usd < 1 THEN 'TRUE' ELSE 'FALSE') AS lower_than_1_usd,
  (IF amount_paid_usd > 5 THEN 'TRUE' ELSE 'FALSE') AS higher_than_5_usd,
  (IF amount_paid_usd > 10 THEN 'TRUE' ELSE 'FALSE') AS higher_than_10_usd,
  (IF amount_paid_usd > 100 THEN 'TRUE' ELSE 'FALSE') AS higher_than_100_usd,
  (IF amount_paid_usd > 1000 THEN 'TRUE' ELSE 'FALSE') AS higher_than_1000_usd
FROM
  bandcampsell
  
-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}