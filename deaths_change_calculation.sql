CREATE TABLE deaths_change_sql AS
	SELECT
	country,
	date,
	total_deaths - lag(total_deaths) OVER (PARTITION BY country ORDER BY date ASC) as deaths_change
	FROM deaths_total;

UPDATE
    deaths_change_sql
SET
    deaths_change = 0
WHERE
    deaths_change IS NULL;
