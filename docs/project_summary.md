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
- Final capital: INR 2,176.29
- Total trades: 18
- Winning trades: 8
- Losing trades: 10
- Stop-loss: 2%
- Take-profit: 3%
- Maximum drawdown: 56.47%
- Sharpe ratio: 0.09

## Honest Interpretation

This is strongest as a backtesting-engine and indicator-implementation project. The strategy output is not presented as deployment-ready because the drawdown and Sharpe ratio show that signal quality needs more refinement.

