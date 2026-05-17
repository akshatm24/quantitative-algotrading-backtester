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

Latest reproducible module run on `TCS.NS` daily data for 2023:

| Metric | Value |
| --- | ---: |
| Initial capital | INR 1,000 |
| Final capital | INR 1,186.25 |
| Profit | INR 186.25 |
| Total return | 18.62% |
| Total trades | 26 |
| Winning trades | 12 |
| Losing trades | 14 |
| Stop-loss | 2% |
| Take-profit | 3% |
| Maximum drawdown | -6.74% |
| Sharpe ratio | 1.25 |

The strategy was built as a learning project. I include both returns and risk metrics because the main contribution is the reproducible indicator/signal/backtest workflow, not an investment recommendation.

## Resume Claim Traceability

| Resume claim | Where to verify |
| --- | --- |
| 8 technical indicators | `src/algotrading_backtester.py`, `notebooks/01_technical_indicators.ipynb` |
| Indicator-wise signal functions | `src/algotrading_backtester.py`, `notebooks/02_signal_generation.ipynb` |
| Weighted combined signal and backtester | `src/algotrading_backtester.py`, `docs/tcs_2023_metrics.json` |
| Stop-loss, take-profit, trade logs, drawdown, Sharpe | `src/algotrading_backtester.py`, `docs/validation.md` |

## Repository Structure

```text
src/
  algotrading_backtester.py       # Reusable indicators, signal logic, and backtest engine

scripts/
  smoke_test.py                   # Deterministic local validation

notebooks/
  01_technical_indicators.ipynb   # Indicator implementations
  02_signal_generation.ipynb      # Buy/sell signals from indicators
  03_backtesting_engine.ipynb     # Backtest engine and metrics

docs/
  backtest_metrics.json           # Deterministic sample-data run
  tcs_2023_metrics.json           # Latest verified TCS.NS 2023 module run
  final_assignment_prompt.pdf     # Original project prompt
  project_summary.md              # Short reviewer-facing explanation
  validation.md                   # Local checks run before publishing

requirements.txt                  # Python environment outline
```

## Run Locally

```bash
python3 -m pip install -r requirements.txt
python3 -m compileall src scripts
python3 scripts/smoke_test.py
python3 -m src.algotrading_backtester --sample
python3 -m src.algotrading_backtester --ticker TCS.NS --start 2023-01-01 --end 2023-12-31 --output docs/tcs_2023_metrics.json
```

## How To Review

Start with `docs/project_summary.md` and `docs/validation.md`, then review `src/algotrading_backtester.py` for the clean reusable implementation. The notebooks preserve the original exploratory workflow.

## Tech Stack

Python, Pandas, NumPy, Matplotlib, yfinance
