-- Find the years where the chemistry price where won by two
-- and the summer olympics where held in europe.
-- Summery of lecture 1.

WITH
  chemistry_laureates(year, name) AS (
    SELECT   year, name
    FROM     nobel
    WHERE    category = 'chemistry'
  ),
  years_with_two_chemistry_laureates(year) AS (
    SELECT   year
    FROM     chemistry_laureates
    GROUP BY year
    HAVING   count() = 2
  ),
  years_with_summer_olympics_in_europe(year) AS (
    SELECT   year
    FROM     olympics
    WHERE    continent = "Europe" AND season = "summer"
  )
SELECT   year, name
FROM     chemistry_laureates
WHERE    year IN (
  SELECT   year
  FROM     years_with_two_chemistry_laureates
) AND year IN (
    SELECT   year
    FROM     years_with_summer_olympics_in_europe
)
