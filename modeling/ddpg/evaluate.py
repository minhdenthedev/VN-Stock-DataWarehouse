import json

import pandas as pd
import numpy as np
from stable_baselines3 import DDPG

from modeling.ddpg.train_env import PortfolioEnv
from utils import *

df = pd.read_csv("/home/m1nhd3n/Works/DataEngineer/DataFlow2025Task2/data/modeling_processed"
                 "/transaction_history_processed.csv", index_col=False)

price_df = df[["stock_code", "transaction_date", "closing_price"]]
price_df["transaction_date"] = pd.to_datetime(price_df["transaction_date"], format="%Y-%m-%d")
price_df = price_df.set_index("transaction_date")

pivot_df = pd.pivot_table(price_df, columns="stock_code", values="closing_price", index="transaction_date")
pivot_df = pivot_df.dropna()

last_date = pivot_df.index.max()
start_date = last_date - pd.DateOffset(months=6)
test_df = pivot_df[(pivot_df.index >= start_date)]

with open("d_weights.json", "r") as f:
    stock_list = list(json.load(f).keys())
test_env = PortfolioEnv(test_df, stock_list)

done = False
obs, _ = test_env.reset()
port_values = []

model = DDPG.load("models/ddpg_portfolio")

while not done:
    action, _states = model.predict(obs)
    action = np.clip(action, 0, 1)  # Ensure weights are non-negative
    action /= action.sum() if action.sum() > 0 else 1
    print(test_env._get_observation())
    obs, reward, done, _, _ = test_env.step(action)
    port_values.append(test_env.current_balance)


annual_return = compute_annual_return(port_values)
annual_volatility = compute_annual_volatility(port_values)
sharpe_ratio = calculate_sharpe_ratio(annual_return, annual_volatility)

print("=" * 8 + "DDPG TESTING RESULTS" + "=" * 8)
print(f"Annual Return: {annual_return}")
print(f"Portfolio Performance: {port_values[-1]}")
print("=" * 8 + "MARKOWITZ TESTING RESULTS" + "=" * 8)
with open("m_weights.json", "r") as f:
    m_weights = json.load(f)
m_annual_return, m_portfolio_performance = calculate_annual_return_markowitz(m_weights, test_df, stock_list)
m_annual_volatility = calculate_annual_volatility_markowitz(m_weights, test_df, stock_list)
m_sharpe_ratio = calculate_sharpe_ratio(m_annual_return, m_annual_volatility)
print(f"Annual Return: {m_annual_return}")
print(f"Portfolio Performance: {m_portfolio_performance}")

