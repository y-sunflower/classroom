import math
import random
import string
from calendar import monthrange
from datetime import date, timedelta
from pathlib import Path
from typing import TypedDict

import polars as pl

SEED = 42
OUTPUT_DIR = Path("docs/kedge_data_analytics_and_AI/data")
START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)
CURRENCY_CODE = "EUR"
N_CUSTOMERS = 1_000
N_PRODUCTS = 30
N_OTHER_SALE_ATTEMPTS = 6_000
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
    message_a: str
    message_b: str
    start_month: int
    end_month: int
    promotion_code: str


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
    opening_stock: int
    monthly_restock_quantity: int


PROMOTION_RATES = {
    "RESET10": 0.10,
    "SPRING10": 0.10,
    "MEMBER15": 0.15,
    "SUMMER5": 0.05,
    "ROUTINE10": 0.10,
    "AUTUMN5": 0.05,
    "GIFT10": 0.10,
    "HOLIDAY15": 0.15,
    "WELCOME5": 0.05,
    "LOYALTY10": 0.10,
    "WEEKEND15": 0.15,
}

GENERIC_PROMOTIONS = [
    {
        "promotion_code": "WELCOME5",
        "description": "Welcome offer",
    },
    {
        "promotion_code": "LOYALTY10",
        "description": "Loyalty offer",
    },
    {
        "promotion_code": "WEEKEND15",
        "description": "Weekend offer",
    },
]


CAMPAIGNS: list[Campaign] = [
    {
        "campaign_id": "CMP01",
        "campaign_name": "New Year Reset",
        "channel": "email",
        "message_a": "Start fresh with practical favorites for your everyday routine.",
        "message_b": "Make your new-year routine easier with practical everyday picks.",
        "start_month": 1,
        "end_month": 2,
        "promotion_code": "RESET10",
    },
    {
        "campaign_id": "CMP02",
        "campaign_name": "Spring Refresh",
        "channel": "ads",
        "message_a": "Refresh your routine with useful picks for spring.",
        "message_b": "Find simple upgrades to make your spring routine feel new.",
        "start_month": 3,
        "end_month": 4,
        "promotion_code": "SPRING10",
    },
    {
        "campaign_id": "CMP03",
        "campaign_name": "Member Picks",
        "channel": "email",
        "message_a": "Explore the favorites selected for our members.",
        "message_b": "See which practical picks other members use every day.",
        "start_month": 5,
        "end_month": 6,
        "promotion_code": "MEMBER15",
    },
    {
        "campaign_id": "CMP04",
        "campaign_name": "Summer Essentials",
        "channel": "ads",
        "message_a": "Get ready for warmer days with simple essentials.",
        "message_b": "Make summer routines easier with useful everyday essentials.",
        "start_month": 6,
        "end_month": 8,
        "promotion_code": "SUMMER5",
    },
    {
        "campaign_id": "CMP05",
        "campaign_name": "Back to Routine",
        "channel": "email",
        "message_a": "Get back into your everyday rhythm with practical picks.",
        "message_b": "Find simple favorites to make your routine easier again.",
        "start_month": 8,
        "end_month": 9,
        "promotion_code": "ROUTINE10",
    },
    {
        "campaign_id": "CMP06",
        "campaign_name": "Autumn Edit",
        "channel": "ads",
        "message_a": "Discover useful upgrades for the autumn season.",
        "message_b": "Refresh your everyday setup with our autumn favorites.",
        "start_month": 9,
        "end_month": 10,
        "promotion_code": "AUTUMN5",
    },
    {
        "campaign_id": "CMP07",
        "campaign_name": "Early Holiday",
        "channel": "email",
        "message_a": "Get a head start on thoughtful holiday gifts.",
        "message_b": "Find useful gifts before the holiday rush begins.",
        "start_month": 11,
        "end_month": 11,
        "promotion_code": "GIFT10",
    },
    {
        "campaign_id": "CMP08",
        "campaign_name": "Holiday Highlights",
        "channel": "ads",
        "message_a": "Explore customer favorites for the holiday season.",
        "message_b": "Make holiday routines easier with these practical picks.",
        "start_month": 11,
        "end_month": 12,
        "promotion_code": "HOLIDAY15",
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
            "opening_stock": rng.randint(80, 130),
            "monthly_restock_quantity": rng.randint(17, 24),
        }
    )

