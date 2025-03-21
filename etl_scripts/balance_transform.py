import os
import re
from datetime import date

import pandas as pd
from utils import BASE_DIR
from time_utils import transform_time_str_to_date


def map_eng_vi(eng_file_path, check_df: pd.DataFrame = None):
    with open(eng_file_path, 'r') as f:
        text = f.read()
        eng_fields = [str(line) for line in text.split("\n")]

    if check_df is None:
        df = pd.read_csv("/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2/data/processed_financial_statement/balance"
                         "/VIC_transformed.csv", index_col=False)
    else:
        df = check_df
    vi_fields = [str(col) for col in df.columns if bool(re.match(r"\d", col))]
    skip_vi_fields = ['2. Dự phòng giảm giá hàng tồn kho (*)']
    skip_eng_fields = ['non_current_assets', 'investment_properties']
    for e in skip_eng_fields:
        eng_fields.remove(e)
    for v in skip_vi_fields:
        vi_fields.remove(v)
    mapper = {vi_fields[i]: eng_fields[i] for i in range(len(eng_fields)) if vi_fields[i]
              not in skip_vi_fields and eng_fields[i] not in skip_eng_fields}
    return mapper, vi_fields, eng_fields


def get_correct_structure_enterprises():
    folder = "/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2/data/processed_financial_statement/balance"
    filenames = os.listdir(folder)
    dfs = []
    for file in filenames:
        df = pd.read_csv(os.path.join(folder, file), index_col=False)
        try:
            vi_to_eng, vi_f, eng_f = map_eng_vi("/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2/data/raw"
                                                "/english_fields_balance.txt", df)
            vi_f.extend(['stock_code', 'time'])
            df = df.drop([col for col in df.columns if col not in vi_f], axis="columns")
            df = df.rename(vi_to_eng, axis="columns")
            dfs.append(df)
        except Exception:
            continue
    return pd.concat(dfs, axis="rows")


def transform_balance():
    save_path = os.path.join(BASE_DIR, "data/transformed/transformed_balance.csv")
    if os.path.exists(save_path):
        return
    df = get_correct_structure_enterprises()
    df = df.reset_index(drop=True)
    df['date_key'] = df['time'].apply(transform_time_str_to_date)
    df.to_csv(save_path, index=False)
