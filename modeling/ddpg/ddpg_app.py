import pandas as pd
from stable_baselines3 import DDPG
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.env_checker import check_env
import numpy as np
from stable_baselines3.common.noise import OrnsteinUhlenbeckActionNoise

# Tham số OU Noise
theta = 0.15  # Điều khiển xu hướng quay về trung bình
sigma = 0.2   # Mức độ nhiễu

import json

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
start_training = last_date - pd.DateOffset(months=30)
end_training = last_date - pd.DateOffset(months=6)

# Filter the dataset
train_df = pivot_df[pivot_df.index < end_training]

stock_list_from_fin = {"GAS", "FPT", "VNM", "PLX", "LPB"}
stock_list_from_hist = {"FPT", "MWG", "HDB", "VCB", "SSI"}
stock_list_from_return = mean_historical_return(train_df[-120:]).sort_values(ascending=False)[:5]
stock_list_from_return = stock_list_from_return[stock_list_from_return >= 0]
stock_list_from_return = set(stock_list_from_return.index)
# stock_list = stock_list_from_return
stock_list = stock_list_from_return.intersection(stock_list_from_fin.union(stock_list_from_hist))
stock_list = list(stock_list)
print(stock_list)

env = PortfolioEnv(train_df, stock_list)
vec_env = make_vec_env(PortfolioEnv, n_envs=1, env_kwargs={"df": train_df, "stock_list": stock_list})


# Add noise to encourage exploration
# n_actions = env.action_space.shape[-1]
# action_noise = NormalActionNoise(mean=
# np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))
# Initialize DDPG model
action_noise = OrnsteinUhlenbeckActionNoise(
    mean=np.zeros(env.action_space.shape[-1]),
    sigma=sigma * np.ones(env.action_space.shape),
    theta=theta * np.ones(env.action_space.shape),
)

model = DDPG("MlpPolicy", env, action_noise=action_noise, verbose=1, learning_rate=1e-3)
# Train the model
model.learn(total_timesteps=100000)
# Save model
model.save("models/ddpg_portfolio")

obs, info = env.reset()
done = False

port_values = []

while not done:
    action, _state = model.predict(obs)
    action = np.clip(action, 0, 1)  # Ensure weights are non-negative
    action /= action.sum() if action.sum() > 0 else 1
    obs, reward, done, _, _ = env.step(action)
    port_values.append(env.current_balance)
    if done:
        optimized_weights = {stock_list[i]: float(action[i]) for i in range(len(stock_list))}

port_values.insert(0, 1)

print(len(port_values))

annual_return = compute_annual_return(port_values)
annual_volatility = compute_annual_volatility(port_values, days_held=1)
sharpe_ratio = calculate_sharpe_ratio(annual_return, annual_volatility)

print("=" * 8 + "DDPG TRAINING RESULTS" + "=" * 8)
print(f"Annual Return: {annual_return}")
print(f"Annual volatility: {annual_volatility}")
print(f"Sharpe Ratio: {sharpe_ratio}")

print("=" * 8 + "MARKOWITZ TRAINING RESULTS" + "=" * 8)
m_weights, performance = optimize_markowitz(train_df, stock_list)
print(f"Optimized weights: {m_weights}")


with open("m_weights.json", "w") as f:
    json.dump(m_weights, f)

with open("d_weights.json", "w") as f:
    json.dump(optimized_weights, f)

