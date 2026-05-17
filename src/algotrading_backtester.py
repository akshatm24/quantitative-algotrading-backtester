from __future__ import annotations

from dataclasses import dataclass, asdict
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def make_sample_price_data(periods: int = 180, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2023-01-02", periods=periods, freq="B")
    trend = np.linspace(0, 18, periods)
    shocks = rng.normal(0, 1.6, periods).cumsum()
    close = 3200 + trend + shocks
    high = close + rng.uniform(8, 35, periods)
    low = close - rng.uniform(8, 35, periods)
    open_ = close + rng.normal(0, 8, periods)
    volume = rng.integers(900_000, 2_500_000, periods)
    return pd.DataFrame({"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume}, index=dates)


def fetch_price_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    import yfinance as yf

    data = yf.Ticker(ticker).history(start=start, end=end, interval="1d", auto_adjust=True)
    if data.empty:
        raise ValueError(f"No price data returned for {ticker} between {start} and {end}")
    return data[["Open", "High", "Low", "Close", "Volume"]].dropna()


def add_indicators(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    close = df["Close"]
    high = df["High"]
    low = df["Low"]

    df["SMA_30"] = close.rolling(30).mean()
    df["EMA_12"] = close.ewm(span=12, adjust=False).mean()
    df["EMA_26"] = close.ewm(span=26, adjust=False).mean()
    df["Middle_Band"] = df["SMA_30"]
    rolling_std = close.rolling(30).std()
    df["Upper_Band"] = df["Middle_Band"] + 2 * rolling_std
    df["Lower_Band"] = df["Middle_Band"] - 2 * rolling_std
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["Stochastic"] = (close - low.rolling(14).min()) / (high.rolling(14).max() - low.rolling(14).min()) * 100

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))

    prev_close = close.shift(1)
    true_range = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    df["ATR"] = true_range.rolling(14).mean()

    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    atr = df["ATR"].replace(0, np.nan)
    df["+DI"] = 100 * pd.Series(plus_dm, index=df.index).rolling(14).sum() / atr
    df["-DI"] = 100 * pd.Series(minus_dm, index=df.index).rolling(14).sum() / atr
    dx = ((df["+DI"] - df["-DI"]).abs() / (df["+DI"] + df["-DI"]).replace(0, np.nan)) * 100
    df["ADX"] = dx.rolling(14).mean()
    return df


def add_signals(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df["Signal_Bollinger"] = np.select(
        [df["Close"] < df["Lower_Band"], df["Close"] > df["Upper_Band"]],
        [1, -1],
        default=0,
    )
    df["Signal_MACD"] = np.select([df["MACD"] > df["MACD_Signal"], df["MACD"] < df["MACD_Signal"]], [1, -1], default=0)
    df["Signal_Stochastic"] = np.select([df["Stochastic"] < 20, df["Stochastic"] > 80], [1, -1], default=0)
    df["Signal_RSI"] = np.select([df["RSI"] < 30, df["RSI"] > 70], [1, -1], default=0)
    df["Signal_ATR"] = np.select(
        [df["Close"] > df["Close"].shift(1) + 1.4 * df["ATR"], df["Close"] < df["Close"].shift(1) - 1.4 * df["ATR"]],
        [1, -1],
        default=0,
    )
    df["Signal_ADX"] = np.select(
        [(df["+DI"] > df["-DI"]) & (df["ADX"] > 25), (df["+DI"] < df["-DI"]) & (df["ADX"] > 25)],
        [1, -1],
        default=0,
    )
    weights = {
        "Signal_Bollinger": 0.15,
        "Signal_MACD": 0.25,
        "Signal_Stochastic": 0.15,
        "Signal_RSI": 0.15,
        "Signal_ATR": 0.20,
        "Signal_ADX": 0.10,
    }
    df["Weighted_Signal"] = sum(df[column] * weight for column, weight in weights.items())
    df["Combined_Signal"] = np.select([df["Weighted_Signal"] > 0, df["Weighted_Signal"] < 0], [1, -1], default=0)
    return df


@dataclass(frozen=True)
class BacktestMetrics:
    initial_capital: float
    final_capital: float
    profit: float
    total_return_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    max_drawdown_pct: float
    sharpe_ratio: float
    stop_loss_pct: float
    take_profit_pct: float


def run_backtest(
    data: pd.DataFrame,
    initial_capital: float = 1000.0,
    stop_loss_pct: float = 0.02,
    take_profit_pct: float = 0.03,
    risk_free_rate: float = 0.01,
) -> tuple[BacktestMetrics, pd.DataFrame]:
    df = data.dropna(subset=["Close", "Combined_Signal"]).copy()
    cash = initial_capital
    position = 0.0
    entry_price = 0.0
    entry_value = 0.0
    trade_rows: list[dict[str, object]] = []
    equity_curve: list[float] = []
    wins = 0
    losses = 0

    for date, row in df.iterrows():
        price = float(row["Close"])
        signal = int(row["Combined_Signal"])
        if position == 0 and signal == 1:
            entry_value = cash
            position = cash / price
            entry_price = price
            cash = 0.0
            trade_rows.append({"date": date, "action": "buy", "price": price, "capital": entry_value})
        elif position > 0:
            exit_reason = None
            if price <= entry_price * (1 - stop_loss_pct):
                exit_reason = "stop_loss"
            elif price >= entry_price * (1 + take_profit_pct):
                exit_reason = "take_profit"
            elif signal == -1:
                exit_reason = "signal_exit"

            if exit_reason:
                cash = position * price
                pnl = cash - entry_value
                wins += int(pnl > 0)
                losses += int(pnl <= 0)
                trade_rows.append({"date": date, "action": exit_reason, "price": price, "capital": cash, "pnl": pnl})
                position = 0.0
                entry_price = 0.0
                entry_value = 0.0

        equity_curve.append(cash + position * price)

    if position > 0:
        final_price = float(df["Close"].iloc[-1])
        cash = position * final_price
        pnl = cash - entry_value
        wins += int(pnl > 0)
        losses += int(pnl <= 0)
        trade_rows.append({"date": df.index[-1], "action": "final_exit", "price": final_price, "capital": cash, "pnl": pnl})
        equity_curve.append(cash)

    equity = pd.Series(equity_curve, dtype=float)
    returns = equity.pct_change().dropna()
    max_drawdown = ((equity / equity.cummax()) - 1).min() if not equity.empty else 0.0
    sharpe = 0.0
    if returns.std(ddof=0) and not np.isnan(returns.std(ddof=0)):
        daily_rf = risk_free_rate / 252
        sharpe = float(((returns.mean() - daily_rf) / returns.std(ddof=0)) * np.sqrt(252))

    metrics = BacktestMetrics(
        initial_capital=round(initial_capital, 2),
        final_capital=round(float(cash), 2),
        profit=round(float(cash - initial_capital), 2),
        total_return_pct=round(float((cash / initial_capital - 1) * 100), 2),
        total_trades=wins + losses,
        winning_trades=wins,
        losing_trades=losses,
        max_drawdown_pct=round(float(max_drawdown * 100), 2),
        sharpe_ratio=round(sharpe, 2),
        stop_loss_pct=stop_loss_pct,
        take_profit_pct=take_profit_pct,
    )
    trades = pd.DataFrame(trade_rows)
    return metrics, trades


def run_pipeline(data: pd.DataFrame) -> tuple[pd.DataFrame, BacktestMetrics, pd.DataFrame]:
    enriched = add_signals(add_indicators(data))
    metrics, trades = run_backtest(enriched)
    return enriched, metrics, trades


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the algotrading backtest.")
    parser.add_argument("--ticker", default="TCS.NS")
    parser.add_argument("--start", default="2023-01-01")
    parser.add_argument("--end", default="2023-12-31")
    parser.add_argument("--sample", action="store_true", help="Use deterministic sample data instead of downloading prices.")
    parser.add_argument("--output", default="docs/backtest_metrics.json")
    args = parser.parse_args()

    data = make_sample_price_data() if args.sample else fetch_price_data(args.ticker, args.start, args.end)
    _, metrics, trades = run_pipeline(data)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(metrics), indent=2), encoding="utf-8")
    print(json.dumps(asdict(metrics), indent=2))
    print(f"trades={len(trades)}")


if __name__ == "__main__":
    main()
