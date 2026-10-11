import polars as pl

store_sales = {
    "store_id": ["SPB-1", "MSK-1", "SPB-1", "MSK-2", "MSK-1", "SPB-1", "MSK-2"],
    "category": ["Электроника", "Одежда", "Одежда", "Электроника", "Электроника", "Электроника", "Одежда"],
    "revenue": [150000.0, 24000.0, 18000.0, 85000.0, 310000.0, 95000.0, 42000.0],
    "is_returned": [False, False, True, False, False, False, False]
}

df_stores = pl.DataFrame(store_sales)

# =====================================================================
# РЕШЕНИЕ АВТОРА (group_by + agg с предикатом внутри pl.col):
# =====================================================================
df_grouped = df_stores.group_by("store_id").agg(
    pl.col("revenue").sum().alias("total_revenue"),
    pl.col("revenue").filter(pl.col("is_returned") == False).sum().alias("successful_revenue"),
    pl.len().alias("operations_count")
)

if __name__ == "__main__":
    print("--- Результат агрегации филиалов ---")
    print(df_grouped)
