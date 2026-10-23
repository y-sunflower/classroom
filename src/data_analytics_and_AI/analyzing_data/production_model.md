---
icon: lucide/brain-circuit
---

## Use a model

Now that we have our model saved to disk, let's see how we can:

- load it
- define the inputs we want
- make a prediction

#### Load the model

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

Let's replace the toy app with one that asks for a customer's details and uses our saved model. Continue editing the `app.py` from the previous section. Add each part below in order.

### Load the model

First, import the libraries we need. `Path` lets us find the saved model in the same folder as `app.py`.

```py
from pathlib import Path

import joblib
import numpy as np
import streamlit as st
```

Load the model once and let Streamlit keep it ready while the app reruns after a user changes an input:

```py
#@st.cache_resource
def load_model():
    model_path = Path(__file__).with_name("exercise_model.joblib")
    return joblib.load(model_path)


model = load_model()
plan_prices = {"Basic": 30, "Deluxe": 50, "Premium": 100}
```

#### Ask for customer details

Add a title and input widgets for the features. The monthly price comes from the selected plan, so users don't have to enter it separately.

```py
st.title("Customer churn prediction")
st.write("Enter a customer's details to estimate their likelihood of churning.")

subscription_level = st.selectbox("Subscription plan", plan_prices)
tenure_months = st.slider("Months subscribed", 1, 60, 9)
food_preference = st.selectbox(
    "Food preference", ["Mixed", "Vegetarian", "Vegan", "High Protein"]
)
delivery_issues_6m = st.slider("Delivery issues in the last 6 months", 0, 6, 0)
satisfaction_score = st.slider("Satisfaction score", 1, 10, 7)
boxes_skipped_6m = st.slider("Boxes skipped in the last 6 months", 0, 6, 0)
discount_choice = st.selectbox("Used a discount?", ["No", "Yes"])
```

#### Pass the inputs to the model

The model expects the features in the same order used during training. Add a button and arrange the selected values in that order. `dtype=object` allows the array to contain both text and numbers.

```py
if st.button("Predict churn", type="primary"):
    discount_used = int(discount_choice == "Yes")
    X = np.array(
        [[
            subscription_level,
            tenure_months,
            plan_prices[subscription_level],
            food_preference,
            delivery_issues_6m,
            satisfaction_score,
            boxes_skipped_6m,
            discount_used,
        ]],
        dtype=object,
    )
```

#### Show the prediction

The model returns a probability for each class. Find the column for class `1` (churn) and display that probability, along with the model's yes-or-no prediction:

```py
    churn_class_index = list(model.classes_).index(1)
    churn_probability = model.predict_proba(X)[0, churn_class_index]

    st.metric("Churn probability", f"{churn_probability:.1%}")
    if model.predict(X)[0] == 1:
        st.warning("This customer is predicted to churn.")
    else:
        st.success("This customer is predicted to stay.")
```

Launch the app:

```sh
uv run streamlit run app.py
```

!!! tip

      Once it works, try a few different customer profiles!
