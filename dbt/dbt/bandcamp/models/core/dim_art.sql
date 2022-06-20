{{ config(materialized = 'table') }}

WITH bandcampart AS 
(
  SELECT
    *
  FROM 
    {{ ref('stg_bandcamp_data') }}
)

SELECT
  id,
  artist_name,
  album_title,
  COALESCE(album_title, 'NA') AS album_title,
  item_type,
  item_type_description,
  slug_type,
  slug_type_description
FROM
  bandcampart
  
-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}