---
icon: lucide/database
---

## Data

> Any information that can be collected, stored, and analyzed

In practice, we often separate tabular and non-tabular data.

=== "Tabular"

    ==Can fit into a table or a spreadsheet==

    - **Numerical**: prices, temperatures, revenue, sensor measurements, ages, time spent, number of clicks, etc.
    - **Categorical**: country, product category, customer type, yes/no values, etc.
    - **Time-series**: stock prices, website traffic, heart rate measurements, IoT readings over time.
    - **Graph/network**: social connections, relationships between companies, transportation networks.
    - **Location/spatial**: GPS coordinates, maps, geographic regions.

=== "Non-tabular"

    ==Everything else==

    - **Text**: emails, reviews, documents, social media posts, support conversations.
    - **Images**: photographs, medical scans, satellite imagery, handwritten digits.
    - **Audio**: speech recordings, music, environmental sounds.
    - **Video**: surveillance footage, sports recordings, driving footage.

## Big data

**Big data** describes data whose scale, speed, diversity, or complexity creates challenges for traditional tools and processes. A common way to remember the challenges is the "3 Vs" (sometimes 5):

|              | Meaning                              | Example                                         |
| ------------ | ------------------------------------ | ----------------------------------------------- |
| **Volume**   | A lot of records                     | Millions of website events                      |
| **Velocity** | Data arrives quickly or continuously | Live clicks during a product launch             |
| **Variety**  | Many formats and sources             | Tables, reviews, images, video, and sensor data |

Big data is not automatically valuable. A large dataset can still be irrelevant, biased, badly collected, or impossible to interpret.

## Smart data

**Smart data** is a practical label for data that has been selected, prepared, contextualised, and governed so that it can support a specific decision. It is not necessarily large.

For a campaign, a small table containing recent, consented, relevant customer segments may be more useful than billions of unfiltered social-media events. Smart data should be:

- relevant to the question
- understandable, with clear definitions and units
- timely enough for the decision
- checked for quality and bias
- collected and used lawfully
- connected to an action or decision.

## Open data

**Open data** is data that people can access, use, and share under stated conditions, usually through an open licence. "Open" does not mean "anything is allowed": a licence can require attribution, prohibit certain uses, or specify how the data can be shared.

!!! tip "Open data in France"

    In France, a lot of data is made public via the [data.gouv.fr platform](https://www.data.gouv.fr/). There are a lot of things you can find: businesses and the economy, real estate and urban planning, geography and addresses, transport and mobility, energy and the environment, health, education, employment and population, agriculture and food, public administration and finance, elections and public life, culture, and security.

## Data in AI vs AI

What we call "AI" often means generative AI, but AI is much more than that.

<center>
    
```mermaid
flowchart TB
    A["Rule-Based Systems<br/>1950s–1980s<br/>IF / ELSE • Expert Systems"]
    B["Early Learning Algorithms<br/>1950s–1990s<br/>Perceptron • Decision Trees"]
    C["Machine Learning<br/>1990s–2010s<br/>SVM • Random Forests • Statistical Learning"]
    D["Deep Learning<br/>2010s<br/>Neural Networks • CNNs • RNNs • Transformers"]
    E["Generative AI<br/>2020s–Today<br/>LLMs • Diffusion Models • Multimodal AI"]

    A -->|"Rules → Learning from data"| B
    B -->|"Better algorithms + more data"| C
    C -->|"Large datasets + GPUs"| D
    D -->|"Foundation models"| E

```

</center>

Today, most people doing data analytics aren't doing AI, but all AI researchers/engineers are working with data.

The rise of Gen AI has been possible mostly **because of compute availability**:

![A graph showing the growth in transistor counts from 1970 to 2020, illustrating Moore's law](https://upload.wikimedia.org/wikipedia/commons/0/00/Moore%27s_Law_Transistor_Count_1970-2020.png?utm_source=en.wikipedia.org&utm_campaign=imageinfo&utm_content=thumbnail_unscaled)

We're now using an extremely high amount of compute, and even more each year:

![A graph showing that the amount of compute used to train AI models doubles over time](https://upload.wikimedia.org/wikipedia/commons/4/4b/Ai_training_compute_doubling_v2.png?utm_source=en.wikipedia.org&utm_campaign=imageinfo&utm_content=thumbnail_unscaled)

## Jobs

Data work is collaborative. Job titles vary between organisations, and one person may perform several roles in a small company.

| Role                              | Main responsibility                                                                      |
| --------------------------------- | ---------------------------------------------------------------------------------------- |
| **Chief Data Officer (CDO)**      | Connects data strategy, governance, and business priorities                              |
| **Data engineer**                 | Builds and maintains systems that collect, move, and store data                          |
| **Data analyst**                  | Explores and summarises data to answer business questions                                |
| **Data scientist**                | Uses statistics, machine learning, and programming to model patterns or make predictions |
| **Data Protection Officer (DPO)** | Advises on privacy, data protection obligations, rights, and governance                  |

In practice, many of those job titles are mixed together and companies often don't make true differences between them. Also,


## Going further:

- [Video, FR] [How does ChatGPT run on a single database server](https://www.youtube.com/watch?v=Awu5RoPmy-0)
- [Blog, EN] [Big data doesn't exist](https://techcrunch.com/2015/09/10/big-data-doesnt-exist/)
```
