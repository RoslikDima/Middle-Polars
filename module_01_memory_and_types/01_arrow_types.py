import pandas as pd
import polars as pl

data = {
    "user_id": [101, 102, None, 104],
    "status": ["active", "banned", "active", "active"],
    "city": ["Москва", "Самара", "Казань", "Москва"]
}

# Решение автора:
df = pd.DataFrame(data)
df = df.astype({
    "user_id": "int64[pyarrow]",
    "status": "category",
    "city": "string[pyarrow]"
})

print(df.dtypes)
