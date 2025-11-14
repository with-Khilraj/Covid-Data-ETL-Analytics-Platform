# reset_tables.py
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# DB credentials
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
db = os.getenv("DB_NAME")

# Create engine
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:3306/{db}")

# Tables to clear (in order to avoid FK issues)
tables = [
    "country_health_profile",
    "country_economy_profile",
    "covid_stats_daily",
    "countries"
]

try:
    with engine.connect() as conn:
        for table in tables:
            print(f"Clearing table: {table}...")
            conn.execute(text(f"DELETE FROM {table};"))
        print("\nAll specified tables cleared successfully!")

except Exception as e:
    print("Error clearing tables:")
    print(e)
