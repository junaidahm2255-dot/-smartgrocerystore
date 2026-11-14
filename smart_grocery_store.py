# Smart Grocery Store Management System
# This application manages products, stock, customer sales, and store reports.

# Return a valid positive integer entered by the user.
def get_positive_integer(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("Invalid input. Please enter a whole number greater than zero.")


# Return a valid non-negative integer entered by the user.
def get_non_negative_integer(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Invalid input. Please enter zero or a positive whole number.")


# Return a valid positive price entered by the user.
def get_positive_price(prompt):
    while True:
        try:
            price = float(input(prompt).strip())
            if price > 0:
                return price
            print("Price must be greater than zero.")
        except ValueError:
            print("Invalid price. Please enter a number, such as 250 or 99.50.")


# Find and return a product by its ID, or None if it does not exist.
def find_product_by_id(products, product_id):
    for product in products:
        if product["id"] == product_id:
            return product
    return None


# Display one product in a consistent readable format.
def display_product(product):
    print("-" * 58)
    print(f"Product ID   : {product['id']}")
    print(f"Product Name : {product['name']}")
    print(f"Category     : {product['category']}")
    print(f"Price        : Rs. {product['price']:.2f}")
    print(f"Available Stock: {product['stock']}")
    print("-" * 58)


# Ask for product details and add a new product if its ID is unique.
def add_new_product(products):
    print("\n--- Add New Product ---")
    product_id = get_positive_integer("Enter product ID: ")

    if find_product_by_id(products, product_id) is not None:
        print("A product with this ID already exists. Product was not added.")
        return

    while True:
        name = input("Enter product name: ").strip()
        if name:
            break
        print("Product name cannot be empty.")

    while True:
        category = input("Enter product category: ").strip()
        if category:
            break
        print("Category cannot be empty.")

    price = get_positive_price("Enter product price (Rs.): ")
    stock = get_non_negative_integer("Enter available stock: ")

    new_product = {
        "id": product_id,
        "name": name.title(),
        "category": category.title(),
        "price": price,
        "stock": stock
    }

    products.append(new_product)
    print(f"{new_product['name']} was added successfully.")


# Display every product currently stored in the products list.
def view_all_products(products):
    print("\n--- All Products ---")
    if not products:
        print("No products are currently available.")
        return

    print(f"{'ID':<8}{'Name':<20}{'Category':<15}{'Price (Rs.)':>12}{'Stock':>8}")
    print("-" * 63)
    for product in products:
        print(
            f"{product['id']:<8}"
            f"{product['name']:<20}"
            f"{product['category']:<15}"
            f"{product['price']:>12.2f}"
            f"{product['stock']:>8}"
        )


# Search for a product using its numeric ID or its name.
def search_product(products):
    print("\n--- Search Product ---")
    search_value = input("Enter product ID or product name: ").strip()

    if not search_value:
        print("Search value cannot be empty.")
        return

    if search_value.isdigit():
        product = find_product_by_id(products, int(search_value))
        if product:
            display_product(product)
        else:
            print("Product not found.")
        return

    matches = []
    for product in products:
        if search_value.lower() in product["name"].lower():
            matches.append(product)

    if matches:
        for product in matches:
            display_product(product)
    else:
        print("Product not found.")


# Add stock to a product or replace its available stock quantity.
def update_product_stock(products):
    print("\n--- Update Product Stock ---")
    product_id = get_positive_integer("Enter product ID: ")
    product = find_product_by_id(products, product_id)

    if product is None:
        print("Product not found.")
        return

    print(f"Current stock of {product['name']}: {product['stock']}")
    print("1. Add stock")
    print("2. Set available stock")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        quantity = get_positive_integer("Enter quantity to add: ")
        product["stock"] += quantity
    elif choice == "2":
        quantity = get_non_negative_integer("Enter new available stock: ")
        product["stock"] = quantity
    else:
        print("Invalid option. Stock was not changed.")
        return

    print(f"Updated stock of {product['name']}: {product['stock']}")


# Complete a sale only when the product exists and enough stock is available.
def process_customer_sale(products, sales_records):
    print("\n--- Process Customer Sale ---")
    product_id = get_positive_integer("Enter product ID: ")
    product = find_product_by_id(products, product_id)

    if product is None:
        print("Product not found. Sale cannot be processed.")
        return

    quantity = get_positive_integer("Enter purchase quantity: ")

    if quantity > product["stock"]:
        print(
            f"Insufficient stock. Available stock is {product['stock']} "
            f"and requested quantity is {quantity}."
        )
        return

    total_amount = product["price"] * quantity
    product["stock"] -= quantity

    sale = {
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity_sold": quantity,
        "total_amount": total_amount
    }
    sales_records.append(sale)

    print("\n========== PURCHASE SUMMARY ==========")
    print(f"Product       : {product['name']}")
    print(f"Product ID    : {product['id']}")
    print(f"Quantity Sold : {quantity}")
    print(f"Unit Price    : Rs. {product['price']:.2f}")
    print(f"Total Amount  : Rs. {total_amount:.2f}")
    print(f"Remaining Stock: {product['stock']}")
    print("Sale completed successfully.")
    print("======================================")


# Display all completed sales stored in the sales records list.
def view_sales_records(sales_records):
    print("\n--- Sales Records ---")
    if not sales_records:
        print("No sales have been recorded yet.")
        return

    print(f"{'Product ID':<13}{'Product Name':<20}{'Quantity':>10}{'Total (Rs.)':>15}")
    print("-" * 58)
    for sale in sales_records:
        print(
            f"{sale['product_id']:<13}"
            f"{sale['product_name']:<20}"
            f"{sale['quantity_sold']:>10}"
            f"{sale['total_amount']:>15.2f}"
        )


# Calculate and display the store's inventory and sales summary.
def generate_store_report(products, sales_records):
    print("\n========== SMART GROCERY STORE REPORT ==========")

    total_products = len(products)
    total_stock = sum(product["stock"] for product in products)
    total_transactions = len(sales_records)
    total_revenue = sum(sale["total_amount"] for sale in sales_records)

    print(f"Total number of products : {total_products}")
    print(f"Total available stock    : {total_stock}")
    print(f"Total sales transactions : {total_transactions}")
    print(f"Total revenue generated  : Rs. {total_revenue:.2f}")

    print("\nProducts with stock below 5 units:")
    low_stock_products = [product for product in products if product["stock"] < 5]
    if low_stock_products:
        for product in low_stock_products:
            print(f"{product['name']} (ID: {product['id']}) - Stock: {product['stock']}")
    else:
        print("No products have stock below 5 units.")

    if products:
        highest_price_product = max(products, key=lambda product: product["price"])
        lowest_price_product = min(products, key=lambda product: product["price"])

        print("\nProduct with the highest price:")
        print(
            f"{highest_price_product['name']} "
            f"(ID: {highest_price_product['id']}) - "
            f"Rs. {highest_price_product['price']:.2f}"
        )

        print("\nProduct with the lowest price:")
        print(
            f"{lowest_price_product['name']} "
            f"(ID: {lowest_price_product['id']}) - "
            f"Rs. {lowest_price_product['price']:.2f}"
        )
    else:
        print("\nNo products are available to compare prices.")

    print("=" * 52)


# Display the main menu and return the user's selected option.
def display_menu():
    print("\n" + "=" * 40)
    print("       SMART GROCERY STORE SYSTEM")
    print("=" * 40)
    print("1. Add New Product")
    print("2. View All Products")
    print("3. Search Product")
    print("4. Update Product Stock")
    print("5. Process Customer Sale")
    print("6. View Sales Records")
    print("7. Generate Store Report")
    print("8. Exit")
    return input("\nEnter your choice: ").strip()


def main():
    # These lists keep product and sales information while the program is running.
    products = [
        {"id": 101, "name": "Milk", "category": "Dairy", "price": 250.00, "stock": 20},
        {"id": 102, "name": "Bread", "category": "Bakery", "price": 120.00, "stock": 15},
        {"id": 103, "name": "Rice", "category": "Grains", "price": 300.00, "stock": 10}
    ]
    sales_records = []

    while True:
        choice = display_menu()

        if choice == "1":
            add_new_product(products)
        elif choice == "2":
            view_all_products(products)
        elif choice == "3":
            search_product(products)
        elif choice == "4":
            update_product_stock(products)
        elif choice == "5":
            process_customer_sale(products, sales_records)
        elif choice == "6":
            view_sales_records(sales_records)
        elif choice == "7":
            generate_store_report(products, sales_records)
        elif choice == "8":
            print("Thank you for using the Smart Grocery Store System. Goodbye!")
            break
        else:
            print("Invalid menu choice. Please select a number from 1 to 8.")


if __name__ == "__main__":
    main()
