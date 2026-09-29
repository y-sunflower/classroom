import math
import random
import string
from datetime import date, timedelta
from pathlib import Path
from typing import TypedDict

import polars as pl

SEED = 42
OUTPUT_DIR = Path("docs/kedge_data_analytics_and_AI/data")
START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)
N_CUSTOMERS = 1_000
N_PRODUCTS = 30
N_SALES = 6_000
N_CAMPAIGN_SENDS = 7_000
N_REVIEWS = 2_500
N_WEBSITE_VISITS = 10_000

CATEGORIES = ["Skincare", "Fitness", "Home", "Accessories", "Wellness"]

TRAFFIC_SOURCES = [
    "organic_search",
    "paid_search",
    "social",
    "email",
    "direct",
    "referral",
]

TRAFFIC_SOURCE_WEIGHTS = [0.27, 0.19, 0.18, 0.14, 0.16, 0.06]
CUSTOMER_SEGMENTS = ["Value", "Regular", "Premium"]
CUSTOMER_SEGMENT_WEIGHTS = [0.35, 0.48, 0.17]


class Campaign(TypedDict):
    campaign_id: str
    campaign_name: str
    channel: str
    message: str
    start_month: int
    end_month: int


class Customer(TypedDict):
    customer_id: str
    segment: str
    engagement: float
    price_sensitivity: float


class Product(TypedDict):
    product_id: str
    product_name: str
    category: str
    base_price: float
    quality: float
    popularity: float


CAMPAIGNS: list[Campaign] = [
    {
        "campaign_id": "CMP01",
        "campaign_name": "New Year Reset",
        "channel": "email",
        "message": "Start fresh with practical favorites.",
        "start_month": 1,
        "end_month": 2,
    },
    {
        "campaign_id": "CMP02",
        "campaign_name": "Spring Refresh",
        "channel": "ads",
        "message": "Refresh your routine for spring.",
        "start_month": 3,
        "end_month": 4,
    },
    {
        "campaign_id": "CMP03",
        "campaign_name": "Member Picks",
        "channel": "email",
        "message": "Popular picks selected for you.",
        "start_month": 5,
        "end_month": 6,
    },
    {
        "campaign_id": "CMP04",
        "campaign_name": "Summer Essentials",
        "channel": "ads",
        "message": "Simple essentials for warmer days.",
        "start_month": 6,
        "end_month": 8,
    },
    {
        "campaign_id": "CMP05",
        "campaign_name": "Back to Routine",
        "channel": "email",
        "message": "Get back into your everyday rhythm.",
        "start_month": 8,
        "end_month": 9,
    },
    {
        "campaign_id": "CMP06",
        "campaign_name": "Autumn Edit",
        "channel": "ads",
        "message": "Discover this season's useful upgrades.",
        "start_month": 9,
        "end_month": 10,
    },
    {
        "campaign_id": "CMP07",
        "campaign_name": "Early Holiday",
        "channel": "email",
        "message": "A head start on thoughtful gifting.",
        "start_month": 11,
        "end_month": 11,
    },
    {
        "campaign_id": "CMP08",
        "campaign_name": "Holiday Highlights",
        "channel": "ads",
        "message": "Explore customer favorites this holiday.",
        "start_month": 11,
        "end_month": 12,
    },
]


rng = random.Random(SEED)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TOTAL_DAYS = (END_DATE - START_DATE).days + 1


