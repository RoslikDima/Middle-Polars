import polars as pl
from datetime import datetime

# 1. Поток рыночных котировок (Quotes)
quotes_data = {
    "timestamp": [
        datetime(2026, 3, 1, 10, 0, 0),
        datetime(2026, 3, 1, 10, 0, 5),
        datetime(2026, 3, 1, 10, 0, 15),
        datetime(2026, 3, 1, 10, 0, 0),
        datetime(2026, 3, 1, 10, 0, 8),
    ],
    "ticker": ["BTC", "BTC", "BTC", "ETH", "ETH"],
    "quote_price": [62000.0, 62150.0, 62400.0, 3400.0, 3425.0]
}

# 2. Фактические сделки клиентов (Trades)
trades_data = {
    "timestamp": [
        datetime(2026, 3, 1, 10, 0, 2),
        datetime(2026, 3, 1, 10, 0, 6),
        datetime(2026, 3, 1, 10, 0, 10),
        datetime(2026, 3, 1, 10, 1, 0),
    ],
    "ticker": ["BTC", "BTC", "ETH", "BTC"],
    "trade_id": [101, 102, 103, 104],
    "execution_price": [62010.0, 62145.0, 3420.0, 62500.0]
}

df_quotes = pl.DataFrame(quotes_data)
df_trades = pl.DataFrame(trades_data)

# =====================================================================
# РЕШЕНИЕ АВТОРА (join_asof с проверкой tolerance):
# =====================================================================
df_quotes = df_quotes.sort("timestamp")
df_trades = df_trades.sort("timestamp")

df_result = (
    df_trades.join_asof(
        df_quotes,
        on="timestamp",
        by="ticker",
        strategy="backward",
        tolerance="10s"
    )
    .with_columns(
        (pl.col("execution_price") - pl.col("quote_price")).alias("slippage")
    )
)

if __name__ == "__main__":
    print("--- Результат выполнения join_asof с допуском 10s ---")
    print(df_result)
