---
icon: lucide/brush-cleaning
---

## What does "clean" means

Data cleaning makes a dataset more consistent and useful for a specific question. Poor quality can distort a campaign comparison, hide an operational issue, or lead a team to act on the wrong customers. In practice, we want to make the [data "tidy"](https://vita.had.co.nz/papers/tidy-data.pdf).

In the previous lesson we saw the common operations of how to clean data (select columns, filter rows, aggregations). Here we'll talk about common issues that we have when cleaning data, why they can occur and how to "fix" (if they need a fix).

## Missing values

=== "completely at random"

      Data is missing for purely random reason. This is the ideal case since ignoring those data has no impact on our analysis, but this is almost never the case in the real world.

      A bank with customer info might have missing info about the job of customers. It's likely that people who don't want to share their job have reasons: bad credit score, illegal activities, ...

=== "at random"

      Missingness isn't random and can be explained by other variables.

      Male are less likely to do depression diagnostic, but this has nothing to do with the level of depression. Statistics allow us to easily take into account maleness.

=== "not at random"

      Missing data where the value of the variable that's missing is related to the reason it's missing. People with high depression symptoms are more likely to not answer questions **because** of their depressions.

=== "by design"

      When sending marketing emails, time spend on the website being empty isn't really missing data if user didn't click on the link to the website.
