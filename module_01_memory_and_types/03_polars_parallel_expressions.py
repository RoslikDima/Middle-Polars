import polars as pl

orders_data = {
    "order_id": [1001, 1002, 1003, 1004, 1005],
    "item_price": [1200.0, 450.0, 8900.0, 3100.0, 150.0],
    "shipping_cost": [250.0, 0.0, 500.0, 300.0, 150.0],
    "discount_rub": [100.0, 50.0, 1000.0, 0.0, 0.0]
}

df_orders = pl.DataFrame(orders_data)

# =====================================================================
# РЕШЕНИЕ АВТОРА (Параллельные вычисления в with_columns):
# =====================================================================
df_result = df_orders.with_columns(
    (pl.col("item_price") + pl.col("shipping_cost") - pl.col("discount_rub")).alias("final_price"),
    (pl.col("shipping_cost") == 0).alias("is_free_shipping"),
    (pl.col("discount_rub") / pl.col("item_price")).alias("discount_share")
)

if __name__ == "__main__":
    print("--- Результат расчета заказа ---")
    print(df_result)
