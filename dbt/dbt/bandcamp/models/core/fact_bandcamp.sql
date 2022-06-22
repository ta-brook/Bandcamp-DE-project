{{ config(materialized='table')}}

WITH dim_key AS
(
  SELECT
    *
  FROM 
    {{ ref('dim_key') }}
),

dim_art AS 
(
  SELECT
    *
  FROM 
    {{ ref('dim_art') }}
),

dim_datetime AS 
(
  SELECT
    *
  FROM 
    {{ ref('dim_datetime') }}
),

dim_location AS
(
  SELECT
    *
  FROM 
    {{ ref('dim_location') }}
),

dim_sell AS
(
  SELECT
    *
  FROM 
    {{ ref('dim_sell') }}
)

SELECT
    dim_key.id AS id,
    dim_key.ts AS timestamp,

    dim_sell.seller_price AS seller_price,
    dim_sell.amount_paid AS amount_paid,
    dim_sell.currency AS currency,
    dim_sell.amount_paid_usd AS amount_paid_usd,

    dim_location.country AS country,
    dim_location.country_code AS country_code,
    dim_location.region AS region,
    dim_location.sub_region AS sub_region,

    dim_art.artist_name AS artist_name,
    dim_art.album_title AS album_title,
    dim_art.item_type AS item_type,
    dim_art.item_type_description AS item_type_description,
    dim_art.slug_type AS slug_type,
    dim_art.slug_type_description AS slug_type_description,

    dim_datetime.hourOfDay AS hourOfDay,
    dim_datetime.dayOfWeek AS dayOfWeek,
    dim_datetime.dayOfMonth AS dayOfMonth

FROM 
    dim_key

JOIN 
    dim_art ON dim_key.id = dim_art.id
JOIN
    dim_datetime ON dim_key.id = dim_datetime.id
JOIN 
    dim_location ON dim_key.id = dim_location.id
JOIN
    dim_sell ON dim_key.id = dim_sell.id
    
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
