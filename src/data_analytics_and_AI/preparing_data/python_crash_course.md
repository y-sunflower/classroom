---
icon: lucide/brush-cleaning
---

In the next lesson, we'll use **Python**, one of the world's most famous programming languages. This page introduces the basic ideas you'll need to read and write small Python programs.

!!! warning

      - Make sure you've installed Positron and uv ([see the guide if not](../setup.md)).
      - **The goal isn't to make you a programming expert**! Instead, I want you to grasp the core concepts of manipulating data with code, learn to do basic operations, and then learn how to use AI to do them for you.

## Get ready

We'll write Python in Positron and use `uv` to run it. `uv` can create a starter script and run it without adding any packages.

=== "Example"

      - Open a new folder in Positron.
      - Create a `main.py` file
      - Open `main.py`, replace its contents with the code below, and save it.
      - Either select the code and hit "Run", or open a terminal and run `uv run main.py`

      ```python
      print("Hello, Python!")
      ```

=== "Exercise"

      Replace the message with one that introduces you. Save `main.py` and run `uv run main.py` again to see the change.

      ```python
      print("Hello, Python!")
      ```

=== "Hint"

      Text that you want Python to display goes inside quotation marks and parentheses: `print("your message")`.

## Read code from top to bottom

Python **runs each line in order**, from the top of the file to the bottom. A comment starts with `#`; Python skips it, so you can leave notes for people reading your code.

=== "Example"

      ```python
      # I can write anything here!
      print("Preparing data")
      print("Let's get started")
      ```

=== "Exercise"

      Run this starter code. Add a second `print` statement below the first so it also displays `Ready to explore`, then run it again.

      ```python
      # Python runs these lines from top to bottom
      print("Sales data")
      # TODO: display "Ready to explore"
      ```

=== "Hint"

      Put each message in its own `print(...)` call. The line order determines which message appears first.

## Store values in variables

A variable gives a name to a value so you can use it later. Use `=` to assign a value.

=== "Example"

      ```python
      product_name = "Notebook"
      quantity = 3
      unit_price = 4.50

      print(product_name)
      print(quantity)
      print(unit_price)
      ```

=== "Exercise"

      Change the three values to describe a product of your choice. Run the code and check that it prints the values you assigned.

      ```python
      product_name = "Notebook"
      quantity = 3
      unit_price = 4.50

      print(product_name)
      print(quantity)
      print(unit_price)
      ```

=== "Hint"

      Put text in quotes, and write numbers without quotes. Choose clear names such as `product_name` and `unit_price`.

## Calculate with values

Python can calculate with numbers. The basic operators are `+` for addition, `-` for subtraction, `*` for multiplication, and `/` for division. Store a calculation in a variable to use its result later.

=== "Example"

      ```python
      quantity = 3
      unit_price = 4.50
      line_total = quantity * unit_price

      print(line_total)
      ```

=== "Exercise"

      Complete the calculation so `total` is the price of five items. Run the code and check the result.

      ```python
      quantity = 5
      unit_price = 2.25

      # TODO: multiply quantity by unit_price and store the result in total
      total = 0
      print(total)
      ```

=== "Hint"

      Multiply the quantity by the unit price with `*`: `5 * 2.25`.

## Work with text

Text values are called **strings**. You can join strings with `+`, or use an f-string to insert values into a sentence. An f-string starts with `f` before the opening quote; put each variable inside braces.

=== "Example"

      ```python
      product_name = "Notebook"
      quantity = 3
      print(f"We sold {quantity} {product_name}s.")
      ```

=== "Exercise"

      Change the values, then replace the TODO with an f-string that prints the product name and price. Run the code to check the sentence.

      ```python
      product_name = "Notebook"
      unit_price = 4.50

      # TODO: print a sentence that includes both values
      ```

=== "Hint"

      Start the text with `f` and put each variable name inside `{}`. For example: `f"The price is {unit_price}"`.

## Python's basic types

Every value has a **type**, which determines what you can do with it. The main types you'll use here are `int` for whole numbers, `float` for decimal numbers, `str` for text, and `bool` for either `True` or `False`. Use `type(...)` to inspect a value's type.

Numbers can be added to other numbers, including an `int` and a `float`. Strings can be joined with other strings, but **Python won't add a number to a string**. Convert a number with `str(...)` when you want to include it in text. Comparisons such as `>` produce a boolean, and `and`, `or`, and `not` combine boolean values.

