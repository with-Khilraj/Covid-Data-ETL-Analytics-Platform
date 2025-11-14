# check_etl.py
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get DB credentials
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
db = os.getenv("DB_NAME")

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:3306/{db}")

# Tables to check
tables = [
    "countries",
    "country_health_profile",
    "country_economy_profile",
    "covid_stats_daily"
]

try:
    with engine.connect() as conn:
        # Print connected database
        result = conn.execute(text("SELECT DATABASE();"))
        db_name = result.fetchone()[0]
        print(f"Connected to database: {db_name}\n")

        # Print row counts for each table
        for table in tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.fetchone()[0]
            print(f"Table '{table}' row count: {count}")

except Exception as e:
    print("Error connecting to the database:")
    print(e)
