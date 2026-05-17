# Quantitative AlgoTrading Backtester

This repository contains my Finance and Analytics Club, IIT Kanpur winter project submission for building an end-to-end algorithmic trading workflow on **TCS 2023 daily price data**.

## What This Project Shows

- Implemented technical indicators from scratch: **SMA, EMA, Bollinger Bands, MACD, Stochastic Oscillator, RSI, ADX, and ATR**.
- Converted indicators into buy/sell signal functions and compared signal counts.
- Combined multiple indicators into a weighted trading signal.
- Built a Python backtesting engine for long trades with stop-loss and take-profit rules.
- Reported trading metrics including profit, total trades, win/loss count, maximum drawdown, and Sharpe ratio.

## Backtest Snapshot

| Metric | Value |
| --- | ---: |
| Initial capital | INR 1,000 |
| Final capital | INR 2,176.29 |
| Profit | INR 1,176.29 |
| Total trades | 18 |
| Winning trades | 8 |
| Losing trades | 10 |
| Stop-loss | 2% |
| Take-profit | 3% |
| Maximum drawdown | 56.47% |
| Sharpe ratio | 0.09 |

The strategy was built as a learning project, so the drawdown and Sharpe ratio are important context: the engine works, while the strategy still needs risk and signal-quality refinement before any real-world use.

## Repository Structure

```text
notebooks/
  01_technical_indicators.ipynb   # Indicator implementations
  02_signal_generation.ipynb      # Buy/sell signals from indicators
  03_backtesting_engine.ipynb     # Backtest engine and metrics

docs/
  final_assignment_prompt.pdf     # Original project prompt
```

## How To Review

Start with `notebooks/03_backtesting_engine.ipynb` for the complete workflow, then inspect the first two notebooks for indicator and signal-generation logic.

## Tech Stack

Python, Pandas, NumPy, Matplotlib, yfinance

