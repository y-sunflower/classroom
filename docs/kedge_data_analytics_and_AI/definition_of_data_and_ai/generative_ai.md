---
icon: lucide/database
---

## Transformers

In 2017, Google researchers published a now extremely famous paper titled [Attention is all you need](https://papers.nips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf), presenting the **Transformer architecture**.

<iframe src="https://ig.ft.com/generative-ai/" width="100%" height="700"></iframe>

Source: [Generative AI exists because of the transformer](https://ig.ft.com/generative-ai/)

## An LLM isn't a database

It might feel natural to compare an LLM to a search tool like Google, but they are very different. An LLM is literally one (or multiple) file(s) stored somewhere. It contains between **dozens of millions** of parameters (see example below) and **hundreds of billions** of parameters (Claude, ChatGPT, etc.).

Here is an AI running completely "offline". Once it says _"Ready: ...."_, you can:

- turn off your wifi
- try to chat with it

!!! warning

      - Don't refresh the page, otherwise it won't work
      - This might slow down your computer a little bit

<iframe src="./local_llm.html" width="100%" height="600"></iframe>

!!! tip

      Everything you ask the AI here is 100% private. Nobody, not even the instructor, could ever know what you ask it.

As you run some tests, you'll see that:

- answers are kind of weird and not very clear
- it often stops mid-sentence

The latter is because, at each step when making predictions, the model computes **what the next word in that sentence will be** (or token, as we should say). Its reasoning is basically something like this:

- Given all tokens so far, it computes a **probability distribution over the possible next tokens**. In the sentence _=="I hope I'll have a good [...]"==_, the LLM tries to figure out what _=="[...]"==_ could be. It is likely to predict something like a 40% chance of _=="day"==_, a 30% chance of _=="morning"==_, etc.
- A **token is selected** from that distribution: it could be the one with the highest chance (e.g., _=="day"==_) or some more sophisticated method.
- That token is **appended to the context**: the sentence becomes _=="I hope I'll have a good day [...]"==_.
- And the process **repeats**.
- Generation stops when the model produces a **special end-of-sequence (EOS) token**, or when some external stopping condition is reached (such as a maximum token limit).

## Before Gen AI

As we said before, there was "AI" long before "Generative AI", and non-generative AI still exists today. The process is exactly the same:

- gather a lot of data. In practice, it's often just user data.
- train an AI model on it for a specific task.
- evaluate that model
- make inferences with it

The list could be much longer, but the following are the most common use cases:

=== "fraud detection"

      *Detects suspicious transactions or unusual behavior that may indicate fraud, such as stolen credit cards or unauthorized payments.*

=== "recommendation systems"

      *Predicts what content or products a user is most likely to be interested in based on their behavior, preferences, and similar users. This is used, for example, by YouTube, TikTok, Instagram, Vinted, ...*

=== "medical image analysis"

      *Analyzes medical images such as X-rays, MRIs, or CT scans to help identify abnormalities, diseases, or other relevant patterns.*

=== "churn prediction"

      *Predicts which customers are likely to stop using a product or service, allowing companies to take action to retain them.*

Most of those uses fall into the **two main categories**:

- regression: predict a number (e.g., how much ice cream we need at this store next week)
- classification: predict a category (e.g., does this patient have a tumor or not?) or a probability (e.g., what are the odds of this patient having a tumor?)

!!! question

      In your opinion, does an LLM do regression or classification?

## Going further:

- [Video, FR] [Arthur Mensch, co-founder of Mistral AI, is being questioned at the National Assembly](https://www.youtube.com/watch?v=kKWOkWv6pJM)
- [Blog, EN] [Meet the $4 Billion AI Superstars That Google Lost](https://www.bloomberg.com/opinion/features/2023-07-13/ex-google-scientists-kickstarted-the-generative-ai-era-of-chatgpt-midjourney)
