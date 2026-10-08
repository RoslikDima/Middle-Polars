import pandas as pd
import polars as pl

# Исходные данные
data = {
    "user_id": [101, 102, None, 104],
    "status": ["active", "banned", "active", "active"],
    "city": ["Москва", "Самара", "Казань", "Москва"]
}

# =====================================================================
# РЕШЕНИЕ АВТОРА (Pandas 2.0):
# =====================================================================
df = pd.DataFrame(data)

df = df.astype({
    "user_id": "int64[pyarrow]",
    "status": "category",
    "city": "string[pyarrow]"
})

print("--- Авторское решение (Pandas 2.0 dtypes) ---")
print(df.dtypes)
print(df)

# =====================================================================
# ЭТАЛОННОЕ РЕШЕНИЕ НА POLARS:
# =====================================================================
df_pl = pl.DataFrame(
    data,
    schema={
        "user_id": pl.Int64,
        "status": pl.Categorical,
        "city": pl.String
    }
)

print("\n--- Аналог в Polars (Arrow Schema) ---")
print(df_pl.schema)
print(df_pl)
