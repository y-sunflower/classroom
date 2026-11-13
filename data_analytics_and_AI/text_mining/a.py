import polars as pl

sales = pl.read_csv("src/data_analytics_and_AI/data/sales.csv")

units_sold = (
    sales.filter(pl.col("sales_channel") == "website")
    .select("product_name", "quantity")
    .group_by("product_name")
    .agg(unit_sold=pl.col("quantity").sum())
    .sort("unit_sold")
    .head()
)

print(units_sold)
