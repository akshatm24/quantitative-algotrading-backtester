# Quantitative AlgoTrading Backtester

Public project portfolio for my Finance and Analytics Club, IIT Kanpur winter project on building an end-to-end algorithmic trading workflow.

**Period:** December 2024 - January 2025  
**Dataset:** TCS daily price data for calendar year 2023

## Recruiter Snapshot

- Implemented technical indicators from scratch: **SMA, EMA, Bollinger Bands, MACD, Stochastic Oscillator, RSI, ADX, and ATR**.
- Converted indicators into buy/sell signal functions and compared signal counts.
- Combined multiple indicators into a weighted trading signal.
- Built a Python backtesting engine for long trades with stop-loss and take-profit rules, trade logs, equity curve, and risk metrics.
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

The strategy was built as a learning project. The drawdown and Sharpe ratio are intentionally included because they show honest evaluation: the engine works, while the strategy still needs risk and signal-quality refinement before any real-world use.

## Resume Claim Traceability

| Resume claim | Where to verify |
| --- | --- |
| 8 technical indicators | `notebooks/01_technical_indicators.ipynb` |
| Indicator-wise signal functions | `notebooks/02_signal_generation.ipynb` |
| Weighted combined signal and backtester | `notebooks/03_backtesting_engine.ipynb` |
| Stop-loss, take-profit, trade logs, drawdown, Sharpe | Backtest class and final output cells |

## Repository Structure

```text
notebooks/
  01_technical_indicators.ipynb   # Indicator implementations
  02_signal_generation.ipynb      # Buy/sell signals from indicators
  03_backtesting_engine.ipynb     # Backtest engine and metrics

docs/
  final_assignment_prompt.pdf     # Original project prompt
  project_summary.md              # Short reviewer-facing explanation

requirements.txt                  # Python environment outline
```

## How To Review

Start with `docs/project_summary.md`, then review `notebooks/03_backtesting_engine.ipynb` for the complete workflow. The first two notebooks show indicator and signal-generation logic.

## Tech Stack

Python, Pandas, NumPy, Matplotlib, yfinance
