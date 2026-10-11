import polars as pl

hub_data = {
    "shipment_id": ["SH-101", "SH-102", "SH-103", "SH-104", "SH-105", "SH-106"],
    "city": ["Москва", "СПб", "Москва", "Казань", "СПб", "Москва"],
    "weight_kg": [12.5, 45.0, 3.2, 80.0, 15.0, 0.8],
    "delivery_type": ["express", "standard", "express", "standard", "standard", "express"],
    "cost": [1200, 2500, 800, 4800, 1600, 450]
}

df_raw = pl.DataFrame(hub_data)

# =====================================================================
# РЕШЕНИЕ АВТОРА (LazyFrame Pipeline):
# =====================================================================
lazy_plan = (
    df_raw.lazy()
    .filter(pl.col("delivery_type") == "express")
    .with_columns((pl.col("cost") / pl.col("weight_kg")).alias("cost_per_kg"))
    .select("shipment_id", "city", "cost_per_kg")
)

df_express = lazy_plan.collect()

if __name__ == "__main__":
    print(f"Тип графа: {type(lazy_plan)}")
    print("--- Результат выполнения Lazy-пайплайна ---")
    print(df_express)
