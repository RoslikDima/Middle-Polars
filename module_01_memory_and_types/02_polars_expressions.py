import polars as pl

# Исходные данные
employees = {
    "employee_id": [10, 11, 12, 13, 14],
    "name": ["Анна", "Борис", "Виктор", "Дарья", "Елена"],
    "salary": [70000, 120000, 45000, 95000, 150000],
    "bonus_pct": [0.10, 0.15, 0.05, 0.20, 0.10]
}

df_emp = pl.DataFrame(employees)

# =====================================================================
# РЕШЕНИЕ АВТОРА (Polars filter + with_columns + alias):
# =====================================================================
df_salary = df_emp.filter(
    pl.col("salary") > 50000
).with_columns(
    (pl.col("salary") * pl.col("bonus_pct")).alias("total_bonus")
)

if __name__ == "__main__":
    print("--- Результат вычислений Polars ---")
    print(df_salary)
