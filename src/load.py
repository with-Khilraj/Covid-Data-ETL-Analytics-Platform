import pandas as pd
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

def load_to_sql(df, table_name, engine, chunksize=1000):

    # 1. Clean DataFrame
    df.columns = df.columns.str.lower().str.strip()
    df = df.where(pd.notnull(df), None)  # convert NaN → None

    # 2. Match dataframe columns to SQL table
    insp = inspect(engine)

    if table_name not in insp.get_table_names():
        raise ValueError(f"Table '{table_name}' does not exist in database!")

    sql_cols = [col["name"] for col in insp.get_columns(table_name)]

    # Keep only matching columns
    df = df[[c for c in df.columns if c in sql_cols]]

    # 3. Insert with error handling
    try:
        df.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=chunksize
        )
        print(f"✓ {table_name} loaded successfully ({len(df)} rows)")

    except SQLAlchemyError as e:
        print(f"✗ ERROR loading table '{table_name}'")
        print("Reason:", e.__cause__ or e)
        raise
