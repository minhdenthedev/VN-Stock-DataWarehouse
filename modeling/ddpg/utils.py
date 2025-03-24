import numpy as np
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt import objective_functions
from pypfopt.efficient_frontier import EfficientFrontier


def compute_annual_return(portfolio_values):
    portfolio_values = np.array(portfolio_values)
    ahead_port_values = portfolio_values[1:]
    portfolio_values = portfolio_values[:-1]
    annual_returns = []
    for i in range(len(ahead_port_values)):
        annual_returns.append(
            ((ahead_port_values[i] - portfolio_values[i]) / portfolio_values[i])
        )

    return (1 + np.average(np.array(annual_returns))) ** 252 - 1


def compute_annual_volatility(portfolio_values, days_held=120):
    portfolio_values = np.array(portfolio_values)
    ahead_port_values = portfolio_values[1:]
    portfolio_values = portfolio_values[:-1]
    annual_returns = []
    for i in range(len(ahead_port_values)):
        annual_returns.append(
            ((ahead_port_values[i] - portfolio_values[i]) / portfolio_values[i])
        )

    return (np.std(np.array(annual_returns)) * np.sqrt(252 / days_held))


def calculate_sharpe_ratio(annual_return, annual_volatility, risk_free_rate=0):
    # Convert percentages to decimal form
    rp = annual_return / 100
    rf = risk_free_rate / 100
    sigma_p = annual_volatility / 100

    # Avoid division by zero
    if sigma_p == 0:
        return float("inf") if rp > rf else float("-inf")

    # Compute Sharpe Ratio
    sharpe_ratio = (rp - rf) / sigma_p

    return sharpe_ratio


def optimize_markowitz(df, stock_list):
    df = df[stock_list]
    mu = mean_historical_return(df)
    S = CovarianceShrinkage(df).ledoit_wolf()
    ef = EfficientFrontier(mu, S)
    ef.add_objective(objective_functions.L2_reg, gamma=0.1)
    weights = ef.max_sharpe()
    return weights, ef.portfolio_performance(verbose=True)


def calculate_annual_return_markowitz(weights, df, stock_list):
    df = df[stock_list]
    weights = np.array(list(weights.values()), dtype=np.float64)
    initial_price = df.iloc[0].to_numpy()
    final_price = df.iloc[-1].to_numpy()
    individual_returns = (final_price - initial_price) / initial_price
    portfolio_return = np.dot(weights, individual_returns)
    portfolio_performance = 1 + portfolio_return
    num_days = len(df)
    annual_return = (1 + portfolio_return) ** (252 / num_days) - 1

    return annual_return, portfolio_performance


def calculate_annual_volatility_markowitz(weights, df, stock_list):
    df = df[stock_list]  # Select relevant stocks

    # Convert OrderedDict weights to NumPy array
    weights = np.array(list(weights.values()), dtype=np.float64)

    # Calculate daily returns
    daily_returns = df.pct_change().dropna()  # Compute percentage change (daily returns)

    # Compute covariance matrix of daily returns
    cov_matrix = daily_returns.cov().to_numpy()

    # Portfolio standard deviation (volatility)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    # Annualized volatility
    annual_volatility = portfolio_volatility * np.sqrt(252)

    return annual_volatility
