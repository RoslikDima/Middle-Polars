import pandas as pd

# Включаем строгий режим Copy-on-Write
pd.options.mode.copy_on_write = True

raw_data = {
    "project_id": [1, 2, 3, 4],
    "budget": [500000, 1200000, 300000, 850000],
    "status": ["planning", "active", "completed", "active"]
}

df_pandas = pd.DataFrame(raw_data)

# =====================================================================
# РЕШЕНИЕ АВТОРА (Проверка CoW):
# =====================================================================
# 1. Создаем срез
df_active = df_pandas[df_pandas["status"] == "active"]

# 2. Модифицируем бюджет в срезе
df_active["budget"] = df_active["budget"] * 1.1

if __name__ == "__main__":
    print("Original:")
    print(df_pandas)
    print("Modified slice:")
    print(df_active)
