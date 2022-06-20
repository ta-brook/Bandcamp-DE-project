{{ config(materialized = 'table') }}

WITH bandcampdatetime AS 
(
  SELECT
    *
  FROM 
    {{ ref('stg_bandcamp_data') }}
)

SELECT
  buy_datetime,
  EXTRACT( DAYOFWEEK FROM buy_datetime) AS dayOfWeek,
  EXTRACT( DAY FROM buy_datetime) AS dayOfMonth,
  EXTRACT( WEEK FROM buy_datetime) AS weekOfYear,
  EXTRACT( MONTH FROM buy_datetime) AS month,
  EXTRACT( YEAR FROM buy_datetime) AS year
FROM
  bandcampdatetime
  
-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}