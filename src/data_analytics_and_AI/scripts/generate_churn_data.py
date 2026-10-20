import numpy as np
import polars as pl

SEED = 42
N_CUSTOMERS = 15000
OUTPUT_FILE = "src/data_analytics_and_AI/data/food_subscription_churn.csv"

rng = np.random.default_rng(SEED)

subscription_level = rng.choice(
    ["Basic", "Deluxe", "Premium"], size=N_CUSTOMERS, p=[0.50, 0.35, 0.15]
)

price_map = {"Basic": 30, "Deluxe": 50, "Premium": 100}

monthly_price = np.array([price_map[level] for level in subscription_level])

food_preference = rng.choice(
    ["Mixed", "Vegetarian", "Vegan", "High Protein"],
    size=N_CUSTOMERS,
    p=[0.45, 0.25, 0.15, 0.15],
)

tenure_months = np.clip(rng.geometric(p=0.065, size=N_CUSTOMERS), 1, 60)

delivery_issues = np.clip(
    rng.poisson(0.65 + 0.12 * (subscription_level == "Basic"), size=N_CUSTOMERS), 0, 6
)

latent_satisfaction = (
    7.7
    - 0.75 * delivery_issues
    + 0.35 * (subscription_level == "Premium")
    + 0.20 * (subscription_level == "Deluxe")
    + rng.normal(0, 1.7, N_CUSTOMERS)
)

satisfaction = np.clip(np.rint(latent_satisfaction), 1, 10).astype(int)

skip_probability = np.clip(
    0.07
    + 0.025 * (10 - satisfaction)
    + 0.025 * (subscription_level == "Premium")
    + 0.025 * (tenure_months < 4),
    0.02,
    0.65,
)

boxes_skipped = rng.binomial(np.minimum(tenure_months, 6), skip_probability)

discount_probability = np.clip(
    0.28
    + 0.12 * (subscription_level == "Basic")
    + 0.10 * (tenure_months < 6)
    - 0.08 * (subscription_level == "Premium"),
    0.05,
    0.80,
)

discount_used = rng.binomial(1, discount_probability)

sigmoid = lambda x: 1 / (1 + np.exp(-x))

logit = (
    -1.90
    + 0.36 * (subscription_level == "Basic")
    - 0.18 * (subscription_level == "Deluxe")
    + 0.20 * (subscription_level == "Premium")
    - 0.025 * np.minimum(tenure_months, 36)
    + 0.28 * delivery_issues
    - 0.20 * (satisfaction - 6)
    + 0.34 * boxes_skipped
    + 0.12 * discount_used
    + 0.12 * (food_preference == "Vegan")
    + 0.08 * (food_preference == "High Protein")
    + 0.65 * ((subscription_level == "Premium") & (satisfaction <= 5))
    + 0.50 * ((delivery_issues >= 2) & (boxes_skipped >= 2))
    - 0.45 * ((tenure_months >= 18) & (satisfaction >= 8))
    + 0.35 * ((discount_used == 1) & (tenure_months <= 3))
    + rng.normal(0, 0.45, N_CUSTOMERS)
)

churn_probability = sigmoid(logit)
churn = rng.binomial(1, churn_probability)

df = pl.DataFrame(
    {
        "subscription_level": subscription_level,
        "tenure_months": tenure_months,
        "monthly_price_eur": monthly_price,
        "food_preference": food_preference,
        "delivery_issues_6m": delivery_issues,
        "satisfaction_score": satisfaction,
        "boxes_skipped_6m": boxes_skipped,
        "discount_used": discount_used,
        "churn": churn,
    }
)

df.write_csv(OUTPUT_FILE)

print(f"Saved {len(df):,} customers to {OUTPUT_FILE}")
print(df.head(10))

print("\nOverall churn rate:")
print(df.select(pl.col("churn").mean()))

print("\nChurn by subscription level:")
print(
    df.group_by("subscription_level")
    .agg(
        pl.len().alias("customers"),
        pl.col("churn").mean().round(3).alias("churn_rate"),
    )
    .sort("subscription_level")
)
