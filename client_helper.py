import socket
import json
import threading
import select
import time
import os
import sys
import re
from config import DEFAULT_IP, DEFAULT_PORT, BUFFER_SIZE

# --- Black Box Overview of Client Helper Code ---

# 1. Connect to Server
# Function: `connect_to_server(ip=DEFAULT_IP, port=DEFAULT_PORT)`
# - Creates a socket connection to the server using the provided IP and port.
# - Returns the client socket if successful or exits on failure.

# 2. Welcome Page
# Function: `welcome_page()`
# - Displays options for logging in, registering, or quitting the application.

# 3. Send Data to Server
# Function: `send_data(data)`
# - Sends a JSON-formatted request to the server.
# - Receives and parses the server's response.
# - Handles errors in connection or invalid responses.

# 4. Login
# Function: `login(username)`
# - Prompts the user for a username and password.
# - Sends login credentials to the server.
# - Stores the current user ID globally if successful.

# 5. Register
# Function: `register()`
# - Collects user details for registration, including email, username, name, and password.
# - Validates the email format.
# - Sends registration details to the server and displays the server's response.

# 6. Main Menu
# Function: `main_menu()`
# - Displays a list of main menu options for actions like viewing products, adding products, or logging out.

# 7. View Products
# Function: `view_products()`
# - Sends a request to the server to retrieve all products in the market.
# - Displays the products and returns dictionaries for product names and owners.

# 8. Add Product
# Function: `add_product(owner)`
# - Collects product details (name, price, description) from the user.
# - Sends these details to the server to add a new product to the marketplace.

# 9. View Owner's Products
# Function: `view_owner(owner_name, product_id)`
# - Requests and displays all products belonging to a specific owner.

# 10. Initiate Communication
# Function: `want_communication(username, owner_name)`
# - Asks if the user wants to communicate with a product owner.
# - Sends a request to the server to initiate communication if the user agrees.

# 11. Clear Screen
# Function: `clear_screen()`
# - Clears the console output based on the operating system.

# 12. Get Balance
# Function: `get_balance(user_id)`
# - Requests the user's account balance from the server.

# 13. Add to Cart
# Function: `add_to_cart(cart, product_id, quantity, price)`
# - Adds a product to the user's shopping cart.

# 14. View Portfolio
# Function: `view_portfolio(username)`
# - Requests and displays the user's portfolio, including balance, owned products, and transaction history.

# 15. Receipt
# Function: `Reciept(cart)`
# - Calculates and returns the total cost of items in the cart.

# 16. Add Funds
# Function: `add_funds(user_id)`
# - Prompts the user to input a deposit amount.
# - Sends a request to the server to add funds to the user's account.

# 17. Buy Product
# Function: `buy_product(user_id, product_id, quantity)`
# - Sends a request to the server to purchase a specified quantity of a product.

# 18. Ask Client List
# Function: `askClientList()`
# - Retrieves a list of notifications or connected users from the server.



























# Add at the top of the file
current_user_id = None

def connect_to_server(ip=DEFAULT_IP, port=DEFAULT_PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip, port))
        print("Connected Successfully")
        return client
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

#client = connect_to_server()

def welcome_page():
      print("***Welcome to AUBoutique***\n")
      print("1. LOGIN\n")
      print("2. REGISTER\n")
      print("3. QUIT")

def send_data(data): 
    try:
        json_data = json.dumps(data)
        client.sendall(json_data.encode('utf-8'))
        response = client.recv(BUFFER_SIZE).decode()
        received_data = json.loads(response)
        return received_data
    except socket.error as e:
        print(f"Connection error: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid response from server: {e}")
        return {"status": "error", "message": "Invalid server response"}

def login(username):
    user_name = input("Enter your username: ")
    password = input("Enter your password: ")
    login_data = {
        "action": "LOGIN",
        "username": user_name,
        "password": password
    }
    response = send_data(login_data)
    print("Server response:", response)
    
    if response.get("status") == "success":
        username[0] = user_name
        # Store user_id globally
        global current_user_id
        current_user_id = response.get("user_id")
        return True
    return False

