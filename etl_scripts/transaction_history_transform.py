from utils import BASE_DIR
import os

import pandas as pd
import json

col_mappers = []
for i in range(1, 5):
    with open(os.path.join(BASE_DIR, f"data/transformed/transaction_history_cols_mapper_{i}.json"), "r") as f:
        col_mappers.append(json.load(f))


def concat_from_folder(folder_path) -> pd.DataFrame:
    enterprise_folders = [f for f in os.listdir(folder_path) if f.endswith("_csv")]
    dfs = []
    for folder in enterprise_folders:
        path = os.listdir(os.path.join(folder_path, folder))
        if len(path) != 53:
            continue
        df = pd.concat([pd.read_csv(os.path.join(folder_path, folder, p)) for p in path], ignore_index=True,
                       axis="rows")
        df['stock_code'] = str(folder[:3])
        dfs.append(df)

    final_df = pd.concat(dfs, ignore_index=True, axis="rows")
    final_df['transaction_date'] = pd.to_datetime(final_df['Ngày'], format="%d/%m/%Y")
    return final_df


def transform_trans_history():
    save_path = os.path.join(BASE_DIR, "data/transformed/transaction_history.csv")
    if os.path.exists(save_path):
        return
    cafe_1 = concat_from_folder(os.path.join(BASE_DIR, "data/processed_financial_statement/cafef-his-1"))
    cafe_2 = concat_from_folder(os.path.join(BASE_DIR, "data/processed_financial_statement/cafef-his-2"))
    cafe_3 = concat_from_folder(os.path.join(BASE_DIR, "data/processed_financial_statement/cafef-his-3"))
    cafe_4 = concat_from_folder(os.path.join(BASE_DIR, "data/processed_financial_statement/cafef-his-4"))

    cafe_1 = cafe_1.drop([c for c in cafe_1.columns if c not in col_mappers[0]], axis="columns")
    cafe_1 = cafe_1.rename(col_mappers[0], axis="columns")
    cafe_2 = cafe_2.drop([c for c in cafe_2.columns if c not in col_mappers[1]], axis="columns")
    cafe_2 = cafe_2.rename(col_mappers[1], axis="columns")
    cafe_3 = cafe_3.drop([c for c in cafe_3.columns if c not in col_mappers[2]], axis="columns")
    cafe_3 = cafe_3.rename(col_mappers[2], axis="columns")
    cafe_4 = cafe_4.drop([c for c in cafe_4.columns if c not in col_mappers[3]], axis="columns")
    cafe_4 = cafe_4.rename(col_mappers[3], axis="columns")

    merge_df = cafe_1.merge(cafe_2, how="outer", on=["stock_code", "transaction_date"], suffixes=("_1", '_2'))
    merge_df = merge_df.merge(cafe_3, how="outer", on=["stock_code", "transaction_date"], suffixes=("_2", "_3"))
    merge_df = merge_df.merge(cafe_4, how="outer", on=["stock_code", "transaction_date"], suffixes=("_3", "_4"))
    for e in merge_df.columns:
        print(e)

    for col in merge_df.columns:
        merge_df[col] = merge_df[col].apply(lambda x: str(x).replace(",", ""))
    merge_df['foreign_ownership'] = merge_df['foreign_ownership'].apply(lambda x: str(x).replace("%", ""))

    merge_df = merge_df.replace("nan", None)
    merge_df.to_csv(save_path, index=False)

