---
icon: lucide/flask-conical
---

## Turn Indigo data into two use cases

Work in pairs. Choose **two decisions** Indigo could improve with the course datasets. For each one, identify the goal, the data that would be available at prediction time, and an action the team could take.

Two good starting points are available in the current data:

| Use case | Dataset and target | Possible action |
| --- | --- | --- |
| Estimate which website visits may lead to a purchase | `website_analytics.csv`; predict `purchased` | Offer checkout help before a visitor completes a purchase |
| Recommend another product to a returning customer | `sales.csv`; use past customer-product purchases | Suggest a product that similar customers bought |

The website file has about 11,000 visits and about 1,000 purchases, enough for a classroom classification exercise. The sales file has nearly 1,000 customers and 30 products, enough for a small recommendation prototype.

!!! warning "Keep the prediction honest"

    Do not give a model information that would only be known after the outcome. For website purchase prediction, leave out `transaction_id`. This starter uses stock availability and cart activity, both known before checkout completes. Traffic source and promotion are possible extensions; use visit duration only if it is measured at the moment the team plans to act. A purchase record is a clue about interest, not proof of preference.

## Install scikit-learn

Open the terminal in your `indigo-data` project and add the package:

```sh
uv add scikit-learn
```

If you do not have the course CSV files in your project yet, download them from the [Indigo data page](../definition_of_data_and_ai/indigo.md) and place them in a `data` folder.

## Start with purchase prediction

This small baseline uses logistic regression to predict whether a website visit led to a purchase. It compares the model with a simple baseline that always predicts “no purchase”.

```python
import polars as pl
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

visits = pl.read_csv("data/website_analytics.csv")

features = (
    visits.select("product_available", "added_to_cart")
    .with_columns(
        pl.col("product_available").cast(pl.Int8),
        pl.col("added_to_cart").cast(pl.Int8),
    )
    .to_numpy()
)
target = visits.get_column("purchased").cast(pl.Int8).to_numpy()

x_train, x_test, y_train, y_test = train_test_split(
    features, target, test_size=0.25, random_state=42, stratify=target
)

baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(x_train, y_train)
print("Always no purchase")
print(classification_report(y_test, baseline.predict(x_test), zero_division=0))

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(class_weight="balanced", max_iter=1000),
)
model.fit(x_train, y_train)
print("Logistic regression")
print(classification_report(y_test, model.predict(x_test), zero_division=0))
```

`purchased` is unevenly distributed, so accuracy alone can hide missed purchases. Compare **precision** (how often a purchase prediction is right) and **recall** (how many actual purchases the model finds). Decide which matters more for the action Indigo would take.

## Build a product recommender

Use `sales.csv` to make a customer-by-product table: each row is a customer, each column is a product, and a cell records whether that customer bought it. Then use `sklearn.neighbors.NearestNeighbors` with cosine distance to find customers with similar purchase histories.

Your recommendation must omit products the customer already bought. Test it by holding out each customer's most recent new product, making recommendations from earlier purchases, and checking how often the held-out product appears near the top. Compare against recommending the most popular products to everyone.

??? question "What should the team deliver?"

    For each use case, show the business question, target or recommendation, input columns, one model, one baseline, and one evaluation result. End with one sentence describing the action Indigo could take and one limitation of the data.

!!! note "About the product data"

    This dataset is simulated and has no product impressions or customer demographics. It can support a classroom recommendation prototype for the existing 30 products. It cannot show whether a real customer saw an item, explain why they liked it, or reliably recommend Indigo's new refillable shampoo before that product has purchase history.