def register(): 
    def validate_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)
        
    while True:
        email = input("\nEnter your email: ")
        if not validate_email(email):
            print("Invalid email format")
            continue
        break
        
    user_name = input("\nCreate a username: ")
    name = input("\nEnter your full name: ")
    password = input("\nCreate a password: ")
    
    user_data = {
        "action": "REGISTER",
        "name": name,
        "email": email,
        "username": user_name,
        "password": password
    }
    response = send_data(user_data)
    print("Server response:", response)
    if response.get("status") == "success":
        print("\nRegistration successful! Please login.")
        return True
    else:
        print(f"\nRegistration failed: {response.get('message')}")
        return False

def main_menu():
    print("---Main Menu---\n")
    print("1. View Products\n")
    print("2. View products by owner\n")
    print("3. Add Product\n")
    print("4. Buy Product\n")
    print("5. View Portfolio\n")
    print("6. Add Funds\n")
    print("7. Text\n")
    print("8. Logout\n")

def view_products():
    view_data = {
        "action": "VIEW_PRODUCTS"
    }
    response = send_data(view_data)
    products = response.get("products", [])  # Default to empty list if no products
    
    product_dict = {}
    owner_dict = {}
    
    if products:
        print("\nAvailable Products:")
        for i, prod in enumerate(products, 1):
            print(f"\n{i}. Name: {prod.get('name')} (ID: {prod.get('product_id')})")
            print(f"Price: ${prod.get('price')}")
            print(f"Owner: {prod.get('owner')}")
            print(f"Description: {prod.get('description')}")
            
            # Store in dictionaries
            product_dict[f"Name {i}"] = (prod.get('name'), prod.get('product_id'))
            owner_dict[f"Owner {i}"] = prod.get('owner')
    else:
        print("No products available")
        
    return product_dict, owner_dict


import base64
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import requests


def add_product(owner):
    '''
    Add a new product to the marketplace.
    '''
    try:
        # Get product details
        name = input("\nName of the product: ")
        while True:
            price = input("\nPrice of the product: ")
            try:
                price = float(price)
                break
            except ValueError:
                print("Please enter a valid number for price")
        
        # Get user_id from login response instead of asking user
        description = input("\nDescription of the product: ")
        
        # Prepare data to send to the server
        add_data = {
            "action": "ADD_PRODUCT",
            "name": name,
            "price": price,
            "description": description,
            "owner": owner,  # username
            "picture_path": None  # For now, we'll skip image handling
        }
        
        # Send to server
        response = send_data(add_data)
        
        # Handle response
        if response.get("status") == "success":
            print("\nProduct added successfully!")
            print(f"Product ID: {response.get('product_id')}")
        else:
            print(f"\nFailed to add product: {response.get('message')}")
            
    except Exception as e:
        print(f"\nError adding product: {e}")

def view_owner(owner_name,product_id):
    request = {
        "action" : "VIEW_OWNER",
        "owner_name" : owner_name,
        "product_id" : product_id
    }
    response = send_data(request)
    owner_products = response.get("owner_products", {}).get(owner_name)
    if owner_products:
        print("\n Products by ", owner_name, ": ")
        for i, product in enumerate(owner_products,1):
            print(f" {i}. Product name: {product.get('name')}\n")
            print(f"Product price: {product.get('price')}\n")
            print(f"Product description: {product.get('description')}\n")

    else:
        print(f"{owner_name} has no products for sale")


    # Sample response structure from the server:
    #Message=
    # {
    #     "status": "success",  # or "error" for request outcome
    #     "products": [  # List of all products available
    #         {"name": "Textbook A", "price": "20", "owner": "user1", "description": "Intro to Math"},
    #         {"name": "Handmade Vase", "price": "15", "owner": "user2", "description": "Ceramic vase"}
    #     ],
    #     "owner_products": {  # Dictionary of products organized by owner
    #         "user1": [
    #             {"name": "Textbook A", "price": "20", "description": "Intro to Math"}
    #         ],
    #         "user2": [
    #             {"name": "Handmade Vase", "price": "15", "description": "Ceramic vase"}
    #         ]
    #     }
    # }

