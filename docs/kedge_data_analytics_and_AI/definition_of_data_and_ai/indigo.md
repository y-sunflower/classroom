---
icon: lucide/database
---

!!! abstract "Indigo"

    For this course, we'll assume that we work for the marketing department of Indigo, a company selling organic cleaning products. Indigo wants to launch a new refillable shampoo product.

We want to answer questions such as:

- Who might be interested in the product in the current customer base?
- Which message and channel should we use?
- How should we brand that product?
- How should we price that product?
- What are customers saying about the product?
- Did the launch increase sales?
- What does that teach us about launching a new product?

## Data

We have access to the following datasets:

=== "Sales"

    Each transaction, products bought, quantity, customer ID, price, and date.

    <csv-table src="../data/sales.csv" caption="Sales transactions" page-size="10"></csv-table>

=== "Website analytics"

    Customer visits, where they came from, products viewed, and whether they added items to their cart or purchased them

    <csv-table src="../data/website_analytics.csv" caption="Website analytics" page-size="10"></csv-table>

=== "Product reviews"

    Customer ratings and written reviews about products.

    <csv-table src="../data/product_reviews.csv" caption="Product reviews" page-size="10"></csv-table>

=== "Marketing campaigns"

    Campaigns sent to customers, channel (email, ads), message, and whether customers clicked or purchased.

    <csv-table src="../data/marketing_campaigns.csv" caption="Marketing campaigns" page-size="10"></csv-table>

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

### Pair activity: what data would Indigo need?

Choose one of the case questions and work with a partner.

1. Write the decision the team wants to make.
2. List three pieces of data that could help.
3. For each piece, write where it could come from.
4. Add one reason the data might be incomplete, misleading, or inappropriate.

Use this template:

| Decision | Data needed | Possible source | One limitation |
| -------- | ----------- | --------------- | -------------- |
|          |             |                 |                |
|          |             |                 |                |
|          |             |                 |                |

## 4. Data types and data sources

### Structured and unstructured data

**Structured data** is organised according to a known format, often rows and columns. Each row might represent a customer, order, or campaign event, while each column has a defined meaning.

| customer_id | order_date | product        | amount_eur |
| ----------- | ---------- | -------------- | ---------: |
| 1042        | 2026-09-03 | refill shampoo |      24.90 |
| 1088        | 2026-09-04 | refill pouch   |      12.50 |

Structured data is convenient to filter and summarise, but a neat table can still contain errors or unfair measurements.

**Unstructured data** does not arrive in a simple table with a fixed schema. Examples include review text, interview recordings, images, videos, presentations, and social-media content. It may contain valuable context, but it usually needs additional interpretation or processing before it can be compared systematically.

Some data is **semi-structured**: it has labels or a loose organisation but not a simple table. Examples include website event records in JSON format, email headers, and some API responses.

### Internal, external, and open data

| Source            | What it means                                             | Marketing example                                                        | Questions to ask                                                                     |
| ----------------- | --------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| **Internal data** | Collected by or for the organisation                      | Orders, CRM records, campaign spend, customer-service contacts           | Was it collected for this purpose? Is it accurate and was it collected with consent? |
| **External data** | Comes from outside the organisation                       | A media platform report, a research panel, a partner, or a market report | What is the provider's method and incentive? Can the definitions be compared?        |
| **Open data**     | External data available for reuse under stated conditions | Public population, weather, transport, or economic statistics            | What licence, geography, date, and limitations apply?                                |

External does not necessarily mean open. A company may buy external data that cannot be freely shared or reused.

### Panel and tracking data

**Panel data** follows the same people, households, stores, or organisations repeatedly over time. It can help reveal changes in behaviour, but participants may drop out or change their behaviour because they know they are being observed.

**Tracking data** records behaviour over time, such as visits, clicks, movement through a website, or repeated exposure to an advertisement. Tracking can support measurement and personalisation, but it raises important questions about consent, identity, retention, and the difference between observing behaviour and understanding motivation.