def logistic(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def random_date() -> date:
    return START_DATE + timedelta(days=rng.randrange(TOTAL_DAYS))


def random_date_between_months(start_month: int, end_month: int) -> date:
    valid_dates = []

    for i in range(TOTAL_DAYS):
        d = START_DATE + timedelta(days=i)

        if start_month <= d.month <= end_month:
            valid_dates.append(d)

    return rng.choice(valid_dates)


def seasonal_multiplier(d: date) -> float:
    yearly_wave = 0.06 * math.sin(2 * math.pi * (d.timetuple().tm_yday - 220) / 365)

    holiday_effect = 0.08 if d.month in (11, 12) else 0

    return 1 + yearly_wave + holiday_effect


customers: list[Customer] = []
for i in range(1, N_CUSTOMERS + 1):
    segment = rng.choices(CUSTOMER_SEGMENTS, weights=CUSTOMER_SEGMENT_WEIGHTS, k=1)[0]
    customers.append(
        {
            "customer_id": f"C{i:05d}",
            "segment": segment,
            "engagement": rng.uniform(-0.7, 0.7),
            "price_sensitivity": rng.uniform(-0.6, 0.6),
        }
    )
customers_by_id = {customer["customer_id"]: customer for customer in customers}
customer_ids = list(customers_by_id)


product_adjectives = [
    "Daily",
    "Pure",
    "Urban",
    "Essential",
    "Bright",
    "Active",
    "Calm",
    "Modern",
]
product_nouns = ["Serum", "Bottle", "Mat", "Lamp", "Bag", "Cream", "Band", "Organizer"]

products: list[Product] = []
for i in range(1, N_PRODUCTS + 1):
    category = CATEGORIES[(i - 1) % len(CATEGORIES)]
    adjective = product_adjectives[(i - 1) % len(product_adjectives)]
    noun = product_nouns[(i * 3) % len(product_nouns)]
    products.append(
        {
            "product_id": f"P{i:03d}",
            "product_name": f"{adjective} {noun} {i:02d}",
            "category": category,
            "base_price": round(rng.uniform(12, 110), 2),
            "quality": rng.uniform(-0.5, 0.5),
            "popularity": rng.uniform(0.75, 1.25),
        }
    )

product_weights: list[float] = [product["popularity"] for product in products]


def create_sale(
    customer_id: str,
    product: Product,
    sale_date: date,
    sales_channel: str,
    campaign_send_id: str | None = None,
    visit_id: str | None = None,
) -> dict[str, object]:
    customer = customers_by_id[customer_id]
    quantity_weights = [0.70, 0.21, 0.07, 0.02]
    if customer["segment"] == "Premium":
        quantity_weights = [0.64, 0.24, 0.09, 0.03]
    quantity = rng.choices([1, 2, 3, 4], weights=quantity_weights, k=1)[0]
    discount = rng.choices(
        [0, 0.05, 0.10, 0.15], weights=[0.67, 0.16, 0.12, 0.05], k=1
    )[0]
    seasonal_price_effect = 1 + (seasonal_multiplier(sale_date) - 1) * 0.15
    unit_price = (
        product["base_price"]
        * (1 - discount)
        * seasonal_price_effect
        * rng.uniform(0.98, 1.02)
    )
    unit_price = round(unit_price, 2)
    return {
        "transaction_id": f"T{len(sales_rows) + 1:06d}",
        "customer_id": customer_id,
        "product_id": product["product_id"],
        "product_name": product["product_name"],
        "quantity": quantity,
        "unit_price": unit_price,
        "transaction_total": round(quantity * unit_price, 2),
        "date": sale_date,
        "sales_channel": sales_channel,
        "campaign_send_id": campaign_send_id,
        "visit_id": visit_id,
    }


sales_rows = []
for i in range(1, N_SALES + 1):
    d = random_date()
    customer_id = rng.choice(customer_ids)
    product = rng.choices(products, weights=product_weights, k=1)[0]
    sales_rows.append(create_sale(customer_id, product, d, "other"))

campaign_rows = []
campaign_website_rows = []
for i in range(1, N_CAMPAIGN_SENDS + 1):
    customer_id = rng.choice(customer_ids)
    customer = customers_by_id[customer_id]
    campaign = rng.choice(CAMPAIGNS)
    sent_date = random_date_between_months(
        campaign["start_month"], campaign["end_month"]
    )
    click_score = (
        -2.1
        + 0.55 * customer["engagement"]
        + (0.20 if campaign["channel"] == "email" else 0)
        + (0.15 if sent_date.month in (11, 12) else 0)
        + rng.uniform(-0.15, 0.15)
    )
    clicked = rng.random() < logistic(click_score)
    time_spent = (
        int(max(8, min(3600, rng.lognormvariate(4.5, 0.8)))) if clicked else None
    )
    purchase_score = (
        -3.0
        + 0.50 * customer["engagement"]
        + 1.25
        + (0.15 if sent_date.month in (11, 12) else 0)
        + rng.uniform(-0.15, 0.15)
    )
    purchased = clicked and rng.random() < logistic(purchase_score)
    send_id = f"SEND{i:06d}"
    visit_id = None
    sale = None
    if clicked:
        product = rng.choices(products, weights=product_weights, k=1)[0]
        visit_id = f"V{N_WEBSITE_VISITS + len(campaign_website_rows) + 1:06d}"
        visit_date = min(sent_date + timedelta(days=rng.randint(0, 14)), END_DATE)
        added_to_cart = purchased or rng.random() < logistic(
            -1.55 + 0.45 * customer["engagement"]
        )
        if purchased:
            sale = create_sale(
                customer_id,
                product,
                visit_date,
                "marketing_campaign",
                campaign_send_id=send_id,
                visit_id=visit_id,
            )
            sales_rows.append(sale)
        campaign_website_rows.append(
            {
                "visit_id": visit_id,
                "customer_id": customer_id,
                "visit_date": visit_date,
                "traffic_source": (
                    "email" if campaign["channel"] == "email" else "paid_search"
                ),
                "product_id": product["product_id"],
                "product_viewed": product["product_name"],
                "added_to_cart": added_to_cart,
                "purchased": purchased,
                "time_spent": time_spent,
                "transaction_id": sale["transaction_id"] if sale else None,
                "campaign_send_id": send_id,
            }
        )
    campaign_rows.append(
        {
            "send_id": send_id,
            "campaign_id": campaign["campaign_id"],
            "campaign_name": campaign["campaign_name"],
            "customer_id": customer_id,
            "channel": campaign["channel"],
            "message": campaign["message"],
            "sent_date": sent_date,
            "clicked": clicked,
            "time_spent": time_spent,
            "purchased": purchased,
            "visit_id": visit_id,
            "transaction_id": sale["transaction_id"] if sale else None,
            "amount_purchased": sale["transaction_total"] if sale else None,
        }
    )

website_rows = campaign_website_rows
for i in range(1, N_WEBSITE_VISITS + 1):
    customer_id = rng.choice(customer_ids)
    customer = customers_by_id[customer_id]
    visit_date = random_date()
    source = rng.choices(
        TRAFFIC_SOURCES,
        weights=TRAFFIC_SOURCE_WEIGHTS,
        k=1,
    )[0]
    product = rng.choices(products, weights=product_weights, k=1)[0]
    source_cart_effect = {
        "organic_search": 0.05,
        "paid_search": 0.10,
        "social": -0.05,
        "email": 0.18,
        "direct": 0.08,
        "referral": 0.02,
    }[source]

    cart_score = (
        -1.55
        + 0.55 * customer["engagement"]
        + 0.20 * (product["popularity"] - 1)
        + source_cart_effect
        + 0.30 * (seasonal_multiplier(visit_date) - 1)
        + rng.uniform(-0.20, 0.20)
    )

    added_to_cart = rng.random() < logistic(cart_score)
    source_purchase_effect = {
        "organic_search": 0.02,
        "paid_search": 0.15,
        "social": -0.08,
        "email": 0.14,
        "direct": 0.10,
        "referral": 0.04,
    }[source]
    purchase_score = (
        -2.75
        + 0.45 * customer["engagement"]
        + 1.45 * int(added_to_cart)
        + source_purchase_effect
        + rng.uniform(-0.20, 0.20)
    )
    purchased = rng.random() < logistic(purchase_score)
    visit_id = f"V{i:06d}"
    time_spent = int(
        max(
            5,
            min(
                3600,
                rng.lognormvariate(
                    3.9 + 0.45 * int(added_to_cart) + 0.45 * int(purchased), 0.8
                ),
            ),
        )
    )
    sale = None
    if purchased:
        sale = create_sale(
            customer_id,
            product,
            visit_date,
            "website",
            visit_id=visit_id,
        )
        sales_rows.append(sale)
    website_rows.append(
        {
            "visit_id": visit_id,
            "customer_id": customer_id,
            "visit_date": visit_date,
            "traffic_source": source,
            "product_id": product["product_id"],
            "product_viewed": product["product_name"],
            "added_to_cart": added_to_cart,
            "purchased": purchased,
            "time_spent": time_spent,
            "transaction_id": sale["transaction_id"] if sale else None,
            "campaign_send_id": None,
        }
    )

sales_df = pl.DataFrame(sales_rows, infer_schema_length=None)
campaigns_df = pl.DataFrame(campaign_rows, infer_schema_length=None)
website_df = pl.DataFrame(website_rows, infer_schema_length=None)


review_texts = {
    1: [
        "Absolute rubbish. Fell apart after two days.",
        "one star because zero isnt an option",
        "Do NOT waste your money on this!!!",
        "It broke immediately. customer service was useless too",
        "Worst thing ive bought in ages, honestly furious",
        "looks cheap feels cheap and it doesnt even work",
        "Returned it. Complete scam at this price.",
        "I hate this so much. unusable",
        "Arrived damaged and the replacement was also damaged. wow.",
        "Not as described at all. seriously disappointing",
        "broke the first time i used it lol",
        "Awful. Just awful. Save yourself the headache",
        "The smell is HORRIBLE and it did nothing",
        "Three weeks and already in the bin",
        "paid for quality got dollar store junk",
        "Would give negative stars if i could!!!",
        "Doesnt fit, doesnt work, waste of time",
        "I regret buying this every single day",
    ],
    2: [
        "Not great. I expected more for the price.",
        "It works sometimes, which is not really good enough",
        "meh. feels flimsy",
        "The photos made it look much better than it is",
        "Had to return it. Shame because the idea was good",
        "Too expensive for something this average",
        "Not terrible but definitely not buying again",
        "Arrived late and the packaging was a mess",
        "It technically works but i dont like using it",
        "Quality control seems all over the place",
        "Kinda disappointing tbh",
        "Fine for a week then started acting weird",
        "Would be ok at half the price",
        "Was expecting better. sadly no",
        "Not worth the hassle",
    ],
    3: [
        "It does the job. Nothing special.",
        "Fine i guess, a few annoying bits",
        "Average product, average price, average experience",
        "Works like it should but doesnt wow me",
        "Some things are good and some are just odd",
        "I have mixed feelings about this one",
        "Not bad! Not great either",
        "Useful enough, though the instructions were confusing",
        "Looks nice but the quality feels pretty basic",
        "Okay for now. Lets see how long it lasts",
        "Could be better but could be worse",
        "I use it, just dont love it",
        "Decent once you figure out how it works",
        "Works as expected, which is fine",
        "Nothing to complain about, nothing to rave about",
    ],
    4: [
        "Really useful and nicer than I expected.",
        "Good value, gets used every day",
        "Looks great and works well so far",
        "Happy with it. delivery was quick too",
        "Solid little product, would recommend",
        "Love the design, one small issue with the packaging",
        "Better than the one I replaced",
        "Works perfectly for what I needed",
        "Easy to use and feels pretty sturdy",
        "Nice quality. took a star off for the price",
        "I reach for this all the time now",
        "Pretty impressed tbh",
        "Does exactly what it says on the tin",
        "Bought one for my sister too",
        "Good product, instructions could be clearer",
    ],
    5: [
        "Absolutely obsessed with this. Best purchase this year!!!",
        "I LOVE IT. already ordered another one",
        "Genuinely life changing for my morning routine",
        "Perfect in every way. no notes",
        "This is SO good why did i wait so long",
        "Best thing ever. I tell everyone about it",
        "Exceeded every expectation by a mile",
        "Finally something that actually works!!!",
        "10/10 would buy again and again",
        "I use it constantly and it still looks brand new",
        "Obsessed. obsessed. obsessed.",
        "My new favorite thing in the house",
        "Incredible quality for the price, wow",
        "Bought as a gift and now keeping it for myself lol",
        "This deserves more than five stars",
        "A+++ no complaints at all",
        "Best purchase ive made in months, hands down",
        "Love love love it. works like a dream",
    ],
}

extra_comments = [
    "shipping was quick",
    "packaging was a bit much",
    "saw it on instagram first",
    "my friend has one too",
    "looked different in the photos",
    "delivery took forever",
    "bought it during the sale",
    "customer support got back to me fast",
]
typos = {
    "because": "becuase",
    "definitely": "definately",
    "received": "recieved",
    "really": "realy",
    "does not": "doesnt",
    "would not": "wouldnt",
}


def vary_review_text(text: str) -> str:
    if rng.random() < 0.24:
        text += " " + rng.choice(extra_comments)
    if rng.random() < 0.16:
        for correct, typo in typos.items():
            if correct in text.lower():
                text = text.replace(correct, typo, 1)
                break
    if rng.random() < 0.20:
        text = text.translate(str.maketrans("", "", string.punctuation))
    style = rng.random()
    if style < 0.12:
        text = text.lower()
    elif style < 0.17:
        text = text.upper()
    elif style < 0.23:
        text = text.rstrip(".") + rng.choice(["!!", "...", "??"])
    return text


review_rows = []
review_sales = rng.sample(sales_rows, k=N_REVIEWS)
for i, sale in enumerate(review_sales, start=1):
    customer = customers_by_id[sale["customer_id"]]
    product = next(
        product for product in products if product["product_id"] == sale["product_id"]
    )
    rating_score = (
        3.65 + product["quality"] + 0.15 * customer["engagement"] + rng.gauss(0, 1.0)
    )
    if rng.random() < 0.18:
        rating = rng.choice([1, 5])
    else:
        rating = max(1, min(5, round(rating_score)))
    max_review_lag = (END_DATE - sale["date"]).days
    review_date = sale["date"] + timedelta(days=rng.randint(0, min(180, max_review_lag)))
    review_rows.append(
        {
            "review_id": f"R{i:06d}",
            "transaction_id": sale["transaction_id"],
            "customer_id": sale["customer_id"],
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "rating": rating,
            "review_text": vary_review_text(rng.choice(review_texts[rating])),
            "review_date": review_date,
        }
    )
reviews_df = pl.DataFrame(review_rows)

sales_df.write_csv(OUTPUT_DIR / "sales.csv")
campaigns_df.write_csv(OUTPUT_DIR / "marketing_campaigns.csv")
reviews_df.write_csv(OUTPUT_DIR / "product_reviews.csv")
website_df.write_csv(OUTPUT_DIR / "website_analytics.csv")
