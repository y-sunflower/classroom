---
icon: lucide/brain-circuit
---

## Question to a model

In marketing, many questions look like this:

- which customers are the most likely to churn?
- which products should we suggest to customers?
- who should we target for our ad campaign?

In data / machine learning, those problems can be (partially?) solve using **prediction techniques**, especially with machine learning models. Those models look for patterns in examples, and for this we need:

- **Target**: which is the thing we want it to predict: probability of churn, expected spend, etc
- **Features**: anything that can help us predict our target: time since subscribed, age, buying behaviors, etc

!!! important

    In all of the examples below, all visualization are in 2d (or 3d), because otherwise we wouldn't be able to represent them. This means that we only have 1 or 2 features, but keep in mind that in the real world we often use much more features.

## Linear regression

Linear regression is the most simple machine learning model. It uses a line to estimate a **number**.

=== "Playground"

    <iframe title="Linear regression playground" src="./playgrounds/linear-regression.html" width="100%" height="620" style="border: none"></iframe>

=== "How it works"

    Each dot represents a customer's age and monthly spending. The model finds a straight line that stays close to the examples, then uses that line to estimate spending for a new customer.

    ``` mermaid
    graph LR
      examples[Past customers] --> line[Find the trend in a straight line]
      age[New customer's age] --> line
      line --> estimate[Estimated monthly spending]
    ```

## Train-test split

When we create a model, we need to find a way to **evaluate** it. Let's say we have a model that predicts the ==spending of a customer next month==. We use that model every month to know how much money we expect to make.

> How can we know whether that value is accurate or not?

For this, we often **split our dataset into 2 sets**: a train set and the test set.

<iframe title="Train and test split animation" src="./playgrounds/train-test-split.html" width="100%" height="620" style="border: none"></iframe>

## Logistic regression

Estimate the probability of one of two outcomes, such as a purchase or no purchase. The threshold controls when a probability becomes a positive prediction.

=== "Playground"

    <iframe title="Logistic regression playground" src="./playgrounds/logistic-regression.html" width="100%" height="620" style="border: none"></iframe>

=== "How it works"

    The model learns which customer traits tend to go with a purchase, then estimates a purchase probability for each new customer. A threshold turns that probability into a yes-or-no prediction. A lower threshold reaches more people, while a higher one focuses on the most likely buyers.

    ``` mermaid
    graph LR
      history[Past customer behavior and purchases] --> model[Learn purchase patterns]
      customer[New customer's behavior] --> model
      model --> probability[Estimated purchase probability]
      probability --> threshold{Above the campaign threshold?}
      threshold -->|Yes| target[Include in campaign]
      threshold -->|No| skip[Do not include]
    ```

## Decision trees

A tree asks a sequence of simple questions about the features. Greater depth can capture more detail, but can also fit noise in the examples.

=== "Playground"

    <iframe title="Decision tree playground" src="./playgrounds/decision-tree.html" width="100%" height="620" style="border: none"></iframe>

=== "How it works"

    A decision tree sorts customers by asking a series of feature-based questions. Each answer leads to another question or to a final prediction. A shallow tree is easier to explain; a very deep tree can memorize quirks in past customers.

    ``` mermaid
    graph TD
      start{Visited the product page?}
      start -->|Yes| email{Opened a recent email?}
      start -->|No| unlikely[Less likely to purchase]
      email -->|Yes| likely[More likely to purchase]
      email -->|No| unsure[Less likely to purchase]
    ```

## Random forests

A forest combines predictions from many decision trees trained on slightly different samples. Compare a small forest with a larger one and change how deep each tree can grow.

=== "Playground"

    <iframe title="Random forest playground" src="./playgrounds/random-forest.html" width="100%" height="620" style="border: none"></iframe>

=== "How it works"

    A random forest builds many decision trees, each using a slightly different sample of customers. The trees each make a prediction, and the forest combines their votes. This makes the result less dependent on the quirks of any one tree.

    ``` mermaid
    graph LR
      customers[Past customers] --> sample1[Sample of customers]
      customers --> sample2[Another sample]
      customers --> sample3[Another sample]
      sample1 --> tree1[Tree 1 vote]
      sample2 --> tree2[Tree 2 vote]
      sample3 --> tree3[Tree 3 vote]
      tree1 --> combine[Combine the votes]
      tree2 --> combine
      tree3 --> combine
      combine --> prediction[Forest prediction]
    ```

## K-nearest neighbors

K-nearest neighbors looks at the most similar examples nearby. Change the number of neighbors and click the chart to ask the model about a new point.

=== "Playground"

    <iframe title="K-nearest neighbors playground" src="./playgrounds/k-nearest-neighbors.html" width="100%" height="620" style="border: none"></iframe>

=== "How it works"

    For a new customer, the model finds the most similar customers in its examples and looks at what they did. If most of the nearest customers purchased, it predicts a purchase. The number of neighbors controls how many examples influence the vote.

    ``` mermaid
    graph LR
      new[New customer] --> find[Find the most similar customers]
      past[Past customers and their purchases] --> find
      find --> neighbors[For example: 3 purchased, 2 did not]
      neighbors --> vote[Purchase is the majority]
      vote --> prediction[Predict a purchase]
    ```
