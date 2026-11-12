import polars as pl

sales = pl.read_csv("src/data_analytics_and_AI/data/sales.csv")

sales_with_line_total = sales.with_columns(
    line_total=(pl.col("quantity") * pl.col("unit_price"))
)
print(sales_with_line_total.select("product_name", "line_total").head())
