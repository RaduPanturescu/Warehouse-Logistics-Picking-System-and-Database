import sqlite3
from datetime import datetime
import random as r
from querry import *
from actions import *

# Connect to the SQLite database (or create it if it doesn't exist)
CONNECT = sqlite3.connect('Example_Warehose.db')
cursor = CONNECT.cursor()

# Create the orders table 

# Normalized table setup (database normalisation principle)
# Using 2 tables, one for the unique ID and timestamp
# And the 2nd for the tiems ordered, linking both tables
# With the unique ID

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

#creating the contents of each order table
cursor.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NON NULL,
    item_name TEXT NON NULL,
    quantity INTEGER NON NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)   
)            
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS item_inventory (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT UNIQUE NOT NULL,
    quantity INTEGER DEFAULT 0
)
''')

# Commit the changes and close the connection (always close connection when DB not in use)
CONNECT.commit()
CONNECT.close()

#Creating the order class
class Order:

    def __init__(self, order_id=None, timestamp=None):
        self.order_id = order_id #unique ID for the order
        self.timestamp = timestamp or datetime.now() #timestamp of the orded
        self.items = [] #empty list to store the items

    def add_item(self, cursor, item_name, quantity):

        # Connect to the database
        CONNECT = sqlite3.connect('Example_Warehose.db')
        cursor = CONNECT.cursor()

        #check to see if item is in stock first with the check_stock method
        if self.check_stock(cursor, item_name, quantity):
            self.items.append({'item_name': item_name,
                            'quantity': quantity})
        else:
            print(f"Not enough stock for item: {item_name}")
        CONNECT.commit()
        CONNECT.close()
        
    def save_to_db(self, cursor):
        # Connect to the database
        CONNECT = sqlite3.connect('Example_Warehose.db')
        cursor = CONNECT.cursor()
        # Docstring
        """Save the order and its items to the database."""
        # Adding the timestamp value from the class to the DB orders table
        cursor.execute('''INSERT INTO orders (timestamp) VALUES (?)''', (self.timestamp,)) 

        self.order_id = cursor.lastrowid # get the auto-generated order_id

        # Itterate trough the list of dictionaires, and adding each item/quantity to DB
        for item in self.items:
            if 'item_name' in item and 'quantity' in item:
                cursor.execute('''
                INSERT INTO order_items (order_id, item_name, quantity)
                VALUES (?, ?, ?)
                ''', (self.order_id, item['item_name'], item['quantity']))
                CONNECT.commit()  

            else:
                print(f"Skipping invalid item: {item}")
            
            # Update the inventory table
            cursor.execute('''
            UPDATE item_inventory
            SET quantity = quantity - ?
            WHERE item_name = ?
            ''', (item['quantity'], item['item_name']))

        # Close Database
        CONNECT.commit()
        CONNECT.close()

    def check_stock(self, cursor, item_name, quantity):
        CONNECT = sqlite3.connect('Example_Warehose.db')
        cursor = CONNECT.cursor()

        cursor.execute('''SELECT quantity FROM item_inventory WHERE item_name = ?''', (item_name,))
        result = cursor.fetchone()

        if result and result[0] >= quantity:
            CONNECT.close()
            return True

        CONNECT.close()
        return False

# !!! CREATE ORDER OBJECT !!! #
def create_order(order_name, items):
    # Create the order object with the unique name
    order_name = Order()

    for item in items:
        order_name.add_item(cursor, item['item_name'], item['quantity'])

    order_name.save_to_db(cursor)

# ||| EXECUTE CODE ||| #

shop_order = [
    {'item_name': 'Gucci Flora', 'quantity': 100},
    {'item_name': 'Dior Sauvage', 'quantity': 50}
]




# MAIN LOOP SEQUENCE
# def main():
#     return None

# if __name__ == "__main__":
#     cls()
#     main()