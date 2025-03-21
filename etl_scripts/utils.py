import os
import pandas
import pandas as pd

BASE_DIR = "/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2"


def aggregate_financial_facts():
    folder = os.path.join(BASE_DIR, "data/transformed")
    save_path = os.path.join(folder, "aggregated_financial.csv")
    # if os.path.exists(save_path):
    #     return
    balance_df = pd.read_csv(os.path.join(folder, "transformed_balance.csv"), index_col=False)
    cashflow_df = pd.read_csv(os.path.join(folder, "transformed_cashflow.csv"), index_col=False)
    inc_df = pd.read_csv(os.path.join(folder, "transformed_inc.csv"), index_col=False)
    merged_df = balance_df.merge(cashflow_df, on=["stock_code", "date_key"], how="outer")
    merged_df = merged_df.merge(inc_df, on=['stock_code', 'date_key'], how="outer")
    merged_df = merged_df.drop(["time_x", "time_y",
                                "interest_expenses_x",
                                "government_bond_repurchase_transactions.1",
                                "held_to_maturity_investments.1"], axis="columns")
    merged_df = merged_df.rename({"interest_expenses_y": "interest_expenses"}, axis="columns")
    merged_df = merged_df.fillna(-1)
    merged_df.to_csv(save_path, index=False)

