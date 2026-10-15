---
icon: lucide/code
---

In the next lesson, we'll use **Python**, one of the world most famous programming language. This page introduces the basic ideas you'll need to read and write small Python programs.

!!! warning

      Make sure you installed Positron and uv, [see the guide if not](../definition_of_data_and_ai/setup.md).

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

      Change the message to introduce yourself, save the file, and run it again.

=== "Hint"

      Text that you want Python to display goes inside quotation marks and parentheses: `print("your message")`.

## Read code from top to bottom

Python normally runs each line in order, from the top of the file to the bottom. A comment starts with `#`; Python skips it, so you can leave notes for people reading your code.

=== "Example"

      ```python
      # I can write anything here!
      print("Preparing data")
      print("Let's get started")
      ```

=== "Exercise"

      Write two `print` statements: one that displays `Sales data` and one that displays `Ready to explore`.

=== "Hint"

      Put each message in its own `print(...)` call. The line order determines which message appears first.

## Store values in variables

A variable gives a name to a value so you can use it later. Use `=` to assign a value. Python works out the type from the value: for example, `str` for text, `int` for whole numbers, and `float` for decimal numbers.

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

      Create variables for a product name, its quantity, and its unit price. Print each value.

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

      Calculate the total for five items that cost 2.25 each. Store it in `total` and print it.

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

      Use an f-string to print a sentence with a product name and its price.

=== "Hint"

      Start the text with `f` and put each variable name inside `{}`. For example: `f"The price is {unit_price}"`.

## Keep several values in a list

A list stores values in order. Write its values between square brackets and separate them with commas. Python counts positions from zero, so the first item is at index `0`.

=== "Example"

      ```python
      products = ["Notebook", "Pen", "Folder"]

      print(products[0])
      print(len(products))
      ```

=== "Exercise"

      Make a list with three product names. Print the second name and the number of names in the list.

=== "Hint"

      The second item has index `1`. Use `len(your_list)` to count the items.

## Make a decision

An `if` statement runs code only when a condition is true. Use `else` for the alternative. The indented lines belong to the condition above them; indentation is part of Python's syntax.

=== "Example"

      ```python
      total = 24

      if total > 20:
          print("Large order")
      else:
          print("Small order")
      ```

=== "Exercise"

      Print `In stock` when `quantity` is greater than zero; otherwise print `Out of stock`.

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

      Loop through a list of three prices and print each price.

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

      Write a function named `greet` that takes a `name` and prints a greeting. Call it with your name.

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

      Add another sale to the list, then change the condition so the program displays sales of 20 euros or more.

=== "Hint"

      Each sale is a dictionary with keys `product` and `total`. Change `> 10` to `>= 20` to include sales that equal 20.
