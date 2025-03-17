import pandas as pd
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from get_enterprise_utils import *
from database_utils import *
import os

from airflow.decorators import dag, task
from datetime import datetime, timedelta

NIEM_YET_URL = "https://cafef.vn/du-lieu/du-lieu-doanh-nghiep.chn"
BASE_DIR = "/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2"


@dag(
    schedule=None,
    catchup=False,
    start_date=datetime(2024, 3, 1)
)
def extract_data_from_sources():
    start = EmptyOperator(task_id="start")
    skip_create_db = EmptyOperator(task_id="skip_create_db")

    load_industries_to_db = PythonOperator(
        task_id="load_industries_into_db",
        python_callable=insert_industries
    )

    check_condition_pg = BranchPythonOperator(
        task_id="check_condition",
        python_callable=branching_postgres
    )

    initiate_postgres = BashOperator(
        task_id='initiate_postgres',
        bash_command='PGPASSWORD="12" pg_restore -U postgres -h localhost -d '
                     'vn_stock_dw /home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2/scripts/sqls/initial.sql',
        env={'PGPASSWORD': '12'},
    )

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def get_list():
        stock_codes = [
            "ACB", "BCM", "BID", "BVH", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG",
            "LPB", "MBB", "MSN", "MWG", "PLX", "SAB", "SHB", "SSB",
            "SSI", "STB",
            "TCB", "TPB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"
        ]
        save_path = os.path.join(BASE_DIR, "data/raw/stock_codes_list.csv")
        if os.path.exists(save_path):
            return pd.read_csv(save_path, sep="|", index_col=False)
        df = pd.DataFrame({"stock_code": stock_codes})
        df.to_csv(save_path, sep='|', index=False)
        return df

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def get_industries_table():
        save_path = os.path.join(BASE_DIR, 'data/raw/industries.csv')
        if os.path.exists(save_path):
            return pd.read_csv(save_path, sep='|', index_col=False)
        df = get_industries_data()
        df.to_csv(save_path, sep='|', index=False)
        return df

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def get_enterprises_data(df):
        try:
            data_folder = os.path.join(BASE_DIR, 'data/raw')
            if os.path.exists(os.path.join(data_folder, 'enterprises.csv')):
                df = pd.read_csv(os.path.join(data_folder, 'enterprises.csv'), sep="|", index_col=False)
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                return df

            df = df.drop_duplicates(subset=['code'])
            df.loc[df['code'] == 'ABA', 'name'] = 'Công ty cổ phần giải pháp thương mại A BA'
            df.loc[df['code'] == 'CRV', 'name'] = 'Công ty Cổ phần Tập đoàn Bất động sản CRV'
            df.loc[df['code'] == 'VTT', 'name'] = 'Công ty Cổ Phần Công nghệ Việt Thành'

            print("Getting enterprises information")
            df = get_all_enterprise_information(df)

            print("Getting industry codes")
            df = get_all_enterprises_industry_code(df)
            df.loc[df['code'] == 'BID', 'industry_code'] = '6419'
            df.loc[df['code'] == 'PDR', 'industry_code'] = '6810'

            print("Getting sub companies")
            sub_companies = get_sub_companies(df)

            print("Saving DFs")
            df.to_csv(os.path.join(data_folder, "enterprises.csv"), sep="|", index=False)
            sub_companies.to_csv(os.path.join(data_folder, "sub_companies.csv"), sep="|", index=False)

            return df
        except Exception as e:
            print(f"Error: {e}")

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def extract_niem_yet(comp_list: pd.DataFrame):
        try:
            site = 'niem_yet'
            url = NIEM_YET_URL
            data_folder = os.path.join(BASE_DIR, 'data/raw')
            save_path = os.path.join(data_folder, site + ".csv")
            if os.path.exists(save_path):
                return pd.read_csv(save_path, sep='|', index_col=False)
            comp_list = comp_list['stock_code'].tolist()
            data = process_url(url, comp_list)
            data.to_csv(save_path, sep="|", index=False)
            return data
        except Exception as e:
            print(f"Error: {e}")

    load_enterprises_into_db = PythonOperator(
        task_id="load_enterprises_into_db",
        python_callable=insert_enterprise
    )

    load_sub_companies_into_db = PythonOperator(
        task_id="load_sub_companies_into_db",
        python_callable=insert_sub_companies
    )

    end = EmptyOperator(task_id="end")

    vn30 = get_list()
    niem_yet = extract_niem_yet(vn30)
    industry_table = get_industries_table()
    get_ent_data = get_enterprises_data(niem_yet)

    start >> check_condition_pg >> [initiate_postgres, skip_create_db] >> end
    start >> vn30 >> niem_yet >> get_ent_data >> load_enterprises_into_db >> load_sub_companies_into_db >> end
    start >> industry_table >> load_industries_to_db >> load_enterprises_into_db


dag = extract_data_from_sources()
