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

> R² (R squared): proportion of the variation in the **target** that is predictable from the **features**. Higher is better.

### Exercise

Use the linear regression playground to add noise to the examples. Compare the fitted line and R² before and after adding noise. In which version would you trust the spending predictions more, and why?

??? question "Answer"

    <span class="answer"><strong>Answer: trust the predictions with less noise more.</strong> With less noise, the points stay closer to the fitted line and R² is usually higher. Adding noise spreads the points around the trend and usually lowers R², even if the fitted line keeps a similar slope. Individual spending predictions become less precise.</span>

## Train-test split

When we create a model, we need to find a way to **evaluate** it. Let's say we have a model that predicts the ==spending of a customer next month==. We use that model every month to know how much money we expect to make.

> How can we know whether that value is accurate or not?

For this, we often **split our dataset into 2 sets**: a train set and the test set.

<iframe title="Train and test split animation" src="./playgrounds/train-test-split.html" width="100%" height="620" style="border: none"></iframe>

## Logistic regression

Estimate the probability of one of two outcomes, such as a <span class="blue">purchase</span> or <span class="orange">no purchase</span>. The threshold controls when a probability becomes a positive prediction.

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

### Exercise

Use the logistic regression playground to compare thresholds of 0.3, 0.5, and 0.7. For each threshold, note how many customers are selected and how many of them actually purchased. Which threshold would you choose if contacting a customer is expensive? Explain your choice.

??? question "Answer"

    <span class="answer"><strong>Answer: a threshold of 0.7 is a reasonable starting point when contact is expensive.</strong> Raising the threshold selects fewer customers, keeping only those with higher predicted purchase probabilities. The aim is to spend less on contacting people who will not purchase, although we also miss some buyers.</span>

## Decision trees

A tree asks a sequence of simple questions about the features. Greater depth can capture more detail, but can also fit noise in the examples.

=== "Playground"

    <iframe title="Decision tree playground" src="./playgrounds/decision-tree.html" width="100%" height="620" style="border: none"></iframe>

