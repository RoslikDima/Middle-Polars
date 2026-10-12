import polars as pl
import numpy as np

# 1. Заказы (Orders)
n_orders = 200_000
orders_data = {
    "order_id": np.arange(1, n_orders + 1),
    "user_id": np.random.randint(1, 10_000, size=n_orders),
    "amount": np.random.uniform(15.0, 1500.0, size=n_orders).round(2),
    "status": np.random.choice(["delivered", "returned", "cancelled"], p=[0.8, 0.1, 0.1], size=n_orders)
}
pl.DataFrame(orders_data).write_parquet("orders_stream.parquet")

# 2. Пользователи (Users)
users_data = {
    "user_id": np.arange(1, 10_001),
    "country": np.random.choice(["DE", "FR", "ES", "IT"], size=10_000),
    "tier": np.random.choice(["bronze", "silver", "gold"], p=[0.6, 0.3, 0.1], size=10_000),
    "meta_info": ["user_profile_heavy_string"] * 10_000
}
pl.DataFrame(users_data).write_parquet("users_dim.parquet")

# =====================================================================
# РЕШЕНИЕ АВТОРА (Оптимизированный Lazy Join):
# =====================================================================
orders_lf = pl.scan_parquet("orders_stream.parquet")
users_lf = pl.scan_parquet("users_dim.parquet")

lf_13 = (
    orders_lf.join(users_lf, on="user_id", how="inner")
    .filter((pl.col("status") == "delivered") & (pl.col("country") == "DE"))
    .select("order_id", "user_id", "amount", "tier")
)

df_germany_orders = lf_13.collect()

if __name__ == "__main__":
    print("--- План выполнения запроса с Pushdown сквозь Join ---")
    print(lf_13.explain())
    print("\n--- Результат ---")
    print(f"Размер: {df_germany_orders.shape}")
    print(df_germany_orders.head())
