import os

import pandas as pd
import psycopg2
from utils import BASE_DIR

DB_CONFIG = {
    "host": "localhost",
    "database": "vn_stock_dw",
    "user": "postgres",
    "password": "12",
    "port": 5432,
}


def check_database_exists(dbname, user, password, host="localhost", port="5432"):
    try:
        # Connect to the default "postgres" database
        conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Allow running DB-level queries
        cur = conn.cursor()

        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
        exists = cur.fetchone() is not None

        # Close connection
        cur.close()
        conn.close()

        return exists

    except psycopg2.Error as e:
        print(f"Error: {e}")
        return False


def branching_postgres():
    if check_database_exists("vn_stock_dw", "postgres", "12"):
        return "skip_create_db"
    return "initiate_postgres"


def insert_industries():
    csv_path = "/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2/data/raw/industries.csv"
    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        # Read CSV file
        df = pd.read_csv(csv_path, sep="|", index_col=False)

        # Convert dataframe to list of tuples
        data_tuples = [tuple(x) for x in df.to_numpy()]

        # Create INSERT query dynamically
        columns = ', '.join(df.columns)
        values_placeholder = ', '.join(['%s'] * len(df.columns))
        insert_query = f"""
        INSERT INTO dim_enterprises_industries ({columns}) 
        VALUES ({values_placeholder})
        ON CONFLICT (industry_code) 
        DO UPDATE SET 
            {', '.join([f"{col} = EXCLUDED.{col}" for col in df.columns if col != "stock_code"])}
        """

        # Execute batch insert
        cur.executemany(insert_query, data_tuples)
        conn.commit()

        print(f"Successfully inserted {len(data_tuples)} rows into dim_enterprises_industries")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def insert_dates_transformed(dates):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        # Convert dataframe to list of tuples
        df = pd.DataFrame({"date_key": dates})
        try:
            df['date_key'] = pd.to_datetime(df['date_key'], format="%Y-%m-%d %H:%M:%S")
        except Exception as e:
            df['date_key'] = pd.to_datetime(df['date_key'], format="%Y-%m-%d")

        # Calculate date attributes
        df["year"] = df["date_key"].dt.year
        df["quarter"] = df["date_key"].dt.quarter
        df["month"] = df["date_key"].dt.month
        df["week"] = df["date_key"].dt.isocalendar().week
        df["day_of_week"] = df["date_key"].dt.dayofweek + 1  # 1=Monday, 7=Sunday

        data_tuples = [tuple(x) for x in df.to_numpy()]

        # Create INSERT query dynamically
        columns = ', '.join(df.columns)
        values_placeholder = ', '.join(['%s'] * len(df.columns))
        insert_query = f"""
            INSERT INTO dim_date ({columns}) 
            VALUES ({values_placeholder})
            ON CONFLICT (date_key) 
            DO UPDATE SET 
                {', '.join([f"{col} = EXCLUDED.{col}" for col in df.columns if col != "date_key"])}
            """

        # Execute batch insert
        cur.executemany(insert_query, data_tuples)
        conn.commit()

        print(f"Successfully inserted {len(data_tuples)} rows into dim_date")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def insert_dates(dates):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        # Convert dataframe to list of tuples
        df = pd.DataFrame({"date_key": dates})
        df["date_key"] = pd.to_datetime(df["date_key"], format="%d/%m/%Y")

        # Calculate date attributes
        df["year"] = df["date_key"].dt.year
        df["quarter"] = df["date_key"].dt.quarter
        df["month"] = df["date_key"].dt.month
        df["week"] = df["date_key"].dt.isocalendar().week
        df["day_of_week"] = df["date_key"].dt.dayofweek + 1  # 1=Monday, 7=Sunday

        data_tuples = [tuple(x) for x in df.to_numpy()]

        # Create INSERT query dynamically
        columns = ', '.join(df.columns)
        values_placeholder = ', '.join(['%s'] * len(df.columns))
        insert_query = f"""
            INSERT INTO dim_date ({columns}) 
            VALUES ({values_placeholder})
            ON CONFLICT (date_key) 
            DO UPDATE SET 
                {', '.join([f"{col} = EXCLUDED.{col}" for col in df.columns if col != "date_key"])}
            """

        # Execute batch insert
        cur.executemany(insert_query, data_tuples)
        conn.commit()

        print(f"Successfully inserted {len(data_tuples)} rows into dim_date")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def insert_enterprise():
    csv_path = "/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2/data/raw/enterprises.csv"
    # Read CSV file
    df = pd.read_csv(csv_path, sep="|", index_col=False)
    df = df.drop("cafef_url", axis="columns")
    df = df.rename({"code": "stock_code", "name": "enterprise_name"}, axis="columns")
    dates = df['listing_date'].tolist()
    insert_dates(dates)
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        # Convert dataframe to list of tuples
        df["listing_date"] = pd.to_datetime(df["listing_date"], format="%d/%m/%Y")
        data_tuples = [tuple(x) for x in df.to_numpy()]

        # Create INSERT query dynamically
        columns = ', '.join(df.columns)
        values_placeholder = ', '.join(['%s'] * len(df.columns))
        insert_query = f"""
        INSERT INTO dim_enterprises ({columns}) 
        VALUES ({values_placeholder})
        ON CONFLICT (stock_code) 
        DO UPDATE SET 
            {', '.join([f"{col} = EXCLUDED.{col}" for col in df.columns if col != "stock_code"])}
        """

        # Execute batch insert
        cur.executemany(insert_query, data_tuples)
        conn.commit()

        print(f"Successfully inserted {len(data_tuples)} rows into dim_enterprises")

    except Exception as e:
        print(f"Error: {e}")
        print(df["listing_date"])
    finally:
        cur.close()
        conn.close()