product_weights: list[float] = [product["popularity"] for product in products]
products_by_id = {product["product_id"]: product for product in products}


def choose_generic_promotion() -> str | None:
    if rng.random() < 0.22:
        return rng.choice(GENERIC_PROMOTIONS)["promotion_code"]
    return None


def create_sale(
    customer_id: str,
    product: Product,
    sale_date: date,
    sales_channel: str,
    stock_available: int,
    promotion_code: str | None,
    campaign_send_id: str | None = None,
    visit_id: str | None = None,
) -> dict[str, object]:
    customer = customers_by_id[customer_id]
    quantity_options = [1, 2, 3, 4]
    quantity_weights = [0.70, 0.21, 0.07, 0.02]
    if customer["segment"] == "Premium":
        quantity_weights = [0.64, 0.24, 0.09, 0.03]
    available_options = [
        quantity for quantity in quantity_options if quantity <= stock_available
    ]
    available_weights = [
        weight
        for quantity, weight in zip(quantity_options, quantity_weights, strict=True)
        if quantity <= stock_available
    ]
    quantity = rng.choices(available_options, weights=available_weights, k=1)[0]
    discount_rate = PROMOTION_RATES.get(promotion_code, 0.0)
    list_unit_price = product["base_price"]
    unit_price = round(list_unit_price * (1 - discount_rate), 2)
    gross_total = round(quantity * list_unit_price, 2)
    transaction_total = round(quantity * unit_price, 2)
    discount_amount = round(gross_total - transaction_total, 2)

    returned_quantity = 0
    return_date = None
    return_status = "none"
    days_until_year_end = (END_DATE - sale_date).days
    if days_until_year_end > 0 and rng.random() < 0.06:
        return_date = sale_date + timedelta(
            days=rng.randint(1, min(30, days_until_year_end))
        )
        if quantity == 1 or rng.random() < 0.65:
            returned_quantity = quantity
            return_status = "full"
        else:
            returned_quantity = rng.randint(1, quantity - 1)
            return_status = "partial"
    refund_amount = round(returned_quantity * unit_price, 2)
    return {
        "transaction_id": f"T{len(sales_rows) + 1:06d}",
        "currency_code": CURRENCY_CODE,
        "customer_id": customer_id,
        "product_id": product["product_id"],
        "product_name": product["product_name"],
        "quantity": quantity,
        "list_unit_price": list_unit_price,
        "unit_price": unit_price,
        "discount_rate": discount_rate,
        "promotion_code": promotion_code,
        "gross_total": gross_total,
        "discount_amount": discount_amount,
        "transaction_total": transaction_total,
        "return_status": return_status,
        "returned_quantity": returned_quantity,
        "return_date": return_date,
        "refund_amount": refund_amount,
        "net_total": round(transaction_total - refund_amount, 2),
        "date": sale_date,
        "sales_channel": sales_channel,
        "campaign_send_id": campaign_send_id,
        "visit_id": visit_id,
    }


inventory_events = []
for _ in range(1, N_OTHER_SALE_ATTEMPTS + 1):
    product = rng.choices(products, weights=product_weights, k=1)[0]
    inventory_events.append(
        {
            "event_type": "offline_sale",
            "sales_channel": "other",
            "event_date": random_date(),
            "customer_id": rng.choice(customer_ids),
            "product": product,
            "promotion_code": choose_generic_promotion(),
            "tie_breaker": rng.random(),
        }
    )

