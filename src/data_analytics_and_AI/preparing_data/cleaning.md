---
icon: lucide/brush-cleaning
---

## What does "clean" mean?

Data cleaning makes a dataset more consistent and useful for a specific question. Poor quality can distort a campaign comparison, hide an operational issue, or lead a team to act on the wrong customers. In practice, we want to make the [data "tidy"](https://vita.had.co.nz/papers/tidy-data.pdf).

In the previous lesson, we saw common ways to clean data (selecting columns, filtering rows, and aggregating). Here we'll talk about common issues that arise when cleaning data, why they occur, and how to "fix" them (if they need fixing).

## Missing values

### Definitions

=== "completely at random"

      Data is missing for purely random reasons. This is the ideal case, since ignoring those values has no impact on our analysis, but it is almost never the case in the real world.

      A bank with customer info might be missing information about its customers' jobs. It's likely that people who don't want to share their job have reasons: a bad credit score, illegal activities, ...

=== "at random"

      Missingness isn't random and can be explained by other variables.

      Men are less likely to receive a diagnosis of depression, but this has nothing to do with their level of depression. Statistics allow us to easily account for sex.

=== "not at random"

      Data is not missing at random when the value of the missing variable is related to the reason it's missing. People with severe symptoms of depression are more likely not to answer questions **because** of their symptoms.

=== "by design"

      When sending marketing emails, a blank value for time spent on the website isn't really missing data if a user didn't click the link to the website. Want to know how much time users spend on your website on average after clicking through from your email campaign? Start by filtering for users who clicked through, and you'll "remove" missing values.

### Exercise

For each scenario, decide whether the data is **completely at random**, **at random**, **not at random**, or missing **by design**. Open each card to check your answer.

??? question "A sensor loses readings during randomly timed transmission glitches"

    The glitches affect readings across devices and times, with no connection to the recorded conditions or the readings themselves. What kind of missing data is this?

    <span class="answer"><strong>Answer: completely at random.</strong> The missingness has no relationship to observed variables or to the missing readings.</span>

??? question "A customer survey does not ask for household income"

    Customers with higher incomes are more likely to skip the income question. What kind of missing data is this?

    <span class="answer"><strong>Answer: not at random.</strong> Whether income is missing is related to the income value itself.</span>

??? question "A satisfaction score is missing more often in one app version"

    A bug in the survey form affects the oldest app version. The app version is recorded for every customer. What kind of missing data is this?

    <span class="answer"><strong>Answer: at random.</strong> Missingness is related to an observed variable, the app version, rather than to the satisfaction score itself.</span>

??? question "A delivery time is blank for orders that were never shipped"

    The dataset records a delivery time only after an order has shipped. What kind of missing data is this?

    <span class="answer"><strong>Answer: by design.</strong> A delivery time does not exist for an order that was never shipped, so the blank is not an unrecorded value.</span>

??? question "A health question is skipped more often by older respondents"

    Age is recorded for everyone, and older respondents are more likely to leave the question blank. What kind of missing data is this?

    <span class="answer"><strong>Answer: at random.</strong> The missingness can be explained by the observed age variable.</span>

## Outliers

In France, before income tax (after social security contributions)

- Average salary is ~2700€/month
- Median salary is ~2200€/month

### Exercise

In this exercise, you'll investigate six outlier cases and figure out what should be done in each one.

<iframe src="./outlier_case_files.html" width="100%" height="900" style="border: none"></iframe>