def want_communication(username, owner_name):
    b = input("Contact owner? y/n ")
    if b=="y":
        INITIATE_COMMUNICATION = {
            "action":"INITIATE_COMMUNICATION",
            "sender":username,
            "receiver":owner_name
        }
        send_data(INITIATE_COMMUNICATION)
    return b=="y"

def clear_screen():
    # Cross-platform clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

def get_balance(user_id):

    balance_req = {
        "action" : "GET_BALANCE",
        "user_id" : user_id
    }
    response = send_data(balance_req)


    return response.get("balance")

def add_to_cart(cart, product_id, quantity, price):
    cart.append({"product_id" : product_id, "quantity": quantity, "price": price})

def view_portfolio(username):
    portfolio_request = {
        "action": "VIEW_PORTFOLIO",
        "username": username,
    }
    response = send_data(portfolio_request)
    
    if response.get("status") != "success":
        print(f"Error viewing portfolio: {response.get('message')}")
        return
    
    balance = response.get("balance", 0)
    owned = response.get("owned_products", [])
    transactions = response.get("transactions", [])
    
    print(f"\nBalance: {balance}")
    print("\nOwned Products:")
    for product in owned:
        print(f"\n Name: {product['name']}, Quantity: {product['quantity']}, Price: {product['price']}, Product_id: {product['product_id']}")
    
    print("\nTransactions:")
    for transaction in transactions:
        if transaction['buyer_id'] == current_user_id:
            action = "Bought"
        elif transaction['seller_id'] == current_user_id:
            action = "Sold"
        else:
            action = "Unknown"  # This should not happen if data is consistent

        print(f"\n {action} {transaction['quantity']} of {transaction['product_name']} for {transaction['sale_price']} on {transaction['date']}")

def Reciept(cart):
    sum = 0
    for product in cart:
        sum+= product['quantity']* product['price']
    return sum

def add_funds(user_id):
    try:
        amount = float(input("\nDeposit amount to your balance: "))
        if amount <= 0:
            print("\nAmount must be positive!")
            return
        add_funds_request = {
            "action": "ADD_FUNDS",
            "user_id": user_id,
            "amount": amount
        }
        response = send_data(add_funds_request)
        if response.get("status") == "success":
            print(f"\nFunds added successfully! New Balance: {response.get('new_balance')}")
        else:
            print(f"\nAn error occurred: {response.get('message')}")
    except ValueError:
        print("\nInvalid amount")

def buy_product(user_id, product_id, quantity):

    BUY_PRODUCTS = { 
        "action": "BUY_PRODUCTS",
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity
    }

    response = send_data(BUY_PRODUCTS)

    if response.get('status') == 'success':
        print("Thank you for using AUBOUTIQUE! Please pass by the AUB Post Office to claim your purchase.")
        print("Purchase ID number:", response.get('purchase_id'))
    elif response.get('status') == 'error':
        print(f"\n{response.get('message')}")

def askClientList(sender,client):
    RETRIEVE_NOTIFICATIONS = {
        "action":"RETRIEVE_NOTIFICATIONS",
        "sender":sender
    }
    data = RETRIEVE_NOTIFICATIONS
    try:
        json_data = json.dumps(data)
        client.sendall(json_data.encode('utf-8'))
        response = client.recv(BUFFER_SIZE).decode()
        response = json.loads(response)
    except socket.error as e:
        print(f"Connection error: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid response from server: {e}")
        return {"status": "error", "message": "Invalid server response"}

    print("Asked for notification. Got:", response)
    return response.get("content")

def askAllClientList(sender,client):
    RETRIEVE_ALL_ONLINE = {
        "action":"RETRIEVE_ALL_ONLINE",
        "sender":sender
    }
    data = RETRIEVE_ALL_ONLINE
    try:
        json_data = json.dumps(data)
        client.sendall(json_data.encode('utf-8'))
        response = client.recv(BUFFER_SIZE).decode()
        response = json.loads(response)
    except socket.error as e:
        print(f"Connection error: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid response from server: {e}")
        return {"status": "error", "message": "Invalid server response"}

    print(response)
    return response.get("content")