campaign_rows = []
campaign_website_rows = []
message_assignments: dict[tuple[str, str], str] = {}
for i in range(1, N_CAMPAIGN_SENDS + 1):
    customer_id = rng.choice(customer_ids)
    customer = customers_by_id[customer_id]
    campaign = rng.choice(CAMPAIGNS)
    sent_date = random_date_between_months(
        campaign["start_month"], campaign["end_month"]
    )
    assignment_key = (campaign["campaign_id"], customer_id)
    if assignment_key not in message_assignments:
        message_assignments[assignment_key] = rng.choice(["A", "B"])
    message_variant = message_assignments[assignment_key]
    message = campaign[f"message_{message_variant.lower()}"]
    click_score = (
        -2.1
        + 0.55 * customer["engagement"]
        + (0.20 if campaign["channel"] == "email" else 0)
        + (0.15 if sent_date.month in (11, 12) else 0)
        + (0.22 if message_variant == "B" else 0)
        + rng.uniform(-0.15, 0.15)
    )
    clicked = rng.random() < logistic(click_score)
    time_spent = (
        int(max(8, min(3600, rng.lognormvariate(4.5, 0.8)))) if clicked else None
    )
    purchase_intent = False
    if clicked:
        purchase_score = (
            -3.0
            + 0.50 * customer["engagement"]
            + 1.25
            + (0.15 if sent_date.month in (11, 12) else 0)
            + (0.18 if message_variant == "B" else 0)
            + rng.uniform(-0.15, 0.15)
        )
        purchase_intent = rng.random() < logistic(purchase_score)
    send_id = f"SEND{i:06d}"
    visit_id = None
    campaign_row = {
        "send_id": send_id,
        "campaign_id": campaign["campaign_id"],
        "campaign_name": campaign["campaign_name"],
        "experiment_id": f"AB-{campaign['campaign_id']}",
        "message_variant": message_variant,
        "customer_id": customer_id,
        "channel": campaign["channel"],
        "message": message,
        "sent_date": sent_date,
        "promotion_code": campaign["promotion_code"],
        "discount_rate": PROMOTION_RATES[campaign["promotion_code"]],
        "currency_code": CURRENCY_CODE,
        "clicked": clicked,
        "time_spent": time_spent,
        "purchased": False,
        "visit_id": None,
        "transaction_id": None,
        "amount_purchased": None,
    }
    if clicked:
        product = rng.choices(products, weights=product_weights, k=1)[0]
        visit_id = f"V{N_WEBSITE_VISITS + len(campaign_website_rows) + 1:06d}"
        visit_date = min(sent_date + timedelta(days=rng.randint(0, 14)), END_DATE)
        added_to_cart = purchase_intent or rng.random() < logistic(
            -1.55 + 0.45 * customer["engagement"]
        )
        website_row = {
            "visit_id": visit_id,
            "customer_id": customer_id,
            "visit_date": visit_date,
            "traffic_source": (
                "email" if campaign["channel"] == "email" else "paid_search"
            ),
            "product_id": product["product_id"],
            "product_viewed": product["product_name"],
            "product_available": None,
            "added_to_cart": added_to_cart,
            "purchased": False,
            "time_spent": time_spent,
            "promotion_code": campaign["promotion_code"],
            "transaction_id": None,
            "campaign_send_id": send_id,
        }
        campaign_row["visit_id"] = visit_id
        campaign_website_rows.append(website_row)
        inventory_events.append(
            {
                "event_type": "website_visit",
                "sales_channel": "marketing_campaign",
                "event_date": visit_date,
                "customer_id": customer_id,
                "product": product,
                "promotion_code": campaign["promotion_code"],
                "purchase_intent": purchase_intent,
                "campaign_send_id": send_id,
                "visit_id": visit_id,
                "campaign_row": campaign_row,
                "website_row": website_row,
                "tie_breaker": rng.random(),
            }
        )
    campaign_rows.append(campaign_row)

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
    purchase_intent = rng.random() < logistic(purchase_score)
    visit_id = f"V{i:06d}"
    time_spent = int(
        max(
            5,
            min(
                3600,
                rng.lognormvariate(
                    3.9 + 0.45 * int(added_to_cart) + 0.45 * int(purchase_intent), 0.8
                ),
            ),
        )
    )
    promotion_code = choose_generic_promotion()
    website_row = {
        "visit_id": visit_id,
        "customer_id": customer_id,
        "visit_date": visit_date,
        "traffic_source": source,
        "product_id": product["product_id"],
        "product_viewed": product["product_name"],
        "product_available": None,
        "added_to_cart": added_to_cart,
        "purchased": False,
        "time_spent": time_spent,
        "promotion_code": promotion_code,
        "transaction_id": None,
        "campaign_send_id": None,
    }
    website_rows.append(website_row)
    inventory_events.append(
        {
            "event_type": "website_visit",
            "sales_channel": "website",
            "event_date": visit_date,
            "customer_id": customer_id,
            "product": product,
            "promotion_code": promotion_code,
            "purchase_intent": purchase_intent,
            "visit_id": visit_id,
            "website_row": website_row,
            "tie_breaker": rng.random(),
        }
    )

