import polars as pl
import numpy as np

# 1. Генерация тестового набора данных
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
# РЕШЕНИЕ АВТОРА (scan_parquet + Predicate/Projection Pushdown):
# =====================================================================
lazy_scan = (
    pl.scan_parquet("orders_big.parquet")
    .filter((pl.col("status") == "Completed") & (pl.col("amount") > 4000.0))
    .select("order_id", "category", "amount")
)

df_filtered = lazy_scan.collect()

if __name__ == "__main__":
    print("Plan optimized:")
    print(lazy_scan.explain())
    print("Rows:", len(df_filtered))
    print(df_filtered.head())
