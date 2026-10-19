---
icon: lucide/brain-circuit
---

## From a question to a model

A machine learning model looks for patterns in examples. We give it **features** (the information it can use) and, for supervised learning, a **target** (the thing we want it to predict).

## First, split the examples

A model learns from its **training data**. Keep a separate **test set** aside until fitting is done; it gives a first check on examples the model has not seen.

<iframe title="Train and test split animation" src="./playgrounds/train-test-split.html" width="100%" height="620" style="border: none"></iframe>

The blue examples are used to fit the line. Orange examples stay hidden from the fit until the final check. Mean absolute error (MAE) shows the average distance between a prediction and an example; lower is closer in this demo. If we keep tuning against the test set, it stops being a fair check.

| Goal | Example question | A useful starting point |
| --- | --- | --- |
| Predict a number | How much might this order cost? | Linear regression |
| Predict a category or probability | Is this visit likely to end in a purchase? | Logistic regression |
| Learn a short set of rules | Which visitors are likely to buy? | Decision tree |
| Combine many rule sets | Can several trees make a steadier prediction? | Random forest |
| Use similar examples | What might this customer like next? | K-nearest neighbors |

The best choice depends on the decision, the available data, and how much explanation the team needs. Try the same sample-size control in each playground and see how the fitted pattern changes.

After fitting a classification model, hover over a shaded square to inspect its probability for each class.

## Linear regression

Use a line to estimate a **number**. Try a small sample, add noise, and increase regularization to see the line become less sensitive to individual points.

<iframe title="Linear regression playground" src="./playgrounds/linear-regression.html" width="100%" height="620" style="border: none"></iframe>

## Logistic regression

Estimate the probability of one of two outcomes, such as a purchase or no purchase. The threshold controls when a probability becomes a positive prediction.

<iframe title="Logistic regression playground" src="./playgrounds/logistic-regression.html" width="100%" height="620" style="border: none"></iframe>

## Decision trees

A tree asks a sequence of simple questions about the features. Greater depth can capture more detail, but can also fit noise in the examples.

<iframe title="Decision tree playground" src="./playgrounds/decision-tree.html" width="100%" height="620" style="border: none"></iframe>

## Random forests

A forest combines predictions from many decision trees trained on slightly different samples. Compare a small forest with a larger one and change how deep each tree can grow.

<iframe title="Random forest playground" src="./playgrounds/random-forest.html" width="100%" height="620" style="border: none"></iframe>

## K-nearest neighbors

K-nearest neighbors looks at the most similar examples nearby. Change the number of neighbors and click the chart to ask the model about a new point.

<iframe title="K-nearest neighbors playground" src="./playgrounds/k-nearest-neighbors.html" width="100%" height="620" style="border: none"></iframe>

!!! note "A model is a tool for a decision"

    A pattern in the data does not explain why something happened. Before acting on a prediction, check what information was available, who may be missing from the data, and what the cost of a wrong prediction would be.
