import pandas as pd
import polars as pl

# 1. Исходные "сырые" данные
data = {
    "user_id": [101, 102, None, 104],
    "status": ["active", "banned", "active", "active"],
    "city": ["Москва", "Самара", "Казань", "Москва"]
}

# 2. Pandas 2.0 (PyArrow backend + категориальный тип)
df_pd = pd.DataFrame(data).astype({
    "user_id": "int64[pyarrow]",
    "status": "category",
    "city": "string[pyarrow]"
})

# 3. Polars (Apache Arrow нативная схема)
df_pl = pl.DataFrame(
    data,
    schema={
        "user_id": pl.Int64,
        "status": pl.Categorical,
        "city": pl.String
    }
)

if __name__ == "__main__":
    print("--- Pandas 2.0 dtypes ---")
    print(df_pd.dtypes)
    print("\n--- Polars schema ---")
    print(df_pl.schema)
