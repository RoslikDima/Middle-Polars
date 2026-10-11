import polars as pl

transactions = {
    "tx_id": [1, 2, 3, 4, 5, 6],
    "account_id": [501, 502, 501, 503, 502, 501],
    "amount": [150.0, 3200.0, 45.0, 910.0, 12000.0, 300.0],
    "status": ["FAILED", "SUCCESS", "SUCCESS", "SUCCESS", "FAILED", "SUCCESS"],
    "comment": ["err_code_1", "ok", "ok", "ok", "timeout", "ok"],
    "raw_payload": ["{...}", "{...}", "{...}", "{...}", "{...}", "{...}"]
}

df_tx = pl.DataFrame(transactions)

# =====================================================================
# РЕШЕНИЕ АВТОРА (Пайплайн и инспекция планов оптимизатора):
# =====================================================================
lf = (
    df_tx.lazy()
    .with_columns((pl.col("amount") * 0.02).alias("fee"))
    .filter(pl.col("status") == "SUCCESS")
    .select("tx_id", "amount", "fee")
)

df_res = lf.collect()

if __name__ == "__main__":
    print("--- Unoptimized Plan ---")
    print(lf.explain(optimized=False))
    print("\n--- Optimized Plan ---")
    print(lf.explain(optimized=True))
    print("\n--- Result ---")
    print(df_res)
