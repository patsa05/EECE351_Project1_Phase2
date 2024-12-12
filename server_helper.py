import json
import sqlite3
import hashlib
import threading
import time
from datetime import datetime, timedelta
from functools import lru_cache
from database import DatabasePool
from config import DATABASE_NAME, BUFFER_SIZE

# Initialize a database connection pool for efficient management of connections
db_pool = DatabasePool(DATABASE_NAME)


# Helper function to send JSON responses to clients
def send_response(response, connection):
    """
    Encodes and sends a JSON response to the client.
    :param response: Dictionary to be sent as a JSON object.
    :param connection: Client's connection object.
    """
    try:
        json_response = json.dumps(response)  # Convert dictionary to JSON string
        connection.sendall(json_response.encode('utf-8'))  # Send response
    except Exception as e:
        print(f"Error sending response: {e}")


# Function to hash passwords securely
def hash_password(password):
    """
    Hashes a password using SHA-256.
    :param password: The plain text password.
    :return: Hashed password as a hexadecimal string.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# Handles user registration requests
def register_server(request):
    """
    Registers a new user in the database.
    :param request: Dictionary containing user details (username, password, email, name).
    :return: A dictionary with the status of the operation.
    """
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

            # Extract user data from the request
            username = request.get('username')
            password = request.get('password')
            email = request.get('email')
            name = request.get('name')

            # Check if username already exists
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                return {"status": "error", "message": "Username already exists"}

            # Hash the password and insert the new user
            hashed_password = hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, password, name, email_address, balance, online)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, hashed_password, name, email, 0.0, False))

            conn.commit()  # Save changes
            return {"status": "success", "message": "Registration successful"}

    except Exception as e:
        print(f"Registration error: {e}")
        return {"status": "error", "message": f"Registration failed: {str(e)}"}


# Handles user login requests
def login(username, password):
    """
    Verifies user credentials for login.
    :param username: The username provided by the user.
    :param password: The plain text password provided by the user.
    :return: A dictionary with the status of the login attempt.
    """
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

            # Retrieve user data from the database
            cursor.execute("""
                SELECT user_id, password FROM users 
                WHERE username = ?
            """, (username,))
            user = cursor.fetchone()

            if not user:
                return {"status": "error", "message": "User not found"}

            # Verify the password
            stored_password = user[1]
            if hash_password(password) == stored_password:
                return {
                    "status": "success",
                    "message": "Login successful",
                    "user_id": user[0],
                    "username": username

                }
            else:
                return {"status": "error", "message": "Invalid password"}

    except Exception as e:
        print(f"Login error: {e}")
        return {"status": "error", "message": "Login failed"}


# Fetches all products available for purchase
def view_all_products():
    """
    Retrieves all products with a quantity greater than zero.
    :return: A dictionary containing the list of available products.
    """
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

            # Fetch product details
            cursor.execute("""
                SELECT p.product_id, p.name, p.price, u.username, p.description, p.quantity
                FROM products p
                JOIN users u ON p.user_id = u.user_id
                WHERE p.quantity > 0
            """)

            products = cursor.fetchall()
            product_list = [{
                "product_id": p[0],
                "name": p[1],
                "price": p[2],
                "owner": p[3],
                "description": p[4],
                "quantity" : p[5]
            } for p in products]

            return {
                "status": "success",
                "products": product_list
            }

    except Exception as e:
        print(f"Error fetching products: {e}")
        return {"status": "error", "message": f"Could not fetch products: {str(e)}"}

def view_owner_products(owner_name, product_id=None):
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

            # Construct the base SQL query
            query = """
                SELECT p.product_id, p.name, p.price, u.username, p.description, p.quantity
                FROM products p
                JOIN users u ON p.user_id = u.user_id
                WHERE lower(u.username) = lower(?) AND p.quantity > 0
            """
            params = [owner_name]

            # Add condition for specific product_id if provided
            if product_id is not None:
                query += " AND p.product_id = ?"
                params.append(product_id)

            cursor.execute(query, params)
            products = cursor.fetchall()

            # Format the product list
            owner_products = [{
                "product_id": p[0],
                "name": p[1],
                "price": p[2],
                "owner": p[3],
                "description": p[4],
                "quantity" : p[5]
            } for p in products]

            return {
                "status": "success",
                "owner_products": {owner_name: owner_products}

            }

    except Exception as e:
        print(f"Error fetching products for owner '{owner_name}': {e}")
        return {"status": "error", "message": f"Could not fetch products: {str(e)}"}



# Adds a product to the database
def add_product_to_db(request):
    response = {"status": "error", "message": ""}
    """
    Adds a new product to the database.
    :param request: Dictionary containing product details.
    :return: A dictionary with the status of the operation.
    """
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

            # Extract product data
            name = request.get('name')
            price = request.get('price')
            owner = request.get('owner')  # The username of the product owner
            print(f"Got owner: {owner}")
            description = request.get('description')
            picture = request.get('picture_path')
            if not owner:
                response["message"] = "Owner username is missing"
                return response
            print(f"Got owner: {owner}")
            # Get user ID from the username
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (owner,))
            result = cursor.fetchone()
            if not result:
                response["message"] = f"User '{owner}' does not exist"
                return response

            user_id = result[0]

            # Insert the product into the database
            cursor.execute("""
                INSERT INTO products (user_id, name, picture, price, description, quantity)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, name, picture, price, description, 1))

            product_id = cursor.lastrowid
            conn.commit()

            return {
                "status": "success",
                "message": "Product added successfully",
                "product_id": product_id
            }

    except Exception as e:
        print(f"Error adding product: {e}")
        return {"status": "error", "message": f"Failed to add product: {str(e)}"}




