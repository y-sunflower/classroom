---
icon: lucide/brain-circuit
---

## Churn data

Here we'll use a new CSV file about **food delivery subscription**:

<csv-table src="../data/food_subscription.csv" caption="Food subscriptions" page-size="6"></csv-table>

!!! info

    If you haven't already, install the required packages. See the [setup guide](../setup.md).

## Prepare the data

### Read the data

```py exec="on" source="above" result="text" session="food-analysis"
import polars as pl

df = pl.read_csv("src/data_analytics_and_AI/data/food_subscription.csv")
print(df)
```

### Calculate churn rate

```py exec="on" source="above" result="text" session="food-analysis"
print(f"Churn rate: {df['churn'].mean():.2%}\n")
```

### Separate features and target

- **target** (aka `y`) = whether the customer churned or not

```py exec="on" source="above" result="text" session="food-analysis"
# The "churn" columns contain the info we want
y = df["churn"].to_numpy()
print(f"Target (y): {y}\n")
```

- **features** (aka `X`) = everything that can help us predict the target (time since subscribed, the kind of subcription, etc)

```py exec="on" source="above" result="text" session="food-analysis"
# Column names of features are everything, except "churn"
feature_columns = df.drop("churn").columns
X = df.select(feature_columns).to_numpy()
print(f"Features (X): {X}\n")
```

### Exercise

Calculate the churn rate for each subscription level. Sort the result from the highest churn rate to the lowest, then write one sentence describing what you observe. Does this comparison show that the subscription level causes churn?

```py
churn_by_plan = (
    df.group_by("subscription_level")
    .agg(churn_rate=pl.col("churn").mean())
    # TODO: sort by churn_rate from highest to lowest
)

print(churn_by_plan)
```
