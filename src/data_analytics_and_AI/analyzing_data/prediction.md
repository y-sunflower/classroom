---
icon: lucide/brain-circuit
---

## Question to a model

In marketing, many questions look like this:

- which customers are the most likely to churn?
- which products should we suggest to customers?
- who should we target for our ad campaign?

In data / machine learning, those problems can be (partially?) solve using **prediction techniques**. A machine learning model looks for patterns in examples. We use:

- **Target**: which is the thing we want it to predict: probability of churn, expected spend, etc
- **Features**: anything that can help us predict our target: time since subscribed, age, buying behaviors, etc

!!! important

    In all of the examples below, all visualization are in 2d (or 3d), because otherwise we wouldn't be able to represent them. This means that we only have 1 or 2 features, but keep in mind that in the real world we often use much more features.

## Linear regression

Linear regression is the most simple machine learning model. It uses a line to estimate a **number**.

<iframe title="Linear regression playground" src="./playgrounds/linear-regression.html" width="100%" height="620" style="border: none"></iframe>

## Train-test split

When we create a model, we need to find a way to **evaluate** it. Let's say we have a model that predicts the ==spending of a customer next month==. We use that model every month to know how much money we expect to make.

> How can we know whether that value is accurate or not?

<iframe title="Train and test split animation" src="./playgrounds/train-test-split.html" width="100%" height="620" style="border: none"></iframe>

The blue examples are used to fit the line. Orange examples stay hidden from the fit until the final check. Mean absolute error (MAE) shows the average distance between a prediction and an example; lower is closer in this demo. If we keep tuning against the test set, it stops being a fair check.

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