# Handles incoming client requests and communication with the server
def handle_client(connection, address, socket_username_array=[], message_queue=[],  usernames_to_ip_port = []):
    # Helper function to clean up the connection upon termination
    def cleanup_connection():
        # If the user was logged in, mark them offline in the database
        if current_username:
            cursor.execute("UPDATE users SET ONLINE = FALSE WHERE username = ?", (current_username,))
            db.commit()
        # Close the connection and remove it from the active connections array
        connection.close()
        for item in socket_username_array:
            if item[0] == connection:
                socket_username_array.remove(item)
                break

    try:
        current_username = None  # Tracks the username of the currently connected client
        db = sqlite3.connect(DATABASE_NAME)  # Connect to the database
        cursor = db.cursor()  # Cursor for executing database queries
        print(f"\nReceived connection from: {address}")

        while True:
            print(socket_username_array)
            try:
                # Receive a request from the client
                request = connection.recv(BUFFER_SIZE).decode('utf-8')
                if not request:
                    break  # Exit loop if no data is received

                # Parse the received request as JSON
                parsed_request = json.loads(request)
                action = parsed_request.get("action")  # Determine the action requested by the client
                print(parsed_request)
                # Handle specific actions requested by the client
                if action == "REGISTER":
                    response = register_server(parsed_request)  # Register a new user

                elif action == "LOGIN":
                    
                    response = login(parsed_request.get("username"), parsed_request.get("password"))
                    if response.get("status") == "success":
                        current_username = parsed_request.get("username")
                        # Link the username with the connection in the active connections array
                        for item in socket_username_array:
                            if item[0] == connection:
                                item[1] = current_username
                                break
                    print(socket_username_array)
                elif action == "VIEW_PRODUCTS":
                    response = view_all_products()  # View all available products

                elif action == "ADD_PRODUCT":
                    print(f"Handling 'ADD_PRODUCT' action for {address}")
                    response = add_product_to_db(parsed_request)
                    debug_database()  # Debug database for verification

                elif action == "INITIATE_COMMUNICATION":
                    # Handle communication initiation between clients
                    receiver_socket = None
                    for item in socket_username_array:
                        if item[1] == parsed_request.get("receiver"):
                            receiver_socket = item[0]  # Find the receiver's connection socket
                    for item in message_queue:
                        if item[0] == receiver_socket:
                            item[1] += "," + parsed_request["sender"]  # Update message queue
                    response = {"status": "success"}  # Acknowledge communication initiation
                elif action == "RETRIEVE_NOTIFICATIONS":
                    receiver_socket = None
                    for item in socket_username_array:
                        if item[1] == parsed_request.get("sender"):
                            receiver_socket = item[0]  # Find the receiver's connection socket
                    # Retrieve notifications/messages for the client
                    content = ""
                    for item in message_queue:
                        if item[0] == receiver_socket:
                            content = item[1]
                            break
                    response = {"action": "RETRIEVE_NOTIFICATIONS_RESPONSE", "content": content}
                elif action == "RETRIEVE_ALL_ONLINE":
                    receiver_socket = None
                    for item in socket_username_array:
                        if item[1] == parsed_request.get("sender"):
                            receiver_socket = item[0]  # Find the receiver's connection socket
                    content = []
                    for item in socket_username_array:
                        if item[0] != receiver_socket and item[0].fileno() != -1:
                            content.append(item[1])
                    response = {"action": "RETRIEVE_ALL_ONLINE_RESPONSE", "content": content}
                elif action == "IP_PORT_OF_PEER_REQUEST":
                    print(usernames_to_ip_port)
                    for item in usernames_to_ip_port:
                        if item[0] == parsed_request.get("key"):
                            response = {"action": "IP_PORT_OF_PEER_RESPONSE", "value": item[1]}
                            break
                    response = {"action": "IP_PORT_OF_PEER_RESPONSE", "value": ()}    
                elif action == "UPDATE_IP_PORT_ON_SERVER_REQUEST":
                    usernames_to_ip_port.append([parsed_request.get("key"),parsed_request.get("value")])
                    print(usernames_to_ip_port)
                    response = {"action": "UPDATE_IP_PORT_ON_SERVER_RESPONSE"}

                elif action == "TERMINATE":
                    response = {"action": "TERMINATE_RESPONSE"}

                elif action == "VIEW_PORTFOLIO":
                    username = parsed_request.get("username")
                    if not username:
                        response = {"status": "error", "message": "No username provided for VIEW_PORTFOLIO"}
                    else:
                        response = view_portfolio(username)

                elif action == "ADD_FUNDS":
                    user_id = parsed_request.get("user_id")
                    amount = parsed_request.get("amount")
                    if user_id is None or amount is None:
                        response = {"status": "error", "message": "User ID or Amount missing for ADD_FUNDS"}
                    else:
                        response = add_funds(user_id, amount)

                elif action == "BUY_PRODUCTS":
                    user_id = parsed_request.get("user_id")
                    product_id = parsed_request.get("product_id")
                    quantity = parsed_request.get("quantity")
                    free_purchase = parsed_request.get("free_purchase", False)

                    if user_id is None or product_id is None or quantity is None:
                        response = {"status": "error", "message": "Missing parameters for BUY_PRODUCTS"}
                    else:
                        response = process_purchase(user_id, product_id, quantity, free_purchase)

                elif action == "VIEW_OWNER":
                    owner_name = parsed_request.get("owner_name")
                    product_id = parsed_request.get("product_id")
                    if not owner_name:
                        response = {"status": "error", "message": "Owner name missing for VIEW_OWNER"}
                    else:
                        print("Im here i recognize owner name and product_id from frontend")
                        response = view_owner_products(owner_name, product_id)

                elif action == "VIEW_ALL_OWNERS":

                    response = view_all_owners_products()

                else:
                    # Handle unknown actions
                    response = {"status": "error", "message": "Unknown action"}

                # Send the response to the client if applicable
                if response is not None:
                    send_response(response, connection)

            except json.JSONDecodeError:
                # Handle JSON parsing errors
                print("Failed to parse JSON request")
                send_response({"status": "error", "message": "Invalid request format"}, connection)

    except Exception as e:
        # Handle general exceptions
        print(f"Error handling client {address}: {e}")
    finally:
        # Ensure connection cleanup is performed
        cleanup_connection()


