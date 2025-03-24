import gymnasium as gym
from gymnasium import spaces
import numpy as np
from stable_baselines3.common.env_util import make_vec_env


class PortfolioEnv(gym.Env):
    def __init__(self, df, stock_list, window_size=120, initial_balance=1.0):
        super(PortfolioEnv, self).__init__()

        self.df = df
        self.stock_list = stock_list
        self.window_size = window_size
        self.initial_balance = initial_balance

        self.current_step = window_size
        self.done = False
        self.num_stocks = len(stock_list)
        self.returns = []

        # State: past `window_size` days of stock prices (normalized)
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(window_size, self.num_stocks), dtype=np.float32)

        # Action: Portfolio allocation (weights sum to 1)
        self.action_space = spaces.Box(low=0, high=1, shape=(self.num_stocks,), dtype=np.float32)

        # Portfolio balance
        self.current_balance = initial_balance
        self.last_price = None

    def reset(self, seed=None, option=None):
        super().reset(seed=seed, options=option)

        self.current_step = self.window_size
        self.current_balance = self.initial_balance
        self.done = False
        return self._get_observation(), {}

    def _get_observation(self):
        prices = self.df.iloc[self.current_step - self.window_size: self.current_step][self.stock_list]
        return prices.to_numpy().astype(np.float32)

    def step(self, action):
        if self.done:
            return self._get_observation(), 0, self.done, {}

        action /= action.sum()

        prices_t = self.df.iloc[self.current_step][self.stock_list].to_numpy()
        prices_t1 = self.df.iloc[self.current_step + 1][self.stock_list].to_numpy()

        returns = (prices_t1 - prices_t) / prices_t
        portfolio_return = np.dot(action, returns)
        self.returns.append(portfolio_return)
        volatility_penalty = -np.std(np.array(returns)) * 0.1

        self.current_balance *= (1 + portfolio_return)

        reward = (portfolio_return + volatility_penalty) * 1000

        self.current_step += 1
        if self.current_step >= len(self.df) - 1:
            self.done = True

        return self._get_observation(), reward, self.done, False, {}
