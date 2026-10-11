import polars as pl

salary_data = {
    "employee": ["Иван", "Мария", "Сергей", "Анна", "Петр", "Ольга"],
    "dept": ["IT", "IT", "IT", "HR", "HR", "Sales"],
    "salary": [120000.0, 180000.0, 90000.0, 80000.0, 100000.0, 95000.0]
}

df_salaries = pl.DataFrame(salary_data)

# =====================================================================
# РЕШЕНИЕ АВТОРА (Оконные функции через .over()):
# =====================================================================
df_salaries_result = df_salaries.with_columns(
    pl.col("salary").mean().over("dept").alias("dept_avg_salary")
).with_columns(
    (pl.col("salary") / pl.col("dept_avg_salary")).alias("salary_ratio_to_dept")
)

if __name__ == "__main__":
    print("--- Результат расчета зарплат с окном over() ---")
    print(df_salaries_result)
