---
icon: lucide/message-square-text
---

We already know how to work with prices, clicks, and customer characteristics. But what do we do with something like this?

> *"Love the product. The packaging though... why does a tiny bottle need this much plastic?"* Customer A

Looking at the average rating doesn't necessarily tell the whole story. The customer can like the product **and** have a problem with its packaging. Those are two different things we could act on.

**Text mining** means extracting useful information from text: reviews, survey answers, support messages, social media posts, etc. Here we'll use customer reviews to figure out what people talk about, how they feel, and what a marketing team could do with that information.

!!! abstract "Our goal"

    We work for an online shop. Before its next campaign, the marketing team wants to know:

    - What do customers keep mentioning?
    - Can we automatically flag unhappy reviews for someone to read?
    - Which findings could improve the product page or campaign message?


## Dataset

We'll reuse a product reviews dataset. One row is one review of a purchased product. For this session, the most useful columns are `review_id`, `product_name`, `rating`, and `review_text`.

<csv-table src="../data/product_reviews.csv" caption="Customer reviews" page-size="6" download="product_reviews.csv"></csv-table>

- Click **Download data** in the table above and save `product_reviews.csv` in your Positron project folder.
- Create a file called `text_mining.py`.
- If needed, install the packages from the Positron terminal:

```sh
uv add polars scikit-learn
```

!!! tip "Run from your project folder"

    The code below expects the CSV and your Python file in the same project folder. Run it with that folder open in Positron.

## Read a few reviews

You can calculate a lot of things without understanding the data, but that's usually a pretty bad idea.

### Example

```python exec="on" source="above" result="text" session="explore-reviews" workdir="src/data_analytics_and_AI/data"
import polars as pl

reviews = pl.read_csv("product_reviews.csv")

for review in reviews.sample(5).to_dicts():
    print(f"\n{review['rating']} stars: {review['review_text']}")
```

`.to_dicts()` turns the rows into Python dictionaries, so we can print the full sentences without the table cutting them off.


## Prepare a text column

`"LOVE"`, `"Love"`, and `"love"` are different strings. For counting words, we probably want to treat them as the same word.

Polars has a [`.str` namespace](https://docs.pola.rs/api/python/stable/reference/expressions/string.html) for operations on text. We'll start with `.str.to_lowercase()` and `.str.strip_chars()`, which removes whitespace at the beginning and end.

### Example

```python exec="on" source="above" result="text" session="explore-reviews"
reviews = reviews.with_columns(
    text_clean=pl.col("review_text")
    .str.to_lowercase()
    .str.strip_chars()
)

print(reviews.select("review_text", "text_clean").head(3))
```

### Exercise

Create this small table and apply the same cleaning steps:

```python
examples = pl.DataFrame({
    "review_text": ["  LOVE IT!!!  ", "Not good.", "Good, but too expensive."]
})

# TODO: create text_clean and print both columns
```

What information would disappear if we also deleted punctuation? What would happen if we deleted the word `"not"`?

!!! warning "Cleaning depends on the question"

    Punctuation, emojis, capitals, and small words can carry meaning. `"good"` and `"not good"` aren't interchangeable!

## Find reviews about a topic


### Example

```python exec="on" source="above" result="text" session="explore-reviews"
packaging_reviews = reviews.filter(
    pl.col("text_clean").str.contains("packaging")
)

print(f"Reviews mentioning packaging: {packaging_reviews.height}\n")
for text in packaging_reviews["review_text"].sample(5):
    print(f'"{text}"')
```

!!! note
        
    It's a substring search, so searching for `"price"` also finds `"overpriced"`.

### Exercise

Find reviews that mention either `"price"` **or** `"expensive"`. Create one `.str.contains(...)` condition for each word, then combine them with `|` (meaning **or**), as in `condition_a | condition_b`.

- Count the matching reviews and calculate their share of all reviews.
- Read five matches. Are they all complaints?
- Find an example your search could miss. Could someone complain about price without using either word?

```python
price_reviews = reviews.filter(
    # TODO: combine two .str.contains(...) conditions
)

# TODO: calculate the share, using price_reviews.height and reviews.height
```

??? question "Does mentioning packaging mean disliking packaging?"

    <span class="answer">No. A keyword tells us something about the topic. It doesn't tell us whether the customer likes it, dislikes it, or is just describing it.</span>

## Count words

Instead of choosing a keyword ourselves, we can look at the **most frequent words**. First, we need to break each review into smaller pieces called **tokens**. Here, a token will simply be a sequence of English letters.

### Example

```python exec="on" source="above" result="text" session="explore-reviews"
words = (
    reviews.select(
        "review_id",
        word=pl.col("text_clean").str.extract_all(r"[a-z]+")
    )
    .explode("word")
)

print(words)
```

- `r"[a-z]+"` is a **regular expression** (often called **regex**), a pattern meaning "one or more letters from a to z".
- `.str.extract_all(...)` creates a list of matches for each review.
- `.explode("word")` turns each list into separate rows: **one row per word occurrence**.

This simple pattern is for our English examples. It will split contractions like `"don't"` and won't handle every language correctly.

Now we can group and count, just like we did with sales:

```python exec="on" source="above" result="text" session="explore-reviews"
word_counts = (
    words.group_by("word")
    .len(name="occurrences")
    .sort("occurrences", descending=True)
)

print(word_counts.head(10))
```

### Exercise

For a topic-frequency ranking, common words such as `"the"` or `"it"` often tell us little about what customers discuss. We can treat them as **stop words** and exclude them from this ranking. They still have meaning in sentences, and a useful stop-word list depends on the task. Here's a short list to get started:

```python
stop_words = ["the", "a", "an", "it", "i", "and", "is", "this", "for", "to", "of", "in"]

useful_words_counts = word_counts.filter(
    # TODO: exclude the chosen stop words using this syntax:
    # ~pl.col("col_name").is_in(list_of_stop_words)
)
```

`~` reverses a condition: here it means "keep words that are **not** in this list".

Compare the ranking before and after filtering. Choose two words worth investigating and read reviews containing them. What can you learn that the ranking alone didn't show?

??? tip "One customer can repeat a word"

    `"Love love love it"` adds three occurrences of `"love"`. If you want to count **reviews mentioning a word**, first use `words.unique(subset=["review_id", "word"])`, then group and count.

Now explore the remaining words and choose **up to ten additional stop words** for this topic ranking. Read reviews containing each candidate and explain why removing it helps. Keep words that convey sentiment or contrast, such as `"not"` and `"but"`, and words that identify a topic, such as `"price"`. Add your choices to `stop_words` and rerun the filter; don't change the original review text.

## Turn mentions into a useful comparison

If there are many more positive reviews, they may also contain more mentions of almost everything. Raw counts alone can be misleading.

Let's compare the **share of reviews mentioning delivery**, separately for each star rating.

### Example

```python exec="on" source="above" result="text" session="explore-reviews"
reviews_delivery = reviews.with_columns(
    mentions_delivery = pl.col("text_clean").str.contains("delivery|shipping")
)

delivery_by_rating = (
    reviews_delivery.group_by("rating")
    .agg(
        n_reviews=pl.len(),
        delivery_mentions=pl.col("mentions_delivery").sum(),
        delivery_share=pl.col("mentions_delivery").mean().round(4)*100,
    )
    .sort("rating")
)

print(delivery_by_rating)
```

### Exercise

Adapt the example to packaging. Keep the number of reviews, number of matches, and share for each rating.

- Which rating group has the highest share?
- Read a few matches from that group. What do they actually say?

