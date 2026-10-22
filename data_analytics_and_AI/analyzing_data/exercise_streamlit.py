from pathlib import Path

import joblib
import numpy as np
import polars as pl
import streamlit as st

MODEL_PATH = Path(__file__).with_name("exercise_model.joblib")
CUSTOMERS_PATH = Path(__file__).parents[1] / "data" / "food_subscription.csv"
PLAN_PRICES = {"Basic": 30, "Deluxe": 50, "Premium": 100}
FEATURE_COLUMNS = [
    "subscription_level",
    "tenure_months",
    "monthly_price_eur",
    "food_preference",
    "delivery_issues_6m",
    "satisfaction_score",
    "boxes_skipped_6m",
    "discount_used",
]


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_customers():
    customers = pl.read_csv(CUSTOMERS_PATH).drop("churn")
    return customers.with_row_index("customer_id", offset=1).select(
        "customer_id", *FEATURE_COLUMNS
    )


def make_prediction(customer):
    customer_features = np.array(
        [[customer[feature] for feature in FEATURE_COLUMNS]], dtype=object
    )
    model = load_model()
    predicted_churn = int(model.predict(customer_features)[0])
    churn_class_index = list(model.classes_).index(1)
    churn_probability = float(
        model.predict_proba(customer_features)[0, churn_class_index]
    )
    return predicted_churn, churn_probability


st.set_page_config(page_title="Churn prediction", page_icon="📦")
st.title("Customer churn prediction")
st.write("Enter a customer's details to estimate their likelihood of churning.")

customer_to_predict = None
from_data, manual_entry = st.tabs(["Choose a customer", "Enter details manually"])

with from_data:
    customers = load_customers()
    st.write("Select a customer row, then predict their churn likelihood.")
    selection = st.dataframe(
        customers,
        hide_index=True,
        height=420,
        on_select="rerun",
        selection_mode="single-row",
        key="customer_table",
    )
    selected_rows = selection.selection.rows
    if selected_rows:
        row = customers.row(selected_rows[0], named=True)
        customer_id = row.pop("customer_id")
        st.caption(f"Selected customer {customer_id}.")
        if st.button("Predict selected customer", type="primary"):
            customer_to_predict = row

with manual_entry:
    with st.form("customer_details"):
        left, right = st.columns(2)

        with left:
            subscription_level = st.selectbox("Subscription plan", PLAN_PRICES)
            tenure_months = st.slider("Months subscribed", 1, 60, 9)
            food_preference = st.selectbox(
                "Food preference", ["Mixed", "Vegetarian", "Vegan", "High Protein"]
            )
            delivery_issues_6m = st.slider(
                "Delivery issues in the last 6 months", 0, 6, 0
            )

        with right:
            satisfaction_score = st.slider("Satisfaction score", 1, 10, 7)
            boxes_skipped_6m = st.slider("Boxes skipped in the last 6 months", 0, 6, 0)
            discount_used = st.selectbox("Used a discount?", ["No", "Yes"])

        submitted = st.form_submit_button("Predict churn", type="primary")

    if submitted:
        customer_to_predict = {
            "subscription_level": subscription_level,
            "tenure_months": tenure_months,
            "monthly_price_eur": PLAN_PRICES[subscription_level],
            "food_preference": food_preference,
            "delivery_issues_6m": delivery_issues_6m,
            "satisfaction_score": satisfaction_score,
            "boxes_skipped_6m": boxes_skipped_6m,
            "discount_used": int(discount_used == "Yes"),
        }

if customer_to_predict:
    predicted_churn, churn_probability = make_prediction(customer_to_predict)

    st.subheader("Prediction")
    if predicted_churn:
        st.warning("This customer is predicted to churn.")
    else:
        st.success("This customer is predicted to stay.")
    st.metric("Churn probability", f"{churn_probability:.1%}")
