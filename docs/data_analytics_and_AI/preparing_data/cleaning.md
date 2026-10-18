---
icon: lucide/brush-cleaning
---

## What does "clean" means

Data cleaning makes a dataset more consistent and useful for a specific question. Poor quality can distort a campaign comparison, hide an operational issue, or lead a team to act on the wrong customers. In practice, we want to make the [data "tidy"](https://vita.had.co.nz/papers/tidy-data.pdf).

In the previous lesson we saw the common operations of how to clean data (select columns, filter rows, aggregations). Here we'll talk about common issues that we have when cleaning data, why they can occur and how to "fix" (if they need a fix).

## Missing values

### Definitions

=== "completely at random"

      Data is missing for purely random reason. This is the ideal case since ignoring those data has no impact on our analysis, but this is almost never the case in the real world.

      A bank with customer info might have missing info about the job of customers. It's likely that people who don't want to share their job have reasons: bad credit score, illegal activities, ...

=== "at random"

      Missingness isn't random and can be explained by other variables.

      Male are less likely to do depression diagnostic, but this has nothing to do with the level of depression. Statistics allow us to easily take into account maleness.

=== "not at random"

      Missing data where the value of the variable that's missing is related to the reason it's missing. People with high depression symptoms are more likely to not answer questions **because** of their depressions.

=== "by design"

      When sending marketing emails, time spend on the website being empty isn't really missing data if user didn't click on the link to the website. Want to know how much time users spend on average on your website from your email campaign? Start by filtering users who did click on your email and you'll "remove" missing values.

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

A data point that differs significantly from others. Those data points can have a very high impact on the analysis we're doing, and the most common ways to deal with them are:

- remove them: simplify everything but arbitrary
- cap them: add upper/lower bound
- use techniques that aren't sensible to outliers
- mathematical transformations

None of them are fully satisfying. The good news is that most of the time extreme values **are here for a reason** (_assuming the data isn't corrupted_).

Let's say we're interested in the raw salary of Kedge BS students, 3 months after they left school. ==Click **generate**==

<iframe src="./outlier.html" width="100%" height="400" style="border: none"></iframe>

!!! tip

      - **Sample size** = how many students we have in our dataset?
      - **Seed** = number that defines randomness (same number implies same result, change number to see a different sample)

Most students are between 35k and 55k, but one student is at 73k, which is **62% more than the average** and **10% more than the second best**.
