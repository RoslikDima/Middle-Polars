import polars as pl

customers_data = {
    "client_id": [201, 202, 203, 204, 205],
    "orders_count": [1, 15, 0, 7, 25],
    "total_spent": [800.0, 45000.0, 0.0, 12000.0, 110000.0]
}

df_cust = pl.DataFrame(customers_data)

# Решение автора:
df_cust = df_cust.with_columns(
    pl.when((pl.col("orders_count") >= 10) & (pl.col("total_spent") >= 30000))
    .then(pl.lit("VIP"))
    .when(pl.col("orders_count") > 0)
    .then(pl.lit("Standard"))
    .otherwise(pl.lit("New"))
    .alias("tier")
)

print(df_cust)
