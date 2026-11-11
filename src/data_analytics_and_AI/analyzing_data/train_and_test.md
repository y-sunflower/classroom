---
icon: lucide/brain-circuit
---

## Data

```python exec="on" source="above" session="train-models"
import polars as pl

df = pl.read_csv("src/data_analytics_and_AI/data/food_subscription.csv")
y = df["churn"].to_numpy()
feature_columns = df.drop("churn").columns
X = df.select(feature_columns).to_numpy()
```

## Simple model

We'll use a very famous library called [`scikit-learn`](https://scikit-learn.org/stable/). It's the world reference when it comes to machine learning.

### Let's create our first machine learning model

- Import a whole bunch of things

```python exec="on" source="above" session="train-models"
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
```

- Split train and test sets

```python exec="on" source="above" session="train-models"
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
```

!!! question

    If we have a dataset with 100 rows and 10 columns (9 features and 1 target) and we use `test_size=0.25`, what are the dimensions (number of rows and columns) of:
    
    - `X_train`
    - `X_test`
    - `y_train`
    - `y_test`

- Create a `ColumnTransformer`

```python exec="on" source="above" session="train-models"
categorical_features = ["subscription_level", "food_preference"]
categorical_columns = [
    i for i, col in enumerate(feature_columns) if col in categorical_features
]
numeric_columns = [
    i for i, col in enumerate(feature_columns) if col not in categorical_features
]

preprocessor = ColumnTransformer(
    [
        ("categorical", OneHotEncoder(), categorical_columns),
        ("numeric", StandardScaler(), numeric_columns),
    ]
)
```

=== "`StandardScaler`"

    <iframe title="StandardScaler animation" src="./standard-scaler.html" width="100%" height="340" style="border: none"></iframe>

=== "`OneHotEncoder`"

    <iframe title="One-hot encoding animation" src="./one-hot-encoding.html" width="100%" height="300" style="border: none"></iframe>

- Train (logistic regression)

```python exec="on" source="above" session="train-models"
from sklearn.pipeline import Pipeline

model = Pipeline([("preprocessor", preprocessor), ("classifier", LogisticRegression())])
model.fit(X_train, y_train)
```

!!! success

    Congrats, you've now created your first machine learning model!

    But is it good though?

## Evaluation metrics

=== "Accuracy"

    $$
    \text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
    $$

    - Measures the proportion of all predictions that the model classifies correctly.
    - Particularly relevant when classes are **balanced** and all types of errors have **similar consequences**.

=== "Precision"

    $$
    \text{Precision} = \frac{TP}{TP + FP}
    $$

    - Measures the proportion of positive predictions that are actually correct.
    - Particularly relevant in **spam detection**, where incorrectly classifying legitimate emails as spam should be avoided.

=== "Recall"

    $$
    \text{Recall} = \frac{TP}{TP + FN}
    $$

    - Measures the proportion of actual positive cases that the model correctly identifies.
    - Particularly relevant in **disease screening**, where missing a positive case can have serious consequences.

=== "F1"

    $$
    F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}
    $$

    - Measures the harmonic mean of precision and recall, providing a single score that balances both metrics.
    - Particularly relevant for **imbalanced datasets** where both false positives and false negatives matter.

=== "AUC"

    $$
    \text{AUC} = \int_0^1 \text{TPR}(\text{FPR}) \, d(\text{FPR})
    $$

    - Measures how well a model distinguishes between positive and negative classes across different classification thresholds.
    - Particularly relevant when comparing binary classifiers **independently of a specific decision threshold**, such as in credit risk prediction.

<script src="../../javascripts/mathjax.js"></script>

### Let's make predictions

```python exec="on" source="above" session="train-models"
y_pred = model.predict(X_test)
print(y_pred, "\n")

y_proba = model.predict_proba(X_test)[:, 1]
print(y_proba)
```

### Evaluate our predictions against the test set

```python exec="on" source="above" session="train-models"
accuracy = accuracy_score(y_test, y_pred) * 100
print(f"Accuracy: {accuracy:.1f}%\n")

precision = precision_score(y_test, y_pred) * 100
print(f"Precision: {precision:.1f}%\n")

recall = recall_score(y_test, y_pred) * 100
print(f"Recall: {recall:.1f}%\n")

F1 = f1_score(y_test, y_pred) * 100
print(f"F1: {F1:.1f}%\n")

auc = roc_auc_score(y_test, y_proba) * 100
print(f"AUC: {auc:.1f}%\n")
```

???+ question "Assuming **retention campaigns** are cheap, which metrics are we the most interested in?"

    <span class="answer">We can use the recall and the auc metrics here, while others have medium to low value.</span>

### Exercise

The default prediction uses a probability threshold of 0.5. Try thresholds of 0.3 and 0.7 using the predicted probabilities. For each threshold, calculate precision and recall, then explain which threshold better fits a retention team that can contact only a small number of customers.

```py
from sklearn.metrics import precision_score, recall_score

for threshold in [0.3, 0.5, 0.7]:
    # TODO: turn y_proba into yes/no predictions using this threshold
    y_threshold = ...

    print(
        threshold,
        precision_score(y_test, y_threshold, zero_division=0),
        recall_score(y_test, y_threshold, zero_division=0),
    )
```

## Compare models

```python exec="on" source="above" result="text" session="train-models"
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

models = {
    "Logistic regression": LogisticRegression(max_iter=1000),
    "Decision tree": DecisionTreeClassifier(
        max_depth=5, min_samples_leaf=20, random_state=42
    ),
    "Random forest": RandomForestClassifier(
        n_estimators=200, min_samples_leaf=5, random_state=42
    ),
    "K-nearest neighbors": KNeighborsClassifier(n_neighbors=5),
}

model_scores = []

for name, classifier in models.items():
    candidate = Pipeline(
        [("preprocessor", preprocessor), ("classifier", classifier)]
    )
    candidate.fit(X_train, y_train)
    y_pred = candidate.predict(X_test)
    y_proba = candidate.predict_proba(X_test)[:, 1]

    model_scores.append(
        {
            "model": name,
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
            "auc": roc_auc_score(y_test, y_proba),
        }
    )

for scores in sorted(model_scores, key=lambda scores: scores["auc"], reverse=True):
    print(
        f"{scores['model']:<21} "
        f"accuracy {scores['accuracy']:.1%} | "
        f"precision {scores['precision']:.1%} | "
        f"recall {scores['recall']:.1%} | "
        f"F1 {scores['f1']:.1%} | "
        f"AUC {scores['auc']:.1%}"
    )
```

### Exercise

Change the decision tree's `max_depth` to 2 and then to 10. Compare its test-set recall and AUC with the original tree. Which setting would you recommend, and what might happen if the tree is too deep?

## Save the best model

!!! note "joblib"

    `joblib` is a Python library that (among others) that let use **save** a model to disk in order to **reuse it later**.

```python exec="on" source="above" session="train-models"
import joblib

joblib.dump(model, "src/data_analytics_and_AI/analyzing_data/exercise_model.joblib")
```
