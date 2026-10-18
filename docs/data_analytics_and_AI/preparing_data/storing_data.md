---
icon: lucide/brush-cleaning
---

## Where the data live

=== "Data warehouse"

    A **data warehouse** stores structured, organised data prepared for reporting and analysis. Teams agree on definitions, formats, and relationships before analysts query it.

    **Marketing example:** a set of consistent campaign, customer, and sales tables used for a monthly performance report.

=== "Data lake"

    A **data lake** stores data in its original or lightly prepared form, often across many formats. Analysts and engineers decide how to interpret it when they use it.

    **Marketing example:** raw website events, campaign exports, product reviews, and image files retained for future analysis.

=== "Both together"

    Many organisations use both. They may keep raw exports in a lake, then publish quality-checked tables to a warehouse. A data lake does not automatically mean that data is messy, and a warehouse does not guarantee that every definition is correct.

!!! note

    In this course, we'll work with **CSV files**. It's a very common data file format, but isn't a database.

## Relational data

A **relational database** stores data in tables with defined columns. A row describes one record, and keys connect records across tables.

| Table            | One row represents               | Example key      |
| ---------------- | -------------------------------- | ---------------- |
| `campaign_sends` | One message sent to one customer | `send_id`        |
| `sales`          | One transaction                  | `transaction_id` |
| `website_visits` | One visit                        | `visit_id`       |

For Indigo, `campaign_sends.send_id` can connect to `sales.campaign_send_id`. A key lets us combine related information without copying every campaign detail into every sale.

Relational systems work well when data has a clear structure and accurate links matter, such as orders, inventory, and campaign reporting. Examples include **PostgreSQL**, **MySQL**, and **SQL Server**.

## Non-relational data

**Non-relational databases**, often grouped under the term _NoSQL_, do not require every record to follow the same table structure. Common models include:

=== "Document"

    Stores records as documents, often JSON. Useful when each product or event can have a different set of attributes.

    ``` json
    {
      "product_id": "P014",
      "name": "Active Mat 14",
      "attributes": {"colour": "blue", "material": "foam"}
    }
    ```

=== "Key-value"

    Stores a value under a key. Useful for fast lookups such as a temporary shopping basket or a cached campaign setting.

=== "Graph"

    Stores entities and the relationships between them. Useful when the connections themselves matter, such as a referral network or products frequently bought together.

=== "Wide-column"

    Groups values by column families and is designed for large, distributed workloads such as streams of website events.

Examples include **MongoDB** for documents, **Redis** for key-value data, and **Neo4j** for graphs. A non-relational system is not automatically faster or more flexible for every task; its data model should fit the questions and workload.
