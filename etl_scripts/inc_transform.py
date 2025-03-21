import os
import re

import pandas as pd

from time_utils import transform_time_str_to_date
from utils import BASE_DIR


def map_eng_vi(eng_file_path, check_df: pd.DataFrame = None):
    with open(eng_file_path, 'r') as f:
        text = f.read()
        eng_fields = [str(line) for line in text.split("\n")]

    if check_df is None:
        df = pd.read_csv("/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2/data/processed_financial_statement"
                         "/inc_state/VIC_transformed.csv", index_col=False)
    else:
        df = check_df
    df = df.drop(['Unnamed: 2'], axis="columns")
    vi_fields = [str(col) for col in df.columns if col not in ['stock_code', 'time', 'Phần lợi nhuận/lỗ từ công ty '
                                                                                     'liên kết liên doanh']]

    mapper = {vi_fields[i]: eng_fields[i] for i in range(len(eng_fields))}
    return mapper, vi_fields, eng_fields


def get_correct_structure_enterprises():
    folder = os.path.join(BASE_DIR, "data/processed_financial_statement/inc_state")
    filenames = os.listdir(folder)
    dfs = []
    for file in filenames:
        df = pd.read_csv(os.path.join(folder, file), index_col=False)
        try:
            vi_to_eng, vi_f, eng_f = map_eng_vi(os.path.join(BASE_DIR, "data/raw"
                                                                       "/english_fields_inc.txt"))
            vi_f.extend(['stock_code', 'time'])
            df = df.drop([col for col in df.columns if col not in vi_f], axis="columns")
            df = df.rename(vi_to_eng, axis="columns")
            dfs.append(df)
        except Exception as e:
            print(e)
            continue
    return pd.concat(dfs, axis="rows")


def transform_inc_state():
    save_path = os.path.join(BASE_DIR, "data/transformed/transformed_inc.csv")
    if os.path.exists(save_path):
        return
    df = get_correct_structure_enterprises()
    df = df.reset_index(drop=True)
    df['date_key'] = df['time'].apply(transform_time_str_to_date)
    df.to_csv(save_path, index=False)

