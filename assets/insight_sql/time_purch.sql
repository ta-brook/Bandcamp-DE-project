SELECT
  hourOfDay,
  COUNT(1) AS purchases
FROM
  fact_bandcamp
GROUP BY 1
ORDER BY 2 DESC
LIMIT 24