def debug_database():
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

            print("\n=== Database Debug Info ===")

            # Fetch and display all users
            cursor.execute("SELECT user_id, username FROM users")
            users = cursor.fetchall()
            print(f"\nUsers ({len(users)}):")
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}")

            # Fetch and display all products
            cursor.execute("SELECT product_id, name, user_id FROM products")
            products = cursor.fetchall()
            print(f"\nProducts ({len(products)}):")
            for product in products:
                print(f"ID: {product[0]}, Name: {product[1]}, User_ID: {product[2]}")

            print("\n=========================")
    except Exception as e:
        # Handle any errors that occur during debugging
        print(f"Debug error: {e}")
def view_portfolio(username):
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

            # Fetch user balance
            cursor.execute("SELECT balance FROM users WHERE username=?", (username,))
            balance_data = cursor.fetchone()
            balance = balance_data[0] if balance_data else 0

            # Fetch products owned by the user
            cursor.execute("""
                SELECT p.product_id, p.name, p.price, p.quantity
                FROM products p
                JOIN users u ON p.user_id = u.user_id
                WHERE u.username=?
            """, (username,))
            owned_products = [{
                "product_id": row[0],
                "name": row[1],
                "price": row[2],
                "quantity": row[3]
            } for row in cursor.fetchall()]

            # Fetch transactions involving the user
            cursor.execute("""
                SELECT t.buyer_id, t.seller_id, p.name, t.quantity, t.sale_price, t.transaction_date
                FROM transactions t
                JOIN products p ON t.product_id = p.product_id
                WHERE t.buyer_id = (SELECT user_id FROM users WHERE username = ?)
                OR t.seller_id = (SELECT user_id FROM users WHERE username = ?)
            """, (username, username))
            transactions = [{
                "buyer_id": row[0],
                "seller_id": row[1],
                "product_name": row[2],
                "quantity": row[3],
                "sale_price": row[4],
                "date": row[5]
            } for row in cursor.fetchall()]

            # Return a detailed portfolio response
            response = {
                "status": "success",
                "balance": balance,
                "owned_products": owned_products,
                "transactions": transactions
            }
            return response

    except Exception as e:
        # Handle errors during portfolio retrieval
        print(f"Error displaying portfolio for {username}: {e}")
        return {"status": "error", "message": "Could not open page"}


