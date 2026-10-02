---
icon: lucide/brush-cleaning
---

## What does "clean" means

Data cleaning makes a dataset more consistent and useful for a specific question. Poor quality can distort a campaign comparison, hide an operational issue, or lead a team to act on the wrong customers.

Cleaning is not about making every column look tidy. It is about documenting decisions so someone else can understand what changed and why.

## Check before changing

| Issue             | What to ask                                                        | Possible response                                                                              |
| ----------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Missing value     | Is it unknown, not collected, or not applicable?                   | Keep it, investigate it, exclude a row for a stated reason, or fill it using a justified rule. |
| Outlier           | Is the value impossible, a data-entry error, or a rare real event? | Verify it, flag it, correct it from a trusted source, or keep it and explain why.              |
| Redundant record  | Which field defines a duplicate for this analysis?                 | Compare the key and context, then remove only confirmed duplicate records.                     |
| Inconsistent name | Are spaces, case, abbreviations, or units mixed?                   | Use a stable naming convention and record the unit in the name or data dictionary.             |
| Inconsistent code | Do labels refer to the same category?                              | Map known variants to one documented code; preserve unknown values for review.                 |

!!! warning "Missing does not mean zero"

    In Indigo's campaign data, `time_spent` is blank for most messages because the recipient did not click. Replacing those blanks with zero could imply that time was measured and found to be zero. Preserve the distinction unless the analysis rule explicitly defines otherwise.

## Inspect a real campaign file

Use Polars to check the schema, the number of records, missing values, and whether the send ID is unique. The file includes expected missing values in later-stage fields such as `time_spent` and `transaction_id`.

```python exec="on" source="above" result="text"
import polars as pl

campaigns = pl.read_csv(
    "docs/kedge_data_analytics_and_AI/data/marketing_campaigns.csv",
    try_parse_dates=True,
)

print(f"Shape: {campaigns.shape}")
print(f"send_id unique: {campaigns['send_id'].n_unique() == campaigns.height}")
print("Missing values in selected columns:")
print(
    campaigns.select(
        pl.col("time_spent").null_count(),
        pl.col("visit_id").null_count(),
        pl.col("transaction_id").null_count(),
    )
)
```

The missing counts are not automatically errors. Compare them with the event flow: a recipient must click before time spent is recorded, and a purchase is less common than a message send.

## Practice on deliberately messy rows

This small example includes a repeated send, inconsistent channel labels, a meaningful blank, and a suspicious time value. We standardise the field names and channel labels, flag the suspicious value for review, and remove only the repeated `send_id`.

```python exec="on" source="above" result="text"
import polars as pl

raw = pl.DataFrame(
    {
        "Send ID": ["S001", "S002", "S002", "S003"],
        "Channel": ["Email", " e-mail ", "email", "SOCIAL"],
        "Time spent (seconds)": [120, None, None, 9999],
        "Clicked": [True, False, False, True],
    }
)

prepared = (
    raw.rename(
        {
            "Send ID": "send_id",
            "Channel": "channel",
            "Time spent (seconds)": "time_spent_seconds",
            "Clicked": "clicked",
        }
    )
    .with_columns(
        pl.col("channel")
        .str.strip_chars()
        .str.to_lowercase()
        .replace({"e-mail": "email"}),
        (pl.col("time_spent_seconds") > 3600).alias("time_needs_review"),
    )
    .unique(subset=["send_id"], keep="first", maintain_order=True)
)

print(prepared)
```

The example flags a value for review rather than deleting it. The duplicate rule uses `send_id` because that field identifies one send in this example. If records describe visits, use a visit key instead.

## Name and code variables consistently

Prefer clear names such as `sent_date`, `discount_rate`, and `time_spent_seconds`. Keep one case convention, avoid spaces and unexplained abbreviations, and include units where they affect interpretation.

For categorical variables, choose one spelling per category. A small codebook could define `email`, `ads`, and `social` as values for `channel`; it should also define whether a value such as `unknown` means missing, unavailable, or not applicable.

??? question "Should every outlier be removed?"

    No. A large order might be a real bulk purchase. First check units, source records, and business context; then decide whether to keep, correct, flag, or exclude it for the stated analysis.

## Continue

[Apply the checks in a practical lab](lab.md){ .md-button .md-button--primary }
