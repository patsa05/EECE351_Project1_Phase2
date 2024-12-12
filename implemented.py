import requests
import json
import sqlite3
import hashlib
import threading
import time
from datetime import datetime, timedelta
from functools import lru_cache
from database import DatabasePool
from config import DATABASE_NAME, BUFFER_SIZE, api_key
import requests
# Initialize database pool

db_pool = DatabasePool(DATABASE_NAME)
def convert_amount(from_currency, amount, to_currency):
        EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/"
        try:
            # Fetch exchange rates
            response = requests.get(f"{EXCHANGE_API_URL}{from_currency}")
            if response.status_code != 200:
                print("Error", "Invalid from currency or network issue.")
                return

            data = response.json()
            rates = data.get("rates", {})
            if to_currency not in rates:
                print("Error", f"Unsupported currency: {to_currency}")
                return

            # Perform conversion
            converted_amount = amount * rates[to_currency]
            return converted_amount
        except Exception as e:
            print("Error", f"An error occurred: {str(e)}")


    


def process_rate_product(request):
    user_id = request["user_id"]
    product_id = request["product_id"]
    rating_stars = request["rating_stars"]

    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

            # Check if the product exists
            cursor.execute("SELECT 1 FROM products WHERE product_id = ?", (product_id,))
            product = cursor.fetchone()
            if not product:
                return {"status": "error", "message": "The product does not exist"}

            # Insert or update the rating
            cursor.execute("""
                INSERT INTO ratings (user_id, product_id, rating_stars)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, product_id) DO UPDATE SET rating_stars = excluded.rating_stars;
            """, (user_id, product_id, rating_stars))

            conn.commit()

            return {"status": "success", "message": "Rating submitted successfully"}

    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            return {"status": "error", "message": "You have already rated this product"}
    except Exception as e:
        print(f"Error processing rating: {e}")
        
        return {"status": "error", "message": "An error occurred while submitting the rating"}

def process_view_average_rating(request):
    product_id = request.get("product_id")

   # if not isinstance(product_id, int):
    #    return {"status": "error", "message": "Invalid product_id"}

    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()

           # Check if the product exists
            cursor.execute("SELECT 1 FROM products WHERE product_id = ?", (product_id,))
            product = cursor.fetchone()
            if not product:
                return {"status": "error", "message": "The product does not exist"}

            cursor.execute("""
                SELECT AVG(rating_stars) AS average_rating
                FROM ratings
                WHERE product_id = ?
            """, (product_id,))
            avg_rating = cursor.fetchone()[0]  # Adjusted for tuple return

            return {
                "status": "success",
                "average_rating": avg_rating,
            }


    except Exception as e:
        print(f"Error fetching average rating: {e}")
        return {"status": "error", "message": "An error occurred while fetching the average rating"}
