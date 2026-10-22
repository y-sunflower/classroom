---
icon: lucide/brain-circuit
---

```py

```


## Evaluation metrics

=== "Accuracy"

    - Measures the proportion of all predictions that the model classifies correctly.
    - Particularly relevant when classes are **balanced** and all types of errors have **similar consequences**.

=== "Precision"

    - Measures the proportion of positive predictions that are actually correct.
    - Particularly relevant in **spam detection**, where incorrectly classifying legitimate emails as spam should be avoided.

=== "Recall"

    - Measures the proportion of actual positive cases that the model correctly identifies.
    - Particularly relevant in **disease screening**, where missing a positive case can have serious consequences.

=== "F1"

    - Measures the harmonic mean of precision and recall, providing a single score that balances both metrics.
    - Particularly relevant for **imbalanced datasets** where both false positives and false negatives matter.

=== "AUC"
    
    - Measures how well a model distinguishes between positive and negative classes across different classification thresholds.
    - Particularly relevant when comparing binary classifiers **independently of a specific decision threshold**, such as in credit risk prediction.