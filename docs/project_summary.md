# Project Summary

## Context

This Finance and Analytics Club project asked participants to build a complete algorithmic trading workflow on TCS 2023 daily price data: technical indicators, signal generation, and a backtesting engine.

## What I Built

- Implemented moving-average, momentum, volatility, and trend-following indicators.
- Converted each indicator into a buy/sell signal function.
- Combined signals through weighted aggregation.
- Built a backtesting class that handles long entries, exits, stop-loss, take-profit, trade logs, equity curve, returns, maximum drawdown, and Sharpe ratio.

## Indicators Covered

- SMA and EMA
- Bollinger Bands
- MACD
- Stochastic Oscillator
- RSI
- ADX
- ATR

## Output Snapshot

- Initial capital: INR 1,000
- Final capital: INR 1,186.25
- Profit: INR 186.25
- Total return: 18.62%
- Total trades: 26
- Winning trades: 12
- Losing trades: 14
- Stop-loss: 2%
- Take-profit: 3%
- Maximum drawdown: -6.74%
- Sharpe ratio: 1.25

## Honest Interpretation

This is strongest as a backtesting-engine and indicator-implementation project. The strategy output is not presented as deployment-ready; it is a reproducible way to reason about signal quality, trade exits, and risk metrics.
