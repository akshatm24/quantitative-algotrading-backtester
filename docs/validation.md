# Validation

Checks run before publishing this portfolio repo:

```bash
python3 -m compileall src scripts
python3 scripts/smoke_test.py
python3 -m src.algotrading_backtester --sample --output docs/backtest_metrics.json
python3 -m src.algotrading_backtester --ticker TCS.NS --start 2023-01-01 --end 2023-12-31 --output docs/tcs_2023_metrics.json
```

Notebook code cells were syntax-checked with `nbformat`.

Latest `TCS.NS` 2023 module result:

```json
{
  "initial_capital": 1000.0,
  "final_capital": 1186.25,
  "profit": 186.25,
  "total_return_pct": 18.62,
  "total_trades": 26,
  "winning_trades": 12,
  "losing_trades": 14,
  "max_drawdown_pct": -6.74,
  "sharpe_ratio": 1.25,
  "stop_loss_pct": 0.02,
  "take_profit_pct": 0.03
}
```

During review, I corrected the reusable module's equity-curve accounting so open positions are valued as `cash + position_value` instead of double-counting cash.
