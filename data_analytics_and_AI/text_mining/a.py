products = [
    {"name": "Notebook", "price": 5.50},
    {"name": "Backpack", "price": 35.00},
    {"name": "Pen", "price": 2.00},
    {"name": "Calculator", "price": 18.50},
    {"name": "Folder", "price": 4.00},
]

count = 0
for x in products:
    if x["price"] > 10:
        count = count + 1


print(count)