def add_funds(user_id, amount):
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

            # Add the specified amount to the user's balance
            cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
            conn.commit()

            # Retrieve the updated balance
            cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            new_balance = cursor.fetchone()[0]

            return {
                "status": "success",
                "message": "Funds added successfully.",
                "new_balance": new_balance
            }
    except Exception as e:
        # Handle errors during the funds addition process
        print(f"Error in add_funds: {e}")
        return {"status": "error", "message": "An error occurred while adding funds"}
def view_all_owners_products():
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
              SELECT u.username, p.product_id, p.name, p.description, p.quantity
              FROM products p
              JOIN users u ON p.user_id = u.user_id
              WHERE p.quantity > 0
              ORDER BY u.username
            """)
            rows = cursor.fetchall()

            owners_dict = {}
            for r in rows:
                owner = r[0]
                if owner not in owners_dict:
                    owners_dict[owner] = []
                owners_dict[owner].append({
                    "product_id": r[1],
                    "name": r[2],
                    "description": r[3],
                    "quantity": r[4]
                })

            return {"status": "success", "owners": owners_dict}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def process_purchase(user_id, product_id, quantity, free_purchase=False):
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

            # Retrieve product details (price, quantity, seller_id)
            cursor.execute("SELECT price, quantity, user_id FROM products WHERE product_id = ?", (product_id,))
            product = cursor.fetchone()
            if not product:
                return {"status": "error", "message": "Product not found"}

            price, available_quantity, seller_id = product

            # Check if the requested quantity is available
            if quantity > available_quantity:
                return {"status": "error", "message": "Not enough products in inventory"}

            # If it's a free purchase, cost is zero
            total_cost = 0 if free_purchase else price * quantity

            # If not a free purchase, check buyer's balance
            if not free_purchase:
                cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
                user_balance = cursor.fetchone()[0]

                # Ensure the buyer has sufficient funds
                if user_balance < total_cost:
                    return {"status": "error", "message": "Insufficient funds"}

            # Deduct quantity from product inventory
            cursor.execute("UPDATE products SET quantity = quantity - ? WHERE product_id = ?", (quantity, product_id))

            if not free_purchase:
                # Deduct funds from the buyer's balance
                cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (total_cost, user_id))

                # Add funds to the seller's balance
                cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (total_cost, seller_id))

            # Record the transaction
            cursor.execute("""
                INSERT INTO transactions (buyer_id, seller_id, product_id, quantity, sale_price)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, seller_id, product_id, quantity, total_cost))

            conn.commit()

            # Return success response
            new_balance = None
            if not free_purchase:
                cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
                new_balance = cursor.fetchone()[0]

            return {
                "status": "success",
                "message": "Purchase successful" if not free_purchase else "Free purchase successful",
                "new_balance": new_balance if new_balance is not None else "N/A",
                "purchase_id": cursor.lastrowid
            }

    except Exception as e:
        print(f"Error processing purchase: {e}")
        return {"status": "error", "message": "An error occurred during purchase"}




