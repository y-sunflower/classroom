import polars as pl

# Read the sales dataset
sales = pl.read_csv("src/data_analytics_and_AI/data/sales.csv")

# Select 3 columns
overview = sales.select("product_name", "quantity", "net_total")

# Print the first 5 rows
print(overview.head())