def insert_sub_companies():
    csv_path = os.path.join(BASE_DIR, "data/raw/sub_companies.csv")
    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        # Read CSV file
        df = pd.read_csv(csv_path, sep="|", index_col=False)
        df = df.rename({
            "stock_code": "parent_stock_code",
            "comp_name": "sub_company_name",
            "comp_type": "company_type"
        }, axis="columns")
        df["ownership_ratio"] = df["ownership_ratio"].apply(lambda x: str(x).replace("%", ""))
        df["charter_capital"] = df["charter_capital"].apply(lambda x: str(x).replace(",", ""))
        df["contributed_capital"] = df["contributed_capital"].apply(lambda x: str(x).replace(",", ""))

        # Convert dataframe to list of tuples
        data_tuples = [tuple(x) for x in df.to_numpy()]

        # Create INSERT query dynamically
        columns = ', '.join(df.columns)
        values_placeholder = ', '.join(['%s'] * len(df.columns))
        insert_query = f"""
            INSERT INTO dim_enterprises_sub_companies ({columns}) 
            VALUES ({values_placeholder})
            ON CONFLICT (parent_stock_code, sub_company_name) 
            DO UPDATE SET 
                {', '.join([f"{col} = EXCLUDED.{col}" for col in df.columns if col not in ["parent_stock_code",
                                                                                           "sub_company_name"]])}
            """

        # Execute batch insert
        cur.executemany(insert_query, data_tuples)
        conn.commit()

        print(f"Successfully inserted {len(data_tuples)} rows into dim_enterprises_sub_companies")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def insert_transaction_hist():
    df = pd.read_csv(os.path.join(BASE_DIR, "data/transformed/transaction_history.csv"),
                     index_col=False)
    df = df.fillna(-1)
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        insert_dates_transformed(df['transaction_date'].tolist())
        data_tuples = [tuple(x) for x in df.to_numpy()]

        columns = ', '.join(df.columns)
        values_placeholder = ', '.join(['%s'] * len(df.columns))
        insert_query = f"""
                INSERT INTO fact_transaction_history ({columns}) 
                VALUES ({values_placeholder})
                ON CONFLICT (stock_code, transaction_date) 
                DO UPDATE SET 
                    {', '.join([f"{col} = EXCLUDED.{col}" for col in df.columns if col not in ["stock_code",
                                                                                               "transaction_date"]])}
                """

        # Execute batch insert
        cur.executemany(insert_query, data_tuples)
        conn.commit()

        print(f"Successfully inserted {len(data_tuples)} rows into fact_transaction_history")

    except Exception as e:
        raise e
    finally:
        cur.close()
        conn.close()


def insert_financial_facts():
    df = pd.read_csv(os.path.join(BASE_DIR, "data/transformed/aggregated_financial.csv"), index_col=False)
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        insert_dates_transformed(df['date_key'].tolist())
        df = df.rename({'date_key': 'financial_year'}, axis="columns")
        df = df.drop(["time"], axis="columns")
        data_tuples = [tuple(x) for x in df.to_numpy()]

        columns = ', '.join(df.columns)
        values_placeholder = ', '.join(['%s'] * len(df.columns))
        insert_query = f"""
                    INSERT INTO fact_financial_statement ({columns}) 
                    VALUES ({values_placeholder})
                    ON CONFLICT (stock_code, financial_year) 
                    DO UPDATE SET 
                        {', '.join([f"{col} = EXCLUDED.{col}" for col in df.columns if col not in ["stock_code",
                                                                                                   "financial_year"]])}
                    """

        # Execute batch insert
        cur.executemany(insert_query, data_tuples)
        conn.commit()

        print(f"Successfully inserted {len(data_tuples)} rows into fact_financial_statement")

    except Exception as e:
        raise e
    finally:
        cur.close()
        conn.close()