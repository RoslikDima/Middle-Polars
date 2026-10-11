import polars as pl
import os
import numpy as np

# Проверяем наличие файла на диске
if not os.path.exists("orders_big.parquet"):
    n_rows = 500_000
    data = {
        "order_id": np.arange(1, n_rows + 1),
        "customer_id": np.random.randint(1000, 50000, size=n_rows),
        "category": np.random.choice(["Electronics", "Fashion", "Home", "Books"], size=n_rows),
        "amount": np.random.uniform(10.0, 5000.0, size=n_rows).round(2),
        "status": np.random.choice(["Completed", "Cancelled", "Refunded"], size=n_rows),
        "payload_text": ["long_metadata_text_field_payload"] * n_rows
    }
    pl.DataFrame(data).write_parquet("orders_big.parquet")

# =====================================================================
# РЕШЕНИЕ АВТОРА (Потоковый пайплайн с группировкой и сортировкой):
# =====================================================================
streaming_plan = (
    pl.scan_parquet("orders_big.parquet")
    .filter(pl.col("status") == "Completed")
    .group_by("category").agg(
        pl.col("amount").sum().alias("total_revenue"),
        pl.col("amount").mean().round(2).alias("avg_check"),
        pl.len().alias("orders_count")
    )
    .sort("total_revenue", descending=True)
)

df_streaming_result = streaming_plan.collect(engine="streaming")

if __name__ == "__main__":
    print("--- Результат выполнения Streaming Engine ---")
    print(df_streaming_result)