=== "Example"

      ```python
      quantity = 3                 # int
      unit_price = 4.50            # float
      product_name = "Notebook"    # str
      is_available = True          # bool

      total = quantity * unit_price
      message = "Total: " + str(total)
      can_purchase = is_available and quantity > 0

      print(type(quantity))
      print(type(unit_price))
      print(type(product_name))
      print(type(is_available))
      print(message)
      print(can_purchase)
      ```

!!! warning

      `"Total: " + total` raises a `TypeError` because `total` is a number and `"Total: "` is text. Convert the number with `str(total)`, or use an f-string such as `f"Total: {total}"`.

!!! tip

      Python has many other types, some of which are described below.

## Keep several values in a list

A list stores values in order. Write its values between square brackets and separate them with commas. Python counts positions from zero, so the first item is at index `0`.

=== "Example"

      ```python
      products = ["Notebook", "Pen", "Folder"]

      print(products[0])
      print(len(products))
      ```

=== "Exercise"

      Add a third product to this list. Then print the second name and the number of names. Run the code to check both results.

      ```python
      products = ["Notebook", "Pen"]

      # TODO: add another product
      # TODO: print the second product
      # TODO: print how many products are in the list
      ```

=== "Hint"

      The second item has index `1`. Use `len(your_list)` to count the items.