sales_rows = []
remaining_stock = {
    product["product_id"]: product["opening_stock"] for product in products
}
current_month = 1
for event in sorted(
    inventory_events, key=lambda item: (item["event_date"], item["tie_breaker"])
):
    while current_month < event["event_date"].month:
        current_month += 1
        for product in products:
            remaining_stock[product["product_id"]] += product[
                "monthly_restock_quantity"
            ]

    product = event["product"]
    product_id = product["product_id"]
    stock_available = remaining_stock[product_id]
    if event["event_type"] == "website_visit":
        website_row = event["website_row"]
        website_row["product_available"] = stock_available > 0
        if stock_available == 0:
            website_row["added_to_cart"] = False

    sale = None
    purchase_intent = event.get("purchase_intent", True)
    if stock_available > 0 and purchase_intent:
        sale = create_sale(
            event["customer_id"],
            product,
            event["event_date"],
            event["sales_channel"],
            stock_available,
            event["promotion_code"],
            campaign_send_id=event.get("campaign_send_id"),
            visit_id=event.get("visit_id"),
        )
        sales_rows.append(sale)
        remaining_stock[product_id] -= sale["quantity"]

    if event["event_type"] == "website_visit":
        website_row["purchased"] = sale is not None
        if sale:
            website_row["transaction_id"] = sale["transaction_id"]
        campaign_row = event.get("campaign_row")
        if campaign_row is not None:
            campaign_row["purchased"] = sale is not None
            if sale:
                campaign_row["transaction_id"] = sale["transaction_id"]
                campaign_row["amount_purchased"] = sale["transaction_total"]

sales_df = pl.DataFrame(sales_rows, infer_schema_length=None)
campaigns_df = pl.DataFrame(campaign_rows, infer_schema_length=None)
website_df = pl.DataFrame(website_rows, infer_schema_length=None)
products_df = pl.DataFrame(
    [
        {
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "list_price": product["base_price"],
            "currency_code": CURRENCY_CODE,
            "opening_stock": product["opening_stock"],
            "monthly_restock_quantity": product["monthly_restock_quantity"],
        }
        for product in products
    ]
)

promotion_rows = [
    {
        "promotion_code": promotion["promotion_code"],
        "description": promotion["description"],
        "discount_rate": PROMOTION_RATES[promotion["promotion_code"]],
        "active_from": START_DATE,
        "active_to": END_DATE,
        "campaign_id": None,
    }
    for promotion in GENERIC_PROMOTIONS
]
for campaign in CAMPAIGNS:
    promotion_end = min(
        date(2025, campaign["end_month"], monthrange(2025, campaign["end_month"])[1])
        + timedelta(days=14),
        END_DATE,
    )
    promotion_rows.append(
        {
            "promotion_code": campaign["promotion_code"],
            "description": f"{campaign['campaign_name']} offer",
            "discount_rate": PROMOTION_RATES[campaign["promotion_code"]],
            "active_from": date(2025, campaign["start_month"], 1),
            "active_to": promotion_end,
            "campaign_id": campaign["campaign_id"],
        }
    )
promotions_df = pl.DataFrame(promotion_rows)


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
    product = products_by_id[sale["product_id"]]
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
products_df.write_csv(OUTPUT_DIR / "products.csv")
promotions_df.write_csv(OUTPUT_DIR / "promotions.csv")
