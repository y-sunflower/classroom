---
icon: lucide/brush-cleaning
---

# Prepare a campaign analysis table

## The task

The Indigo team wants to compare campaign message variants. Prepare a dataset that connects campaign sends to attributed sales, checks data quality, and produces a summary that can be reused.

We will use `marketing_campaigns.csv` and `sales.csv`. The source files are synthetic course data. A send can have no sale, and some sales do not have a campaign send ID, so missing links are part of the data rather than an automatic reason to discard a row.

<csv-table src="../data/marketing_campaigns.csv" caption="Campaign sends" page-size="8"></csv-table>

## Load and inspect

`read_csv` loads each file into a Polars DataFrame. Inspect row counts, columns, nulls, and keys before joining or changing values.

```python exec="on" source="above" result="text"
import polars as pl

data_dir = "docs/kedge_data_analytics_and_AI/data"
campaigns = pl.read_csv(f"{data_dir}/marketing_campaigns.csv", try_parse_dates=True)
sales = pl.read_csv(f"{data_dir}/sales.csv", try_parse_dates=True)

print(f"Campaign sends: {campaigns.height:,} rows, {campaigns.width} columns")
print(f"Sales: {sales.height:,} rows, {sales.width} columns")
print(f"Unique send IDs: {campaigns['send_id'].n_unique():,}")
print(f"Rows with no campaign send ID in sales: {sales['campaign_send_id'].null_count():,}")
```

## Prepare the join

First, keep only sales linked to a campaign send and aggregate them by that send. Then join the summary to the campaign sends. This keeps one row per send and avoids repeating a send when it has multiple attributed sales.

```python exec="on" source="above" result="text"
import polars as pl

data_dir = "docs/kedge_data_analytics_and_AI/data"
campaigns = pl.read_csv(f"{data_dir}/marketing_campaigns.csv", try_parse_dates=True)
sales = pl.read_csv(f"{data_dir}/sales.csv", try_parse_dates=True)

sales_by_send = (
    sales.filter(pl.col("campaign_send_id").is_not_null())
    .group_by("campaign_send_id")
    .agg(
        pl.len().alias("attributed_transactions"),
        pl.col("net_total").sum().alias("attributed_net_revenue_eur"),
    )
)

prepared = (
    campaigns.select(
        "send_id",
        "campaign_name",
        "message_variant",
        "channel",
        "sent_date",
        "clicked",
        "purchased",
    )
    .join(sales_by_send, left_on="send_id", right_on="campaign_send_id", how="left")
    .with_columns(
        pl.col("attributed_transactions").fill_null(0),
        pl.col("attributed_net_revenue_eur").fill_null(0.0),
    )
)

print(f"Prepared rows: {prepared.height:,}")
print(f"One row per send: {prepared['send_id'].n_unique() == prepared.height}")
print(prepared.select("send_id", "message_variant", "clicked", "attributed_net_revenue_eur").head(5))
```

## Summarise the result

The code below groups the prepared data by campaign and message variant. In this course dataset, a send without a matched sale contributes zero campaign-attributed revenue; the source files remain unchanged. If a missing link could indicate a tracking failure in a real project, investigate it before treating it as zero. The rates use all sends as the denominator, so they answer “what share of sent messages resulted in a click or purchase?”