!!! question

      In your opinion, how can you get **the last element of a list** (assuming you don't know its length)?

## Store related values in a dictionary

A dictionary stores values under named keys. Write each key and value as a pair inside braces. Use a key in square brackets to look up its value. Dictionaries are useful when each record has named fields, such as a product and its price.

=== "Example"

      ```python
      sale = {
            "product": "Notebook",
            "quantity": 3,
            "unit_price": 4.50
      }

      print(sale["product"])
      print(sale["quantity"] * sale["unit_price"])
      ```

=== "Exercise"

      Run this starter code. Change the product and quantity, then add a print statement that looks up and displays the unit price. Run it again to check your changes.

      ```python
      sale = {"product": "Notebook", "quantity": 3, "unit_price": 4.50}

      print(sale["product"])
      print(sale["quantity"])
      # TODO: print the unit price using its key
      ```

=== "Hint"

      Look up a value with the key in square brackets, for example `sale["unit_price"]`.

## Make a decision

An `if` statement runs code only **when a condition is true**. Use `else` for the alternative. The ==indented lines== belong to the condition above them; indentation is part of Python's syntax.

=== "Example"

      ```python
      total = 24

      if total > 20:
          print("Large order")
      else:
          print("Small order")
      ```

=== "Exercise"

      Run this code several times. The quantity is randomly chosen each time between 0 and 5, as the comment explains. Add an `if` and `else` so it prints `In stock` when the quantity is greater than zero and `Out of stock` otherwise. Run it several more times and observe both outcomes.

      ```python
      import random

      # Pick a new whole number from 0 to 5 each time you run the program
      quantity = random.randint(0, 5)
      print(f"Quantity: {quantity}")

      # TODO: print "In stock" when quantity is above 0
      # TODO: otherwise print "Out of stock"
      ```

=== "Hint"

      Compare `quantity` with zero using `>`. Indent the `print` lines underneath `if` and `else`.

## Repeat work with a loop

A `for` loop runs its indented code once for each item in a sequence, such as a list. The loop variable takes the value of the current item each time.

=== "Example"

      ```python
      products = ["Notebook", "Pen", "Folder"]

      for product in products:
          print(product)
      ```

=== "Exercise"

      Run the starter code. Add a `for` loop that prints each price in the list, then run it again and check that all three prices appear.

      ```python
      prices = [2.25, 4.50, 1.75]

      # TODO: loop through prices and print each one
      ```

=== "Hint"

      Use `for price in prices:` and indent the `print(price)` line beneath it.

## Reuse steps with a function

A function is a named set of steps. Define one with `def`, give it a name and any inputs in parentheses, then indent its body. Call the function by writing its name with parentheses.

=== "Example"

      ```python
      def calculate_total(quantity, unit_price):
          return quantity * unit_price

      total = calculate_total(3, 4.50)
      print(total)
      ```

=== "Exercise"

      Replace `pass` with a print statement that greets the name. Change the name in the function call, then run the code to see your greeting.

      ```python
      def greet(name):
          pass  # TODO: print a greeting that includes name

      greet("Sam")
      ```

=== "Hint"

      Define it with `def greet(name):`, then put `print(f"Hello, {name}!")` on an indented line. Call it with `greet("Sam")`.

## Put the pieces together

The same building blocks work together in a program. Here, a loop visits each sale, a condition keeps larger sales, and an f-string displays the result. In the next lesson, Polars will help us do similar work with columns and many rows of data.

=== "Example"

      ```python
      sales = [
          {"product": "Notebook", "total": 24.00},
          {"product": "Pen", "total": 6.00},
          {"product": "Folder", "total": 18.00},
      ]

      for sale in sales:
          if sale["total"] > 10:
              print(f"{sale['product']}: {sale['total']} euros")
      ```

=== "Exercise"

      Run the starter code and note which sales appear. Add another sale to the list, then change the condition from `> 10` to `>= 20`. Run it again and check that only sales of 20 euros or more appear.

      ```python
      sales = [
          {"product": "Notebook", "total": 24.00},
          {"product": "Pen", "total": 6.00},
          {"product": "Folder", "total": 18.00},
      ]

      for sale in sales:
          if sale["total"] > 10:
              print(f"{sale['product']}: {sale['total']} euros")
      ```

=== "Hint"

      Each sale is a dictionary with keys `product` and `total`. Change `> 10` to `>= 20` to include sales that equal 20.

## Going further

!!! info

      Those are exercises to make practices the concepts seen before. Using AI wouldn't make sense here, but **feel free to use it** to give you hints and explanations of things you don't understand.

=== "Calculate a shopping cart"

      You have a list of product prices. Write a program that:

      1. Prints each price.
      2. Calculates the total price of all products.
      3. Prints the total using an f-string.
      4. Calculates the average price of a product.

      Starter code:

      ```py
      prices = [12.50, 8.00, 15.75, 4.25]
      
      # TODO: calculate the total using a loop
      
      # TODO: calculate the average price
      
      # TODO: display the total and average
      ```

      Expected result:

      ```
      Total: 40.5 euros
      Average price: 10.125 euros
      ```

=== "Find expensive products"

      You have a small collection of products. Write a program that:

      1. Displays the name and price of each product.
      2. Displays only products costing more than 10 euros.
      3. Counts how many products cost more than 10 euros.
      4. Prints that count.

      Starter code:

      ```py
      products = [
            {"name": "Notebook", "price": 5.50},
            {"name": "Backpack", "price": 35.00},
            {"name": "Pen", "price": 2.00},
            {"name": "Calculator", "price": 18.50},
            {"name": "Folder", "price": 4.00},
      ]

      # TODO: display all products

      # TODO: find products costing more than 10 euros

      # TODO: display the number of expensive products
      ```

      Expected result for expensive products:

      ```
      Backpack: 35.0 euros
      Calculator: 18.5 euros
      Number of expensive products: 2
      ```

=== "Analyze sales data"

      You have a small sales dataset. Your goal is to write a program that produces a simple sales report.

      1. Create a function `calculate_total(quantity, unit_price)` that returns the total amount of a sale.
      2. Use a loop to calculate the total for each sale.
      3. Calculate the total revenue across all sales.
      4. Display only sales worth at least 20 euros.
      5. Print the total revenue at the end.

      Starter code:

      ```py
      sales = [
            {"product": "Notebook", "quantity": 3, "unit_price": 5.00},
            {"product": "Pen", "quantity": 10, "unit_price": 2.00},
            {"product": "Backpack", "quantity": 2, "unit_price": 35.00},
            {"product": "Folder", "quantity": 4, "unit_price": 3.50},
      ]

      def calculate_total(quantity, unit_price):
            pass

      # TODO: loop through the sales

      # TODO: calculate the total for each sale

      # TODO: display sales worth at least 20 euros

      # TODO: calculate and display total revenue
      ```

      Expected result:

      ```
      Pen: 20.0 euros
      Backpack: 70.0 euros
      Total revenue: 119.0 euros
      ```

      These exercises build toward the next lesson: working with tabular data using Polars. Students will have already practiced selecting records, calculating values, filtering by conditions, and aggregating results using plain Python.