import pandas as pd
import polars as pl

data = {
    "user_id": [101, 102, None, 104],
    "status": ["active", "banned", "active", "active"],
    "city": ["Москва", "Самара", "Казань", "Москва"]
}

# 1. Pandas 2.0 с PyArrow и категориями
df_pd = pd.DataFrame(data).astype({
    "user_id": "int64[pyarrow]",
    "status": "category",
    "city": "string[pyarrow]"
})

# 2. Polars с нативной схемой Arrow
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
    print("
--- Polars schema ---")
    print(df_pl.schema)
