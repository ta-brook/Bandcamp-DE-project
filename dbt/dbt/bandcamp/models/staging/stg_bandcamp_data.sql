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
  CAST({{ update_country_name('country')}} AS STRING) AS buyer_country,
  CAST(UPPER(country_code) AS STRING) AS buyer_country_code,

  -- artist info
  CAST(artist_name AS STRING) AS artist_name,
  CAST(album_title AS STRING) AS album_title,
  CAST(item_type AS STRING) AS item_type,
  {{ get_item_type_description('item_type') }} AS item_type_description,
  CAST(slug_type AS STRING) AS slug_type,
  {{ get_slug_type_description('slug_type') }} AS slug_type_description,

  -- sale info
  CAST(item_price AS NUMERIC) AS seller_price,
  CAST(amount_paid AS NUMERIC) AS amount_paid,
  CAST(currency AS STRING) AS currency,
  CAST(amount_paid_usd AS NUMERIC) AS amount_paid_usd
FROM
  bandcampdata
WHERE 
  currency IN (
    SELECT 
      AlphabeticCode
    FROM
      {{ ref('currency') }}
    WHERE 
      AlphabeticCode IS NOT NULL
  )
  AND
  country  IN (
    SELECT 
      name
    FROM 
      {{ ref('country_regional_code') }}
  )
ORDER BY 
  buy_datetime

