-- =====================================================
-- COVID-19 Database Schema (Optimized)
create database if not exists covid;
use covid;

-- 1. Countries Table (static metadata)
CREATE TABLE countries (
    country_id INT AUTO_INCREMENT PRIMARY KEY, 
    country VARCHAR(200) NOT NULL, 
    iso_code VARCHAR(20), 
    continent VARCHAR(100), 
    population BIGINT, 
    median_age FLOAT, 
    aged_65_older FLOAT, 
    aged_70_older FLOAT, 
    gdp_per_capita FLOAT
);

-- 2. CountryHealthProfile Table (rarely-changing health indicators)
CREATE TABLE country_health_profile (
    health_id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    
   cardiovasc_death_rate FLOAT, 
   diabetes_prevalence FLOAT, 
   handwashing_facilities FLOAT, 
   hospital_beds_per_thousand FLOAT, 
   life_expectancy FLOAT, 
   human_development_index FLOAT,

    FOREIGN KEY (country_id) REFERENCES countries(country_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- 3. CountryEconomyProfile Table (economy/general indicators)
CREATE TABLE country_economy_profile (
    economy_id INT AUTO_INCREMENT PRIMARY KEY, 
    country_id INT NOT NULL, 
    
    extreme_poverty FLOAT, 
    female_smokers FLOAT, 
    male_smokers FLOAT, 
    excess_mortality FLOAT,

    FOREIGN KEY (country_id) REFERENCES countries(country_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- 4. CovidStatsDaily Table (daily time-series data)
CREATE TABLE covid_stats_daily (
    stats_id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    date DATE NOT NULL,

    -- cases
    new_cases DOUBLE, 
    total_cases DOUBLE, 
    new_cases_smoothed DOUBLE, 
    new_cases_per_million DOUBLE, 
    new_cases_smoothed_per_million 
    DOUBLE, total_cases_per_million DOUBLE,

    -- deaths
    new_deaths INT, 
    total_deaths INT, 
    new_deaths_smoothed DOUBLE, 
    new_deaths_per_million DOUBLE, 
    new_deaths_smoothed_per_million DOUBLE, 
    total_deaths_per_million DOUBLE,

    -- hospital usage
    icu_patients DOUBLE, 
    icu_patients_per_million DOUBLE, 
    hosp_patients DOUBLE, 
    hosp_patients_per_million DOUBLE, 
    weekly_icu_admissions DOUBLE, 
    weekly_icu_admissions_per_million DOUBLE, 
    weekly_hosp_admissions DOUBLE, 
    weekly_hosp_admissions_per_million DOUBLE,

    stringency_index DOUBLE, 
    reproduction_rate DOUBLE, 
    
    total_tests DOUBLE, 
    new_tests DOUBLE, 
    total_tests_per_thousand DOUBLE, 
    new_tests_per_thousand DOUBLE, 
    new_tests_smoothed DOUBLE, 
    new_tests_smoothed_per_thousand DOUBLE, 
    
    positive_rate DOUBLE, 
    tests_per_case DOUBLE,

    -- vaccinations
    total_vaccinations DOUBLE, 
    people_vaccinated DOUBLE, 
    people_fully_vaccinated DOUBLE, 
    total_boosters DOUBLE, 
    new_vaccinations DOUBLE, 
    new_vaccinations_smoothed DOUBLE, 
    total_vaccinations_per_hundred DOUBLE, 
    people_vaccinated_per_hundred DOUBLE,
    people_fully_vaccinated_per_hundred DOUBLE, 
    total_boosters_per_hundred DOUBLE, 
    new_vaccinations_smoothed_per_million DOUBLE,

    -- constraints and indexes
    UNIQUE KEY (country_id, Date),
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX (country_id, date),
    INDEX (date)
);
