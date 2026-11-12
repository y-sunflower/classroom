sales = [
    {"product": "Notebook", "quantity": 3, "unit_price": 5.00},
    {"product": "Pen", "quantity": 10, "unit_price": 2.00},
    {"product": "Backpack", "quantity": 2, "unit_price": 35.00},
    {"product": "Folder", "quantity": 4, "unit_price": 3.50},
]

for x in sales:
    if x["unit_price"] * x["quantity"] > 20:
        print(f"{x['product']}: {x['unit_price']}euros")
        print(f"{x['product']}: {x['unit_price']}euros")
x