=== "How it works"

    At each decision point, or **node** :material-information-outline:{ title="A point where the tree asks a question and splits the examples." }, the tree tries possible cutoffs on its features (such as fewer or more product visits). It chooses a cutoff that leaves the resulting groups with less mixing between purchasers and non-purchasers, and then repeats the process inside each group.

    A group where the tree stops asking questions is a **leaf** :material-information-outline:{ title="The final group at the end of a branch, where the tree makes a prediction." }. It predicts the purchase probability from the share of training customers in that group who purchased.

    The **maximum depth** :material-information-outline:{ title="The most questions allowed between the top of the tree and a prediction." } sets how many questions can appear along a path from the top of the tree to a leaf. The **minimum examples per group** :material-information-outline:{ title="The smallest number of training examples allowed on either side of a split." } sets how many training customers each side of a split must contain. A group stops splitting when it reaches the depth limit, contains only one outcome, or cannot be divided while keeping the minimum examples on both sides.

    ``` mermaid
    graph TD
      start{Visited the product page?}
      start -->|Yes| email{Opened a recent email?}
      start -->|No| unlikely[Less likely to purchase]
      email -->|Yes| likely[More likely to purchase]
      email -->|No| unsure[Less likely to purchase]
      classDef leaf fill:#e4f3e8,stroke:#3a7d44,color:#1f3d23,stroke-width:2px
      class unlikely,likely,unsure leaf
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

    **K** :material-information-outline:{ title="The number of nearest examples used to make one prediction." } is the number of nearby examples used to make a prediction. When you click the chart, the model measures the straight-line distance from that point to the plotted examples and selects the K closest. It estimates the purchase likelihood from the share of those neighbors who purchased. For example, with K = 7, if 5 of the neighbors purchased, the estimate is 5 out of 7, or about 71%.

    A small K makes the prediction depend on a very local group, so one unusual example can change it. A larger K includes a wider neighborhood and tends to make predictions smoother, though examples farther away can influence the result. The playground lets you compare odd values from 1 to 31; odd values avoid a tied vote between two outcomes.

    ``` mermaid
    graph LR
      new[New customer] --> find[Find K closest examples]
      past[Past customers and their purchases] --> find
      find --> neighbors[Example: K = 7; 5 purchased, 2 did not]
      neighbors --> vote[Purchase likelihood: 5 out of 7]
      vote --> prediction[About 71%]
    ```

### Exercise

Use the K-nearest neighbors playground to predict the same point with K = 1, K = 7, and K = 15. Record the predicted purchase likelihood each time. Which result changes the most when you move the point slightly, and what does that tell you about the choice of K?

??? question "Answer"

    <span class="answer"><strong>Answer: K = 1 is usually the most sensitive to a small move.</strong> Its purchase likelihood is either 0% or 100%, depending on the single closest example, so moving across a boundary can flip the prediction completely. With K = 7 or K = 15, the likelihood is the share of purchasers among those neighbors; replacing one neighbor has a smaller effect. Your exact values depend on the point you choose. Larger K usually makes predictions smoother, but can blur useful local patterns, so compare values on new data before choosing.</span>

## Underfitting and overfitting

A model should learn patterns that also work for **new examples**. This ability is called ==generalization==. Fitting the training data very closely does not guarantee good predictions for new customers.

<iframe title="Visual comparison of underfitting, a good fit, and overfitting" src="./fitting-comparison.html" width="100%" height="470" style="border: none"></iframe>

=== "Underfitting"

    **The model misses the pattern.** A straight line cannot capture every curved relationship. A tree that can ask only one question may miss useful combinations of customer behaviors.

    - **Typical signal:** errors are high on both training and unseen data, compared with a useful baseline or the task's requirements.
    - **Why it happens:** the model is too restricted, useful features are missing, or training has stopped too early.
    - **What to try:** add useful features, allow more model complexity, or train longer if learning has not finished. More rows alone may not fix a model that cannot represent the pattern.

=== "Good fit (normal)"

    **The model captures the pattern without chasing every dot.** Some variation is noise: random differences that the available features cannot explain. A useful model can leave training errors and still make good predictions.

    - **Typical signal:** errors are low enough for the task on both training and unseen data, with a reasonably small gap.
    - **What matters:** the model improves on a relevant baseline and works on examples that represent future use.
    - **Keep in mind:** similar training and unseen errors are not enough by themselves. Both could be equally bad!

=== "Overfitting"

    **The model learns details that do not generalize.** It follows chance fluctuations or unusual training examples as though they were reliable patterns. A very deep tree or K-nearest neighbors with K = 1 can do this.

    - **Typical signal:** very low training error, but substantially higher error on unseen data. This difference is the **generalization gap**.
    - **What to try:** simplify the model, limit tree depth, increase K, or add regularization (a penalty that discourages overly complex fits). More representative training examples can also help.
    - **Keep in mind:** complexity alone does not prove overfitting. Check how the model performs on unseen examples.

!!! tip "Compare fairly, then keep a final test"

    Compare the **same metric** on training and unseen data. For errors such as **MAE** (mean absolute error), lower is better; for scores such as accuracy or R², higher is better. There is no universal gap that proves overfitting: consider the baseline, sample size, noise, and task.

    Use a **validation set** to compare model settings. Keep a separate **test set** for the final evaluation, after choosing the model. Repeatedly adjusting a model based on its test score can make that score too optimistic. These comparisons assume no data leakage and that the evaluation examples represent the people or situations where the model will be used.

## Exercises

For each of the five cases below, decide whether the evidence suggests **underfitting**, **overfitting**, or a **good fit (normal)**. Identify the clue that supports your answer before selecting it. All data are illustrative; validation examples were kept out of training.

<iframe title="Five exercises to diagnose underfitting, overfitting, and a good fit" src="./fit-diagnosis.html" width="100%" height="850" style="border: none"></iframe>
