# transform.py
import pandas as pd
import re

def load_csv(file_path):
    df = pd.read_csv(file_path)

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace("-", "_")
    )

    if "date" in df.columns:
      df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")


    if "country" in df.columns:
        df["country"] = df["country"].str.strip()

    missing_columns = [
        "aged_65_older",
        "aged_70_older",
        "cardiovasc_death_rate",
        "female_smokers",
        "male_smokers",
        "new_people_vaccinated_smoothed",
        "new_people_vaccinated_smoothed_per_hundred",
    ]

    for col in missing_columns:
        if col not in df.columns:
            df[col] = None

    return df


def prepare_countries(df):
    return df[
        [
            "country",
            "iso_code",
            "continent",
            "population",
            "median_age",
            "aged_65_older",
            "aged_70_older",
            "gdp_per_capita",
        ]
    ].drop_duplicates(subset=["country"]).reset_index(drop=True)


def prepare_health(df, country_map):
    health = df[
        [
            "country",
            "cardiovasc_death_rate",
            "diabetes_prevalence",
            "handwashing_facilities",
            "hospital_beds_per_thousand",
            "life_expectancy",
            "human_development_index",
        ]
    ].drop_duplicates(subset=["country"]).reset_index(drop=True)

    health["country_id"] = health["country"].map(country_map)
    health.drop(columns=["country"], inplace=True)
    return health


def prepare_economy(df, country_map):
    economy = df[
        [
            "country",
            "extreme_poverty",
            "female_smokers",
            "male_smokers",
            "excess_mortality",
        ]
    ].drop_duplicates(subset=["country"]).reset_index(drop=True)

    economy["country_id"] = economy["country"].map(country_map)
    economy.drop(columns=["country"], inplace=True)
    return economy


def prepare_daily(df, country_map):

    daily_cols = [
        "date",
        "new_cases",
        "total_cases",
        "new_cases_smoothed",
        "new_cases_per_million",
        "new_cases_smoothed_per_million",
        "total_cases_per_million",

        "new_deaths",
        "total_deaths",
        "new_deaths_smoothed",
        "new_deaths_per_million",
        "new_deaths_smoothed_per_million",
        "total_deaths_per_million",

        "icu_patients",
        "icu_patients_per_million",
        "hosp_patients",
        "hosp_patients_per_million",

        "weekly_icu_admissions",
        "weekly_icu_admissions_per_million",
        "weekly_hosp_admissions",
        "weekly_hosp_admissions_per_million",

        "stringency_index",
        "reproduction_rate",

        "total_tests",
        "new_tests",
        "total_tests_per_thousand",
        "new_tests_per_thousand",
        "new_tests_smoothed",
        "new_tests_smoothed_per_thousand",
        
        "positive_rate",
        "tests_per_case",


        "total_vaccinations",
        "people_vaccinated",
        "people_fully_vaccinated",
        "total_boosters",
        "new_vaccinations",
        "new_vaccinations_smoothed",

        "total_vaccinations_per_hundred",
        "people_vaccinated_per_hundred",
        "people_fully_vaccinated_per_hundred",
        "total_boosters_per_hundred",
        "new_vaccinations_smoothed_per_million",

        "new_people_vaccinated_smoothed",
        "new_people_vaccinated_smoothed_per_hundred",
    ]

    daily = df[["country"] + daily_cols].copy()
    
    # Remove unwanted suffixes
    daily.columns = [re.sub(r'_m\d+$', '', c) for c in daily.columns]

    daily["country_id"] = daily["country"].map(country_map)

    # Drop original country column
    daily.drop(columns=['country'], inplace=True)

    # Convert NaN → None
    daily = daily.where(pd.notnull(daily), None)


    return daily
