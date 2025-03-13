import pandas as pd

from get_enterprise_utils import *
import os

from airflow.decorators import dag, task
from datetime import datetime, timedelta

NIEM_YET_URL = "https://cafef.vn/du-lieu/du-lieu-doanh-nghiep.chn"
QUY_URL = "https://cafef.vn/du-lieu/danh-sach-cac-quy-dau-tu.chn"
NGAN_HANG_URL = "https://cafef.vn/du-lieu/danh-sach-cac-ngan-hang.chn"
CHUNG_KHOAN_URL = "https://cafef.vn/du-lieu/danh-sach-cac-cong-ty-chung-khoan.chn"
BASE_DIR = "/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2"


@dag(
    schedule=None,
    catchup=False,
    start_date=datetime(2024, 3, 1)
)
def extract_data_from_sources():
    @task(retries=3, retry_delay=timedelta(minutes=1))
    def get_sub_companies_task(df: pd.DataFrame):
        save_path = os.path.join(BASE_DIR, "data/raw/subcompanies.csv")
        if os.path.exists(save_path):
            return pd.read_csv(save_path, sep="|")
        df = get_sub_companies(df)
        df.to_csv(save_path, sep="|")
        return df

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def get_vn30_list_task():
        save_path = os.path.join(BASE_DIR, "data/raw/vn30_list.csv")
        if os.path.exists(save_path):
            return pd.read_csv(save_path, sep="|")
        df = get_vn30_list()
        df.to_csv(save_path, sep='|')
        return df

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def get_industry_code_of_enterprises(df: pd.DataFrame):
        save_path = os.path.join(BASE_DIR, 'data/raw/e_w_info_industry.csv')
        if os.path.exists(save_path):
            return pd.read_csv(save_path, sep="|")
        df = get_all_enterprises_industry_code(df)
        df.to_csv(save_path, sep="|")
        return df

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def get_more_enterprises_information(df: pd.DataFrame):
        save_path = os.path.join(BASE_DIR, 'data/raw/e_w_info.csv')
        if os.path.exists(save_path):
            return pd.read_csv(save_path, sep='|')
        df = get_all_enterprise_information(df)
        df.to_csv(save_path, sep='|')
        return df

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def get_industries_table():
        save_path = os.path.join(BASE_DIR, 'data/raw/industries.csv')
        if os.path.exists(save_path):
            return pd.read_csv(save_path, sep='|')
        df = get_industries_data()
        df.to_csv(save_path, sep='|')
        return df

    @task()
    def aggregate_companies(df_list=None):
        try:
            dfs = []
            data_folder = os.path.join(BASE_DIR, 'data/raw/enterprises')
            if os.path.exists(os.path.join(data_folder, 'enterprises.csv')):
                return pd.read_csv(os.path.join(data_folder, 'enterprises.csv'))
            if df_list is None:
                filenames = os.listdir(data_folder)
                for filename in filenames:
                    dfs.append(pd.read_csv(os.path.join(data_folder, filename), sep="|"))
            else:
                dfs = df_list

            df = pd.concat(dfs, axis="rows", ignore_index=True)
            df = df.drop_duplicates(subset=['code'])
            df.loc[df['code'] == 'ABA', 'name'] = 'Công ty cổ phần giải pháp thương mại A BA'
            df.loc[df['code'] == 'CRV', 'name'] = 'Công ty Cổ phần Tập đoàn Bất động sản CRV'
            df.loc[df['code'] == 'VTT', 'name'] = 'Công ty Cổ Phần Công nghệ Việt Thành'
            df.to_csv(os.path.join(data_folder, "enterprises.csv"))
            return df
        except Exception as e:
            print(f"Error: {e}")

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def extract_niem_yet(comp_list: pd.DataFrame):
        try:
            site = 'niem_yet'
            url = NIEM_YET_URL
            data_folder = os.path.join(BASE_DIR, 'data/raw/enterprises')
            save_path = os.path.join(data_folder, site + ".csv")
            if os.path.exists(save_path):
                return pd.read_csv(save_path, sep='|')
            comp_list = comp_list['stock_code'].tolist()
            data = process_url(url, comp_list)
            data.to_csv(save_path, sep="|")
            return data
        except Exception as e:
            print(f"Error: {e}")

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def extract_banks(comp_list: pd.DataFrame):
        try:
            site = 'ngan_hang'
            url = NGAN_HANG_URL
            data_folder = os.path.join(BASE_DIR, 'data/raw/enterprises')
            save_path = os.path.join(data_folder, site + ".csv")
            if os.path.exists(save_path):
                return pd.read_csv(save_path, sep='|')
            comp_list = comp_list['stock_code'].tolist()

            data = process_url(url, comp_list)
            data.to_csv(save_path, sep="|")
            return data
        except Exception as e:
            print(f"Error: {e}")

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def extract_stocks(comp_list: pd.DataFrame):
        try:
            site = 'chung_khoan'
            url = CHUNG_KHOAN_URL
            data_folder = os.path.join(BASE_DIR, 'data/raw/enterprises')
            save_path = os.path.join(data_folder, site + ".csv")
            if os.path.exists(save_path):
                return pd.read_csv(save_path, sep='|')
            comp_list = comp_list['stock_code'].tolist()
            data = process_url(url, comp_list)
            data.to_csv(save_path, sep="|")
            return data
        except Exception as e:
            print(f"Error: {e}")

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def fix_missing_industry_code(df: pd.DataFrame):
        save_path = os.path.join(BASE_DIR, 'data/raw/e_w_i_fix.csv')
        if os.path.exists(save_path):
            return pd.read_csv(save_path, sep="|")
        df.loc[df['code'] == 'BID', 'industry_code'] = '6419'
        df.loc[df['code'] == 'PDR', 'industry_code'] = '6810'
        df.to_csv(save_path, sep="|")
        return df

    vn30 = get_vn30_list_task()
    niem_yet = extract_niem_yet(vn30)
    industry_table = get_industries_table()
    aggregate_comps = aggregate_companies([niem_yet])
    enterprises_w_info = get_more_enterprises_information(aggregate_comps)
    enterprises_w_industry = get_industry_code_of_enterprises(enterprises_w_info)
    e_w_i_fix = fix_missing_industry_code(enterprises_w_industry)
    sub_companies = get_sub_companies_task(e_w_i_fix)


dag = extract_data_from_sources()
