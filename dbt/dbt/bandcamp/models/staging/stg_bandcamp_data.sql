{{ config(materialized='view') }}

WITH bandcampdata AS 
(
  SELECT
    *
  FROM {{ source('staging', 'bandcamp_data') }}
)

SELECT
  -- identifier unique keys
  CAST(_id AS STRING) AS id,

  -- timestamp
  CAST(unix_timestamp AS timestamp) AS buy_datetime,

  -- country info
  CAST(country AS STRING) AS buyer_country,
  CAST(UPPER(country_code) AS STRING) AS buyer_country_code,

  -- art info
  CAST(artist_name AS STRING) AS artist_name,
  CAST(album_title AS STRING) AS album_title,
  CAST(item_type AS STRING) AS item_type,
  CAST(slug_type AS STRING) AS slug_type,

  -- sale info
  CAST(item_price AS NUMERIC) AS seller_price,
  CAST(amount_paid AS NUMERIC) AS amount_paid,
  CAST(currency AS STRING) AS currency,
  CAST(amount_paid_usd AS NUMERIC) AS amount_paid_usd
FROM
  bandcampdata
ORDER BY 
  buy_datetime


-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}