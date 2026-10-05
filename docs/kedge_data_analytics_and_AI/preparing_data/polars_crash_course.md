---
icon: lucide/brush-cleaning
---

In this course we'll use [`polars`](https://pola.rs/), a famous dataframe library. It's **open source** (the entire underlying code is freely [available online](https://github.com/pola-rs/polars)) and **completly free**.

## Why not just use Excel?

Excel is a bit more accessible than writing code when it comes to manipulating data because everything is very **visual** and **interactive**. Thing is, this also comes with important limitations:

- 1M rows limit in Excel: insanely low
- Not meant to be used for: automation, reproducibility, scalability, composability, and integration
- Commercial software:

      - you need a Microsoft License
      - you don't own your work
      - [your data isn't private](https://www.youtube.com/watch?v=SlIZxdeoWDY "Video on Microsoft being a 'spyware'")

!!! note

      Those limitations are approximately the same for alternative products such as Google Sheets.

With programming tools (especially `polars`), working with 100 or 100M rows **doesn't make such a big difference**.

The n°1 reason that people use Excel is that it is (or rather _seems_) simpler to use. But in the AI era, coding has become dramastically more accessible, **especially if you know what you're doing**, which is required no matter which tool you use.

Instead, the best investment you could make is understand how `polars` work in general, and work with AI to handle the rest. **You'll never have privacy, performance, automation or scalability issue**.

!!! warning

      The goal isn't to make you a programming expert! Instead, I want you to grasp the core concepts of manipulating data with coding, how to do basic operations, and then how to use AI to do it for you.

## Read files

Reading a file = Opening an Excel spreadsheet

=== "Example"

      ```python exec="on" source="above" result="text"
      import polars as pl

      # We read the CSV file and create a "sales" dataframe
      sales = pl.read_csv("docs/kedge_data_analytics_and_AI/data/sales.csv")

      # We print the "head" (first 5 rows) of the dataframe
      print(sales.head())
      ```

=== "Exercise"

      - (if you haven't already) Download the [datasets](../definition_of_data_and_ai/indigo.md) and put them inside the `indigo-data` folder.
      - create a `read.py` file
      - In that file, write the code to read the `sales.csv` file and print the first 5 rows.

=== "Hint"

      - When calling `pl.read_csv(...)`, the `...` needs to be replaced with the **path to the CSV file**.
      - If you get `FileNotFoundError: No such file or directory`, it's because the path is wrong.

## Select data

Use `select` to choose the columns you need. Keeping a small set of relevant columns makes a table easier to inspect and share.

=== "Example"

      ```python exec="on" source="above" result="text"
      import polars as pl

      # Read the sales dataset
      sales = pl.read_csv("docs/kedge_data_analytics_and_AI/data/sales.csv")

      # Select 3 columns
      overview = sales.select("transaction_id", "date", "net_total")

      # Print the first 5 rows
      print(overview.head())
      ```

=== "Exercise"

      Select the `product_name`, `quantity`, and `net_total` columns from `sales`. Store the result in a variable named `product_sales` and print its first five rows.

=== "Hint"

      - Pass each column name to `sales.select(...)`, then use `.head()` to show a few rows. Column names are **case-sensitive** and must match the CSV header.
      - When unsure about column names, you can either click on the CSV file in Positron, or run `print(sales.columns)`.

## Filter rows

Use `filter` to keep rows that match a condition. `pl.col("column")` refers to a column, and comparisons such as `==`, `>`, and `!=` create conditions. Combine conditions with `&` for “and” or `|` for “or”; put parentheses around each condition.

=== "Example"

      ```python exec="on" source="above" result="text"
      import polars as pl

      # Read the dataset
      sales = pl.read_csv("docs/kedge_data_analytics_and_AI/data/sales.csv")

      # Keep transaction with an amount of 100€
      high_value_sales = sales.filter(pl.col("net_total") > 100)

      # Print the first rows
      print(high_value_sales.select("transaction_id", "product_name", "net_total").head())
      ```

=== "Exercise"

      Keep only sales where `sales_channel` is `"online"`. Store the result in `online_sales`, then print its first five rows.

=== "Hint"

      Compare the column expression with the string value: `pl.col("sales_channel") == "online"`. Put that condition inside `sales.filter(...)`.

## Group By

Use `group_by` to collect rows with the same value, then `agg` to calculate a summary for each group. Common aggregations include `.sum()`, `.mean()`, and `.len()`.

=== "Example"

      ```python exec="on" source="above" result="text"
      import polars as pl

      sales = pl.read_csv("docs/kedge_data_analytics_and_AI/data/sales.csv")
      sales_by_channel = (
          sales.group_by("sales_channel")
          .agg(
              pl.len().alias("transactions"),
              pl.col("net_total").sum().round(2).alias("net_revenue"),
          )
          .sort("sales_channel")
      )
      print(sales_by_channel)
      ```

=== "Exercise"

      Group the sales by `product_name` and calculate the total `quantity` sold for each product. Name the total column `units_sold`, then sort the result by `units_sold` from highest to lowest.

=== "Hint"

      Start with `sales.group_by("product_name")`, then aggregate `pl.col("quantity").sum().alias("units_sold")`. Finish with `.sort("units_sold", descending=True)`.
