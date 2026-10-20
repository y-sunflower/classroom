from pathlib import Path

import joblib
import numpy as np
import polars as pl
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

SEED = 42
CAMPAIGN_SIZE = 500
CONTACT_COST = 1
RETENTION_MONTHS = 3
RETENTION_SUCCESS_RATE = 0.1

df = pl.read_csv("src/data_analytics_and_AI/data/food_subscription_churn.csv")
feature_columns = [column for column in df.columns if column != "churn"]

print(f"\nCustomers: {df.height}")
print(f"Churn rate: {df['churn'].mean():.2%}")

X = df.select(feature_columns).to_numpy()
y = df["churn"].to_numpy()
customer_indices = np.arange(df.height)

X_train, X_test, y_train, y_test, _train_indices, test_indices = train_test_split(
    X,
    y,
    customer_indices,
    test_size=0.30,
    stratify=y,
    random_state=SEED,
)

categorical_features = ["subscription_level", "food_preference"]
numeric_features = [
    "tenure_months",
    "monthly_price_eur",
    "delivery_issues_6m",
    "satisfaction_score",
    "boxes_skipped_6m",
    "discount_used",
]
categorical_columns = [feature_columns.index(column) for column in categorical_features]
numeric_columns = [feature_columns.index(column) for column in numeric_features]

preprocessor = ColumnTransformer(
    [
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            categorical_columns,
        ),
        ("numeric", StandardScaler(), numeric_columns),
    ]
)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=SEED),
    "Decision Tree": DecisionTreeClassifier(
        max_depth=5, min_samples_leaf=20, random_state=SEED
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200, min_samples_leaf=5, random_state=SEED, n_jobs=-1
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=150, learning_rate=0.05, max_depth=3, random_state=SEED
    ),
}

trained_models = {}
probabilities = {}
evaluation = []

for name, model in models.items():
    pipeline = Pipeline([("preprocessing", preprocessor), ("classifier", model)])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    trained_models[name] = pipeline
    probabilities[name] = y_proba

    evaluation.append(
        {
            "model": name,
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, y_proba),
        }
    )

evaluation_df = pl.DataFrame(evaluation).sort("roc_auc", descending=True)

print("\nMODEL PERFORMANCE")
print(evaluation_df)

print("\nROC-AUC BY MODEL")
print(evaluation_df.select("model", "roc_auc").with_columns(pl.col("roc_auc").round(3)))

# MARKETING CAMPAIGN SIMULATION
campaign_results = []
selected_customers = {}
test_customer_info = pl.DataFrame(
    {
        "customer_id": test_indices,
        "test_order": np.arange(len(test_indices)),
        "actual_churn": y_test,
    }
)
test_customers = (
    df.select(feature_columns)
    .with_row_index("customer_id")
    .with_columns(pl.col("customer_id").cast(pl.Int64))
    .join(test_customer_info, on="customer_id")
    .sort("test_order")
)

for name, y_proba in probabilities.items():
    customers = test_customers.with_columns(
        pl.Series("churn_probability", y_proba)
    ).with_columns(
        (
            pl.col("churn_probability")
            * RETENTION_SUCCESS_RATE
            * RETENTION_MONTHS
            * pl.col("monthly_price_eur")
            - CONTACT_COST
        ).alias("expected_value")
    )

    targeted = customers.sort("expected_value", descending=True).head(CAMPAIGN_SIZE)
    selected_customers[name] = set(targeted["customer_id"].to_list())
    actual_churners = int(targeted["actual_churn"].sum())
    campaign_cost = targeted.height * CONTACT_COST
    expected_saved_revenue = targeted.select(
        (
            pl.col("actual_churn")
            * pl.col("monthly_price_eur")
            * RETENTION_MONTHS
            * RETENTION_SUCCESS_RATE
        ).sum()
    ).item()

    expected_profit = expected_saved_revenue - campaign_cost
    predicted_profit = targeted["expected_value"].sum()

    campaign_results.append(
        {
            "model": name,
            "customers_targeted": targeted.height,
            "actual_churners_targeted": actual_churners,
            "precision_at_200": actual_churners / len(targeted),
            "campaign_cost": campaign_cost,
            "predicted_profit": predicted_profit,
            "expected_profit": expected_profit,
            "roi": expected_profit / campaign_cost,
        }
    )

campaign_df = pl.DataFrame(campaign_results).sort("expected_profit", descending=True)

print("\nCAMPAIGN RESULTS")
print(
    campaign_df.with_columns(
        pl.col("precision_at_200").round(3),
        pl.col("predicted_profit").round(2),
        pl.col("expected_profit").round(2),
        pl.col("roi").round(2),
    )
)


# COMPARE TARGETED CUSTOMERS

print("\nCUSTOMER TARGETING OVERLAP")
names = list(models.keys())
overlap = np.array(
    [[len(selected_customers[a] & selected_customers[b]) for b in names] for a in names]
)

overlap_table = {"model": names}
overlap_table.update({name: overlap[:, index] for index, name in enumerate(names)})
print(pl.DataFrame(overlap_table))


# BEST MODELS

best_auc = evaluation_df.row(0, named=True)
best_profit = campaign_df.row(0, named=True)
best_model_path = Path(__file__).with_name("best_churn_model.joblib")
joblib.dump(trained_models[best_auc["model"]], best_model_path)

print("\nFINAL RESULTS")
print(
    f"Best predictive model: {best_auc['model']} (ROC-AUC: {best_auc['roc_auc']:.3f})"
)

print(
    f"Most profitable model: {best_profit['model']} "
    f"(Expected profit: €{best_profit['expected_profit']:.2f})"
)
print(f"Saved predictive model to {best_model_path}")

print(
    f"\nNote: Profit estimates assume a {RETENTION_SUCCESS_RATE * 100}% retention success rate "
    f"and {RETENTION_MONTHS} months of saved revenue."
)
