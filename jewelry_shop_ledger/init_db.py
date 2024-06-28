import sqlite3

connection = sqlite3.connect('database/shop.db')

with connection:
    connection.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            date_of_first_purchase TEXT NOT NULL,
            notes TEXT
        )
    ''')
    connection.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            date_of_transaction TEXT NOT NULL,
            total_price REAL NOT NULL,
            amount_paid REAL NOT NULL,
            remaining_amount REAL NOT NULL,
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')

connection.close()
