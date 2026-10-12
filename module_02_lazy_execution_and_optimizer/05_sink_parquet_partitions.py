import polars as pl
import numpy as np
import os

os.makedirs("partitions_data", exist_ok=True)

# 1. Подготовка тестовых партиций
for part_id in [1, 2, 3]:
    n = 100_000
    df_part = pl.DataFrame({
        "order_id": np.arange((part_id - 1) * n + 1, part_id * n + 1),
        "region": np.random.choice(["North", "South", "East", "West"], size=n),
        "margin": np.random.uniform(-50.0, 500.0, size=n).round(2),
        "is_fraud": np.random.choice([0, 1], p=[0.98, 0.02], size=n)
    })
    df_part.write_parquet(f"partitions_data/orders_part_{part_id}.parquet")

# =====================================================================
# РЕШЕНИЕ АВТОРА (Потоковое считывание партиций и сброс на диск):
# =====================================================================
sink_path = "profitable_orders.parquet"

lf = (
    pl.scan_parquet("partitions_data/orders_part_*.parquet")
    .filter((pl.col("is_fraud") == 0) & (pl.col("margin") > 100.0))
    .select("order_id", "region", "margin")
)

lf.sink_parquet(sink_path)

if __name__ == "__main__":
    df_preview = pl.read_parquet(sink_path, n_rows=5)
    print("--- Первые 5 строк потокового файла (profitable_orders.parquet) ---")
    print(df_preview)
