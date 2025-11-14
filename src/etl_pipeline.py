import pandas as pd
from src.db import get_engine
from src.transform import (
    load_csv,
    prepare_countries,
    prepare_health,
    prepare_economy,
    prepare_daily
)
from src.load import load_to_sql

# 1. Load raw CSV
df = load_csv("data/raw/compact.csv")

# 2. Connect to MySQL
engine = get_engine()

# 3. Load Countries Table
countries = prepare_countries(df)
load_to_sql(countries, "countries", engine)

# 4. Create CountryID mapping
country_map_df = pd.read_sql("SELECT country_id, country FROM countries", engine)

# IMPORTANT: Match correct column names
country_map_dict = dict(zip(country_map_df["country"], country_map_df["country_id"]))

# 5. HEALTH TABLE
health = prepare_health(df, country_map_dict)
load_to_sql(health, "country_health_profile", engine)

# 6. ECONOMY TABLE
economy = prepare_economy(df, country_map_dict)
load_to_sql(economy, "country_economy_profile", engine)

# 7. DAILY FACT TABLE
daily = prepare_daily(df, country_map_dict)
load_to_sql(daily, "covid_stats_daily", engine)

print("ETL process completed successfully!")
