import os.path
import re
import pandas as pd
from utils import BASE_DIR
from time_utils import transform_time_str_to_date


def map_eng_vi(eng_file_path, check_df: pd.DataFrame = None):
    with open(eng_file_path, 'r') as f:
        text = f.read()
        eng_fields = [str(line) for line in text.split("\n")]

    if check_df is None:
        df = pd.read_csv("/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2/data/processed_financial_statement"
                         "/cash_flow/VIC_transformed.csv", index_col=False)
    else:
        df = check_df
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    df = df.drop(columns=unnamed_cols, errors='ignore')
    drop_cols = [
        "stock_code",
        "time",
        "I. Lưu chuyển tiền từ hoạt động kinh doanh",
        "2. Điều chỉnh cho các khoản",
        "II. Lưu chuyển tiền từ hoạt động đầu tư",
        "III. Lưu chuyển tiền từ hoạt động tài chính",
        'Lưu chuyển tiền thuần từ hoạt động tài chính',
        'Lưu chuyển tiền thuần trong kỳ',
        'Tiền và tương đương tiền đầu kỳ',
        'Ảnh hưởng của thay đổi tỷ giá hối đoái quy đổi ngoại tệ',
        'Tiền và tương đương tiền cuối kỳ'
    ]
    vi_fields = [c for c in df.columns.tolist() if c not in drop_cols]
    mapper = {vi_fields[i]: eng_fields[i] for i in range(len(vi_fields))}
    return mapper


def get_corrected_dfs():
    folder = os.path.join(BASE_DIR, "data/processed_financial_statement/cash_flow")
    filenames = os.listdir(folder)
    dfs = []
    for file in filenames:
        df = pd.read_csv(os.path.join(folder, file), index_col=False)
        try:
            mapper = map_eng_vi("/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2/data/raw/english_fields_cashflow"
                                ".txt",
                                df)
            keep_cols = [c for c in mapper.keys()]
            keep_cols.extend(["stock_code", "time"])
            df = df.drop([c for c in df.columns if c not in keep_cols], axis="columns")
            df = df.rename(mapper, axis="columns")
            dfs.append(df)
        except Exception:
            continue

    return pd.concat(dfs, axis="rows")


def transform_cashflow():
    save_path = os.path.join(BASE_DIR, "data/transformed/transformed_cashflow.csv")
    if os.path.exists(save_path):
        return
    df = get_corrected_dfs()
    df['date_key'] = df['time'].apply(transform_time_str_to_date)
    df = df.reset_index(drop=True)
    df.to_csv(save_path, index=False)

