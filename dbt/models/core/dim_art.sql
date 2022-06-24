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
  artist_name,
  COALESCE(album_title, 'NA') AS album_title,
  item_type,
  item_type_description,
  slug_type,
  slug_type_description
FROM
  stg_bandcamp_data

{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}