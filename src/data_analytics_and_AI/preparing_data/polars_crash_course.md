---
icon: lucide/brush-cleaning
---

In this course we'll use [`polars`](https://pola.rs/), a famous dataframe library. It's **open source** (the entire underlying code is freely [available online](https://github.com/pola-rs/polars)) and **completely free**.

## Why not just use Excel?

Excel is a bit more accessible than writing code when it comes to manipulating data because everything is very **visual** and **interactive**. Thing is, this also comes with important limitations:

- 1M-row limit in Excel: insanely low
- It's not meant for automation, reproducibility, scalability, composability, or integration
- Commercial software:

      - you need a Microsoft licence
      - you don't own your work
      - [your data isn't private](https://www.youtube.com/watch?v=SlIZxdeoWDY "Video on Microsoft being a 'spyware'")

!!! note

      Those limitations are approximately the same for alternative products such as Google Sheets.

With programming tools (especially `polars`), working with 100 or 100M rows **doesn't make such a big difference**. `polars` will stay free forever, and you don't depend on any entity.

The #1 reason people use Excel is that it is (or rather, _seems_) simpler to use. But in the AI era, coding has become dramatically more accessible, **especially if you know what you're doing**, which is required no matter which tool you use.

Instead, the best investment you could make is to understand how `polars` works in general and work with AI to handle the rest. **You'll never have privacy, performance, automation, or scalability issues**.

## Install dataset

> **One row represents a completed transaction**. `transaction_id` is its unique ID. `gross_total` is the list-price total before discounts; `transaction_total` is after discounts and before refunds; `net_total` is after refunds. `discount_amount`, `refund_amount`, `returned_quantity`, `return_status`, and `return_date` describe discounts and returns. `sales_channel` identifies other sales, website sales, or campaign-attributed sales. `campaign_send_id` and `visit_id` connect attributed sales to their originating events.

<csv-table src="../data/sales.csv" caption="Sales transactions" page-size="6"></csv-table>

!!! info

      Put the `sales.csv` file in the same folder as the project you created earlier.

### Google colab

```py
sales = pl.read_csv("https://raw.githubusercontent.com/y-sunflower/classroom/refs/heads/main/src/data_analytics_and_AI/data/sales.csv")
```

First cell:

```sh
!pip install polars
```


## Read files

Reading a file is like opening an Excel spreadsheet.

### Example

```python exec="on" source="above" result="text"
import polars as pl

# We read the CSV file and create a "sales" dataframe
sales = pl.read_csv("src/data_analytics_and_AI/data/sales.csv")

# We print the "head" (first 5 rows) of the dataframe
print(sales.head())
```

### Exercise

- Create a `read.py` file
- In that file, write the code to read the `sales.csv` file and print the first 5 rows.

## Select data

Use `select` to choose the columns you need. Keeping a small set of relevant columns makes a table easier to inspect and share.

### Example

```python exec="on" source="above" result="text"
import polars as pl

# Read the sales dataset
sales = pl.read_csv("src/data_analytics_and_AI/data/sales.csv")

# Select 3 columns
overview = sales.select("transaction_id", "date", "net_total")

# Print the first 5 rows
print(overview.head())
```

### Exercise

Select the `product_name`, `quantity`, and `net_total` columns from `sales`. Store the result in a variable named `product_sales` and print its first five rows.

## Filter rows

Use `filter` to keep rows that match a condition. `pl.col("column")` refers to a column, and comparisons such as `==`, `>`, and `!=` create conditions. Combine conditions with `&` for “and” or `|` for “or”; put parentheses around each condition.

### Example

```python exec="on" source="above" result="text"
import polars as pl

# Read the dataset
sales = pl.read_csv("src/data_analytics_and_AI/data/sales.csv")

# Keep transactions with an amount greater than €100
high_value_sales = sales.filter(pl.col("net_total") > 100)

# Print the first few rows
print(high_value_sales.select("transaction_id", "product_name", "net_total").head())
```

### Exercise

Keep only sales where `sales_channel` is `"website"`. Store the result in `online_sales`, then print its first five rows.

## Group by

Use `group_by` to collect rows with the same value, then `agg` to calculate a summary for each group. Common aggregations include `.sum()`, `.mean()`, and `.len()`.

### Example

```python exec="on" source="above" result="text"
import polars as pl

# Read the sales dataset
sales = pl.read_csv("src/data_analytics_and_AI/data/sales.csv")

# Group by sales channel and compute total sales for each one
sales_agg = sales.group_by("sales_channel").agg(net_revenue=pl.col("net_total").sum())

# Print the result (no need for head() here since there are just 3 channels)
print(sales_agg)
```

### Exercise

Group the sales by `product_name` and calculate the total `quantity` sold for each product. Name the total column `units_sold`, then sort the result by `units_sold` from highest to lowest.

## Expressions

A Polars expression describes a calculation using one or more columns. Use `pl.col("column")` to refer to a column, then combine expressions with arithmetic or methods such as `.sum()`. Polars evaluates the expression inside an operation such as `with_columns`, `select`, or `agg`.

### Example

```python exec="on" source="above" result="text"
import polars as pl

sales = pl.read_csv("src/data_analytics_and_AI/data/sales.csv")
sales_with_discount = sales.with_columns(
      discount_per_unit=(pl.col("list_unit_price") - pl.col("unit_price"))
)
print(sales_with_discount.select("product_name", "discount_per_unit").head())
```

### Exercise

Create a new `line_total` column by multiplying `quantity` by `unit_price`. Store the result in `sales_with_line_total` and print the `product_name` and `line_total` columns for the first five rows.

## Chaining operations

Each Polars operation returns a DataFrame that the next operation can use. Chaining lets you filter rows, select columns, and then group and summarize the remaining data in one readable sequence.

### Example

```python exec="on" source="above" result="text"
import polars as pl

sales = pl.read_csv("src/data_analytics_and_AI/data/sales.csv")
online_revenue = (
      sales.group_by("sales_channel")      # For each sales channel
      .agg(pl.col("net_total").sum())      # Compute total of sales
      .sort("net_total", descending=True)  # And sort them by amount
)
print(online_revenue)
```

### Exercise

Chain operations to keep online sales, select the `product_name` and `quantity` columns, then group by product and calculate total units sold. Name the result `units_sold` and print the final table. Sort it in the ascending order.