```python exec="on" source="above" result="text"
import polars as pl

data_dir = "docs/kedge_data_analytics_and_AI/data"
campaigns = pl.read_csv(f"{data_dir}/marketing_campaigns.csv", try_parse_dates=True)
sales = pl.read_csv(f"{data_dir}/sales.csv", try_parse_dates=True)

sales_by_send = (
    sales.filter(pl.col("campaign_send_id").is_not_null())
    .group_by("campaign_send_id")
    .agg(pl.col("net_total").sum().alias("attributed_net_revenue_eur"))
)
prepared = (
    campaigns.select("send_id", "campaign_name", "message_variant", "clicked", "purchased")
    .join(sales_by_send, left_on="send_id", right_on="campaign_send_id", how="left")
    .with_columns(pl.col("attributed_net_revenue_eur").fill_null(0.0))
)

summary = (
    prepared.group_by("campaign_name", "message_variant")
    .agg(
        pl.len().alias("sends"),
        pl.col("clicked").sum().alias("clicks"),
        pl.col("purchased").sum().alias("purchases"),
        pl.col("attributed_net_revenue_eur").sum().round(2).alias("net_revenue_eur"),
    )
    .with_columns(
        (pl.col("clicks") / pl.col("sends") * 100).round(1).alias("click_rate_pct"),
        (pl.col("purchases") / pl.col("sends") * 100).round(1).alias("purchase_rate_pct"),
    )
    .sort(["campaign_name", "message_variant"])
)

print(summary.head(8))
```

Rates describe what happened in this dataset. They do not by themselves prove that a message variant caused the difference; check that the experiment design assigned variants fairly before making a causal claim.

## Store the prepared data

Polars can write a prepared table to Parquet for analytical use, or CSV when a simple exchange format is more useful. This example writes to a temporary folder so a site build does not create an output file in the course repository. In class, replace the temporary path with an agreed project output location to keep your deliverable.

```python exec="on" source="above" result="text"
from pathlib import Path
from tempfile import TemporaryDirectory

import polars as pl

data_dir = "docs/kedge_data_analytics_and_AI/data"
campaigns = pl.read_csv(f"{data_dir}/marketing_campaigns.csv", try_parse_dates=True)
prepared = campaigns.select(
    "send_id",
    "campaign_name",
    "message_variant",
    "sent_date",
    "clicked",
    "purchased",
)

with TemporaryDirectory() as temp_dir:
    output_path = Path(temp_dir) / "prepared_campaigns.parquet"
    prepared.write_parquet(output_path)
    check = pl.read_parquet(output_path)
    print(f"Saved and reopened: {check.height:,} rows")
    print(f"File format: {output_path.suffix}")
```

## Your turn

Work in pairs. Use Polars to answer the questions below, then compare your choices with another pair.

- How many sends and purchases does each message variant have across all campaigns?
- Which columns contain missing values, and which missing values have a clear meaning?
- Does the joined table still have one row per send? How did you check?
- Would you share a CSV or a Parquet file with the next analyst? Explain the choice.
- What would you record in a short data dictionary for `clicked`, `purchased`, and `net_total`?

??? success "A check for your result"

    In `prepared`, `send_id` should remain unique after the join. A missing attributed amount can be filled with zero for a revenue sum only after the team confirms that an absent linked sale means no attributed revenue in this analysis. Keep the original source files unchanged and document the cleaning rules.

## Basic Polars operations

These operations appear in the lab. `select` chooses columns, `filter` keeps matching rows, `with_columns` creates or changes columns, `group_by` aggregates records, and `join` connects related tables.

```python exec="on" source="above" result="text"
import polars as pl

example = pl.DataFrame(
    {
        "channel": ["email", "ads", "email", "ads"],
        "clicked": [True, False, True, True],
        "revenue_eur": [24.0, 0.0, 15.0, 32.0],
    }
)

result = (
    example.filter(pl.col("clicked"))
    .select("channel", "revenue_eur")
    .group_by("channel")
    .agg(pl.col("revenue_eur").sum().alias("revenue_eur"))
    .sort("channel")
)

print(result)
```

## Key terms

| Term                    | Meaning                                                                                       |
| ----------------------- | --------------------------------------------------------------------------------------------- |
| Data warehouse          | Structured, prepared data organised for reliable reporting and analysis                       |
| Data lake               | A store for data in varied formats, often kept close to its original form                     |
| Relational database     | A system that stores structured records in connected tables                                   |
| Non-relational database | A system with another data model, such as documents, key-value pairs, graphs, or wide columns |
| Data cleaning           | Checking and preparing data for a defined use, with decisions recorded                        |
