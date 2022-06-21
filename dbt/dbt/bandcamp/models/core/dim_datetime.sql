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
  buy_datetime,
  EXTRACT( DAYOFWEEK FROM buy_datetime) AS dayOfWeek,
  EXTRACT( DAY FROM buy_datetime) AS dayOfMonth,
  EXTRACT( WEEK FROM buy_datetime) AS weekOfYear,
  EXTRACT( MONTH FROM buy_datetime) AS month,
  EXTRACT( YEAR FROM buy_datetime) AS year
FROM
  stg_bandcamp_data
  
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}