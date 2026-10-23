---
icon: lucide/brain-circuit
---

## Use a model

Now that we have our model saved to disk, let's see how we can:

- load it
- define the inputs we want
- make a prediction

### Load the model

```py exec="on" source="above" session="use-model"
import joblib
import numpy as np

model = joblib.load("src/data_analytics_and_AI/analyzing_data/exercise_model.joblib")
```

### Inputs

```py exec="on" source="above" session="use-model"
subscription_level = "Deluxe"
tenure_months = 9
monthly_price_eur = 50
food_preference = "Mixed"
delivery_issues_6m = 0
satisfaction_score = 7
boxes_skipped_6m = 0
discount_used = 0

X = np.array([[
      subscription_level,
      tenure_months,
      monthly_price_eur,
      food_preference,
      delivery_issues_6m,
      satisfaction_score,
      boxes_skipped_6m,
      discount_used,
]], dtype=object)
```

### Make prediction

```py exec="on" source="above" session="use-model"
probability = model.predict_proba(X)[0, list(model.classes_).index(1)]

print(f"Churn probability: {probability:.1%}")
```

!!! question

      What is the churn probability of someone who is a **vegetarian** with a **premium** subscription, been subscribed since **2 months**, **no issue delivery** in the last 6 months, **satisfaction of 1** and **without discount**?

## Web application

This works well, but now let's say the CMO :material-information-outline:{ title="Chief Marketing Officer" } wants to be able to use that model too? Let's make a web app!

!!! tip

      For this we'll use [Streamlit](https://streamlit.io/), the **simplest way to create a web app with Python**.

### Basic app

Create a new `app.py` file with the following:

```py
import streamlit as st

st.title("My first app")
st.write("Welcome to my app!")

name = st.text_input("Your name")

if st.button("Submit"):
    if name:
        st.success(f"Hello, {name}!")
    else:
        st.warning("Please enter your name.")
```

Then open a terminal and run:

```sh
uv run streamlit run app.py
```

Change the code in `app.py` so that instead of asking for the name, it asks for the age. Use `st.number_input()` instead of `st.text_input()`. The code should display a different message depending on whether user is more than 20 yo or not.

### Integrate our model
