'''
database.py
The Shop’s Filing Cabinet

What it Contains: Code to connect to your database, 
handle transactions, and manage connection pooling.

Why You Need It: Separates database 
connection logic from other files, 

'''
from contextlib import contextmanager
import sqlite3

class DatabasePool:
    def __init__(self, db_name):
        self.db_name = db_name
        
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

def create_tables():
    conn = sqlite3.connect('AUBoutique.db')
    cursor = conn.cursor()

    # Create users table with correct fields
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        email_address TEXT UNIQUE NOT NULL,
        role TEXT CHECK(role IN ('buyer', 'seller')),
        products TEXT,
        balance REAL DEFAULT 0.0,
        online BOOLEAN DEFAULT FALSE
    )""")

    # Create products table
    cursor.execute("""CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        picture BLOB,
        price REAL NOT NULL,
        description TEXT,
        quantity INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )""")

    # Create transactions table with sale_price column
    cursor.execute("""CREATE TABLE IF NOT EXISTS transactions(
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        buyer_id INTEGER,
        seller_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        sale_price REAL,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (buyer_id) REFERENCES users(user_id),
        FOREIGN KEY (seller_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )""")

    conn.commit()
    conn.close()





        


