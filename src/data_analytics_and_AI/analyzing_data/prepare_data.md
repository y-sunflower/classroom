---
icon: lucide/brain-circuit
---

## Goal

We want to make it easy to know **what are the chances of a customer to churn**. For this, we need to:

- find the relevant data and clean it
- train and evaluate multiple machine learning models
- make it easy to use the best model _in production_
- measure if it's financially viable to contact customers

## Churn data

Here we'll use a new CSV file about **food delivery subscription**:

<csv-table src="../data/food_subscription.csv" caption="Food subscriptions" page-size="6"></csv-table>

!!! info

    If you haven't already, install the required packages. See the [setup guide](../setup.md).

## Prepare the data

### Read the data

```python exec="on" source="above" result="text" session="food-analysis"
import polars as pl

df = pl.read_csv("src/data_analytics_and_AI/data/food_subscription.csv")
print(df)
```

### Calculate churn rate

```python exec="on" source="above" result="text" session="food-analysis"
churn_rate = df["churn"].mean()
churn_rate = df["churn"].sum() / df.height

print(f"Churn rate: {churn_rate:.2%}\n")
```

### Separate features and target

- **target** (aka `y`) = whether the customer churned or not (1 = true, 0 = false)

```python exec="on" source="above" result="text" session="food-analysis"
# The "churn" columns contain the info we want
y = df["churn"].to_numpy()
print(f"Target (y): {y}\n")
```

- **features** (aka `X`) = everything that can help us predict the target (time since subscribed, the kind of subcription, number of issues reported, etc)

```python exec="on" source="above" result="text" session="food-analysis"
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
    # TODO: compute the mean of "churn"
    # TODO: sort by churn_rate from highest to lowest
)

print(churn_by_plan)
```

!!! tip

    Look at the [polars crash course](../preparing_data/polars_crash_course.md#group-by)!
