import json
import os

def load_products():
    file_path = os.path.join(os.path.dirname(__file__), 'products.json')
    if not os.path.exists(file_path):
        print("Error: products.json file not found.")
        return []
    with open(file_path, 'r') as f:
        products = json.load(f)
    return products

def display_products(products):
    if not products:
        print("No products available.")
    else:
        print("Available Products:")
        for product in products:
            print(f"{product['id']}. {product['name']} - ${product['price']} (Stock: {product['stock']}, Discount: {product['discount']}%)")

def search_product(products):
    search_term = input("Enter product name or ID to search: ")
    for product in products:
        if product['name'].lower() == search_term.lower() or str(product['id']) == search_term:
            print("Product Found:")
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']}")
            print(f"Stock: {product['stock']}")
            print(f"Discount: {product['discount']}%")
            return
    print("Product not found.")

def add_to_cart(products, cart):
    try:
        product_id = int(input("Enter product ID to add to cart: "))
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Error: Please enter a valid number.")
        return

    for product in products:
        if product['id'] == product_id:
            if product['stock'] >= quantity:
                cart.append({'name': product['name'], 'original_price': product['price'], 'discount': product['discount'], 'quantity': quantity})
                product['stock'] -= quantity
                print(f"Added {quantity} {product['name']}s to your cart.")
            else:
                print("Insufficient stock.")
            return
    print("Product not found.")

def view_cart(cart):
    if not cart:
        print("Your cart is empty!")
        return
    print("Cart:")
    subtotal = 0
    for i, item in enumerate(cart):
        final_price = item['original_price'] * (1 - item['discount'] / 100)
        subtotal += final_price * item['quantity']
        print(f"{i+1}. {item['name']} - ${item['original_price']} each, Discount: {item['discount']}%, Final Price: ${final_price:.2f} each, Quantity: {item['quantity']}, Total: ${final_price * item['quantity']:.2f}")
    print(f"Cart Subtotal: ${subtotal:.2f}")

def remove_from_cart(cart, products):
    try:
        product_id = int(input("Enter product ID to remove from cart: "))
    except ValueError:
        print("Error: Please enter a valid number.")
        return

    for i, item in enumerate(cart):
        for product in products:
            if product["id"] == product_id and item["name"] == product["name"]:
                cart.pop(i)
                product["stock"] += item["quantity"]
                print(f"Removed {item['name']} from your cart.")
                return
    print("Product not found in cart.")

def checkout(cart, customer_name):
    if not cart:
        print("Your cart is empty! Nothing to checkout.")
        return

    subtotal = sum(item['original_price'] * (1 - item['discount'] / 100) * item['quantity'] for item in cart)
    tax = subtotal * 0.1
    total = subtotal + tax
    
    print(f"\nCheckout Summary for {customer_name}:")
    for item in cart:
        final_price = item['original_price'] * (1 - item['discount'] / 100)
        print(f"{item['name']} - ${item['original_price']} with {item['discount']}% discount → ${final_price:.2f} x {item['quantity']} = ${final_price * item['quantity']:.2f}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax (10%): ${tax:.2f}")
    print(f"Total Payable: ${total:.2f}")

    
    receipt_file = 'receipt.json'
    if os.path.exists(receipt_file):
        with open(receipt_file, 'r') as f:
            try:
                receipts = json.load(f) 
                if not isinstance(receipts, list):
                    receipts = [] 
            except json.JSONDecodeError:
                receipts = []  
    else:
        receipts = []


    new_receipt = {
        "customer_name": customer_name,
        "cart": cart,
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "total": round(total, 2)
    }
    receipts.append(new_receipt)

  
    with open(receipt_file, 'w') as f:
        json.dump(receipts, f, indent=4)

    print("Receipt saved in 'receipt.json'.")
    cart.clear()

def main():
    customer_name = input("Enter your name: ") 
    products = load_products()
    cart = []
    while True:
        print(f"\nWelcome, {customer_name}! E-commerce Shopping System")
        print("1. Display available products")
        print("2. Search for a product")
        print("3. Add products to cart")
        print("4. View cart")
        print("5. Remove items from cart")
        print("6. Checkout and generate receipt")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            display_products(products)
        elif choice == "2":
            search_product(products)
        elif choice == "3":
            add_to_cart(products, cart)
        elif choice == "4":
            view_cart(cart)
        elif choice == "5":
            remove_from_cart(cart, products)
        elif choice == "6":
            checkout(cart, customer_name)
        elif choice == "7":
            print(f"Exiting... Thank you for shopping, {customer_name}!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
