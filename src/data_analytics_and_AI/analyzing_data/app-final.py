from pathlib import Path

import joblib
import numpy as np
import streamlit as st


# @st.cache_resource
def load_model():
    model_path = Path(__file__).with_name("exercise_model.joblib")
    return joblib.load(model_path)


model = load_model()
plan_prices = {"Basic": 30, "Deluxe": 50, "Premium": 100}

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

if st.button("Predict churn", type="primary"):
    discount_used = int(discount_choice == "Yes")
    X = np.array(
        [
            [
                subscription_level,
                tenure_months,
                plan_prices[subscription_level],
                food_preference,
                delivery_issues_6m,
                satisfaction_score,
                boxes_skipped_6m,
                discount_used,
            ]
        ],
        dtype=object,
    )

    churn_class_index = list(model.classes_).index(1)
    churn_probability = model.predict_proba(X)[0, churn_class_index]

    st.metric("Churn probability", f"{churn_probability:.1%}")
    if model.predict(X)[0] == 1:
        st.error("This customer is predicted to churn.")
    else:
        st.success("This customer is predicted to stay.")
