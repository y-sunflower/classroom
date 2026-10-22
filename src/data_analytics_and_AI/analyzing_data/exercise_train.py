import joblib
import numpy as np
import polars as pl
import polars.selectors as cs
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

df = pl.read_csv("src/data_analytics_and_AI/data/food_subscription.csv")
feature_columns = [column for column in df.columns if column != "churn"]

X = df.select(feature_columns).to_numpy()
y = df["churn"].to_numpy()
customer_indices = np.arange(df.height)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, stratify=y)

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
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(max_depth=5, min_samples_leaf=20),
    "Random Forest": RandomForestClassifier(n_estimators=200, min_samples_leaf=5),
    "K Neighbors": KNeighborsClassifier(n_neighbors=5),
}

trained_models = {}
evaluation = []

for name, model in models.items():
    pipeline = Pipeline([("preprocessing", preprocessor), ("classifier", model)])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    trained_models[name] = pipeline

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
evaluation_display = evaluation_df.with_columns(
    cs.float().map_elements(lambda x: f"{x:.1%}", return_dtype=pl.String)
)

print("\nMODEL PERFORMANCE")
print(evaluation_display)

print("\nROC-AUC BY MODEL")
print(evaluation_display.select("model", "roc_auc"))

best_model_name = evaluation_df["model"][0]
best_model = trained_models[best_model_name]

joblib.dump(best_model, "exercise_model.joblib")

print(f"\nBest model: {best_model_name}")
print(f"ROC-AUC: {evaluation_df['roc_auc'][0]:.1%}")

thresholds = np.arange(0.1, 0.91, 0.01)

threshold_results = []

for threshold in thresholds:
    y_pred = (y_proba >= threshold).astype(int)

    threshold_results.append(
        {
            "threshold": threshold,
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
        }
    )

threshold_df = pl.DataFrame(threshold_results).sort("f1", descending=True)

print(threshold_df)

best_threshold = threshold_df["threshold"][0]
print(f"Best threshold: {best_threshold:.2f}")
