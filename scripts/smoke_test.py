from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.algotrading_backtester import make_sample_price_data, run_pipeline


def main() -> None:
    enriched, metrics, trades = run_pipeline(make_sample_price_data())
    assert {"SMA_30", "MACD", "RSI", "ADX", "Combined_Signal"}.issubset(enriched.columns)
    assert metrics.initial_capital == 1000.0
    closed_trades = 0 if trades.empty else len(trades[trades["action"] != "buy"])
    assert metrics.total_trades == closed_trades
    print(metrics)


if __name__ == "__main__":
    main()
