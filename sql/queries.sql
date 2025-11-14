use covid;

# Shows top 20 countries by total cases along with vaccination status.
SELECT 
    c.country,
    MAX(d.total_cases) AS total_cases,
    MAX(d.total_deaths) AS total_deaths,
    MAX(d.people_fully_vaccinated) AS fully_vaccinated,
    MAX(d.total_boosters) AS total_boosters
FROM covid_stats_daily d
JOIN countries c ON d.country_id = c.country_id
GROUP BY c.country
ORDER BY total_cases DESC
LIMIT 20;

# Visualize new cases over time:
SELECT 
    d.date,
    d.new_cases,
    d.new_deaths,
    d.new_cases_smoothed,
    d.new_deaths_smoothed
FROM covid_stats_daily d
JOIN countries c ON d.country_id = c.country_id
WHERE c.country = 'Nepal'
ORDER BY d.date;

# Shows trends by ISO week
SELECT 
    YEARWEEK(d.date, 1) AS year_week,
    SUM(d.new_cases) AS weekly_cases,
    SUM(d.new_deaths) AS weekly_deaths
FROM covid_stats_daily d
JOIN countries c ON d.country_id = c.country_id
WHERE c.country = 'India'
GROUP BY year_week
ORDER BY year_week;


# Compare which countries had higher fatality relative to cases.
SELECT 
    c.country,
    MAX(d.total_deaths)/MAX(d.total_cases)*100 AS case_fatality_rate
FROM covid_stats_daily d
JOIN countries c ON d.country_id = c.country_id
GROUP BY c.country
ORDER BY case_fatality_rate DESC
LIMIT 20;

#Percentage of population fully vaccinated:
SELECT 
    c.country,
    MAX(d.people_fully_vaccinated)/c.population*100 AS pct_fully_vaccinated
FROM covid_stats_daily d
JOIN countries c ON d.country_id = c.country_id
GROUP BY c.country
ORDER BY pct_fully_vaccinated DESC
LIMIT 20;


#see correlations between health/economic indicators and COVID impact.
SELECT 
    c.country,
    chp.life_expectancy,
    chp.human_development_index,
    cep.extreme_poverty,
    MAX(d.total_cases_per_million) AS cases_per_million,
    MAX(d.total_deaths_per_million) AS deaths_per_million
FROM covid_stats_daily d
JOIN countries c ON d.country_id = c.country_id
JOIN country_health_profile chp ON c.country_id = chp.country_id
JOIN country_economy_profile cep ON c.country_id = cep.country_id
GROUP BY c.country
ORDER BY cases_per_million DESC
LIMIT 20;

