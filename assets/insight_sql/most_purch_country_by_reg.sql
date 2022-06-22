SELECT
  region,
  country,
  COUNT(1) AS purchases
FROM
  fact_bandcamp
GROUP BY
  country, region
HAVING
  COUNT(1) = 
  (
    SELECT
      MAX(c)
    FROM 
    (
      SELECT
        COUNT(1) AS c
      FROM
        fact_bandcamp
      WHERE 
        region = 'Americas'
      GROUP BY country
    )
  )
  OR
  COUNT(1) = 
  (
    SELECT
      MAX(c)
    FROM 
    (
      SELECT
        COUNT(1) AS c
      FROM
        fact_bandcamp
      WHERE 
        region = 'Europe'
      GROUP BY country
    )
  )
  OR
  COUNT(1) = 
  (
    SELECT
      MAX(c)
    FROM 
    (
      SELECT
        COUNT(1) AS c
      FROM
        fact_bandcamp
      WHERE 
        region = 'Oceania'
      GROUP BY country
    )
  )
  OR
  COUNT(1) = 
  (
    SELECT
      MAX(c)
    FROM 
    (
      SELECT
        COUNT(1) AS c
      FROM
        fact_bandcamp
      WHERE 
        region = 'Asia'
      GROUP BY country
    )
  )
  OR
  COUNT(1) = 
  (
    SELECT
      MAX(c)
    FROM 
    (
      SELECT
        COUNT(1) AS c
      FROM
        fact_bandcamp
      WHERE 
        region = 'Africa'
      GROUP BY country
    )
  )