### Activity: match the source to the question

For each question, choose one or more suitable data sources. Then write one limitation.

| Marketing question                                 | Possible data source | One limitation |
| -------------------------------------------------- | -------------------- | -------------- |
| Did the campaign increase orders?                  |                      |                |
| What do customers like or dislike about the scent? |                      |                |
| Which regions might need more delivery capacity?   |                      |                |
| How does behaviour change after three months?      |                      |                |

!!! tip "Do not confuse a proxy with the thing itself"

    A click is a record of clicking, not proof that someone read, liked, remembered, or believed a message. A purchase is evidence of a transaction, not a complete explanation of motivation.

### Data quality: fit for purpose

Before using data, check at least the following dimensions:

- **Accuracy:** Does it represent what it claims to represent?
- **Completeness:** Are important values missing?
- **Consistency:** Do the same concepts use the same definitions and formats?
- **Timeliness:** Is it recent enough for this decision?
- **Uniqueness:** Are records duplicated?
- **Validity:** Do values follow the expected rules, such as a percentage between 0 and 100?
- **Representativeness:** Who is absent or overrepresented?
- **Provenance:** Who collected it, how, when, and under what conditions?

Quality is not the same as perfection. A dataset is fit for purpose when its limitations are understood and acceptable for the decision being made.

## 5. The people behind data and AI

Data work is collaborative. Job titles vary between organisations, and one person may perform several roles in a small company.

| Role                              | Main responsibility                                                                      | Example question from Indigo                                        |
| --------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Chief Data Officer (CDO)**      | Connects data strategy, governance, and business priorities                              | Are we building responsible data capabilities?                      |
| **Data engineer**                 | Builds and maintains systems that collect, move, and store data                          | Can campaign, order, and website data arrive reliably in one place? |
| **Data analyst**                  | Explores and summarises data to answer business questions                                | Which channel had the strongest conversion rate last month?         |
| **Statistician**                  | Designs measurement, samples, experiments, and uncertainty analysis                      | Is the apparent campaign effect larger than normal variation?       |
| **Data scientist**                | Uses statistics, machine learning, and programming to model patterns or make predictions | Which customers are likely to respond to an offer?                  |
| **Data translator**               | Connects business needs, data work, and communication across teams                       | What does "successful launch" mean, and how will we measure it?     |
| **Data Protection Officer (DPO)** | Advises on privacy, data protection obligations, rights, and governance                  | Are we allowed to use this personal data for this purpose?          |

The DPO is not the person who "makes data safe" alone. Everyone who collects, analyses, shares, or acts on data has a responsibility to handle it appropriately.

### Activity: who should be involved?

For each request, identify the first role you would involve and at least one other role they might need.

1. "Our dashboard shows a 40% improvement. Can we publish it?"
2. "The customer data from two systems uses different country codes."
3. "Can we use browsing behaviour to target people with a new offer?"
4. "We want to predict which customers will stop buying."

The marketing manager remains responsible for the business decision. Data specialists help make the evidence more reliable; they do not replace accountability.

### Activity: the AI question checklist

Choose one of the techniques above and answer these questions:

1. What is the decision that the system will support?
2. What is the input data?
3. What would the output be: a number, category, ranking, text, or image?
4. What would count as a useful and fair result?
5. Who could be missing, misclassified, or harmed?
6. What should a person check before acting on the output?

If you cannot answer the first two questions, the problem is probably not ready for AI. Start by clarifying the decision and the data.

!!! warning "Human judgement remains part of the system"

    A model can be technically accurate and still be a poor business choice if the target is wrong, the data is unfair, the output is not actionable, or the use violates people's expectations or rights.

## Exit ticket

Answer these questions in your own words:

1. What is the difference between big data and smart data?
2. Why is open data not automatically suitable for a marketing decision?
3. Give one example of structured data and one example of unstructured data.
4. Which role would you involve for a privacy question? Which role would you involve for a data pipeline problem?
5. For customer-review analysis, which AI technique could help, and what is one limitation?
