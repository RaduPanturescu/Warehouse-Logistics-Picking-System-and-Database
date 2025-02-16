import sqlite3
import os
from Warehouse_Picking_System import *


#=== MODIFY DATABASE ===#

# clear terminal text
cls = lambda: os.system('cls')

def add_to_inventory(items):
    # Connect to the database
    CONNECT = sqlite3.connect('Example_Warehose.db')
    cursor = CONNECT.cursor()

    # Loop through each item in the list
    for item in items:
        # Insert the item into the item_inventory table
        
        cursor.execute('''
        INSERT INTO item_inventory (item_name, quantity)
        VALUES (?, ?)
        ON CONFLICT(item_name) DO UPDATE SET quantity = quantity + excluded.quantity 
        ''', (item["item_name"], item["quantity"]))

    # Commit the changes to the database
    CONNECT.commit()
    # Close the database connection
    CONNECT.close()

# Delete one specific item from order_items
def delete_WIDGET_A(deleted_item):
    CONNECT = sqlite3.connect('Example_Warehose.db')
    cursor = CONNECT.cursor()

    query = '''
    DELETE FROM order_items
    WHERE item_name = ?
    '''

    cursor.execute(query, (deleted_item,))
    CONNECT.commit()
    CONNECT.close()

# Delete an order from the orders table
def delete_order_table(deleted_order_id):
    CONNECT = sqlite3.connect('Example_Warehose.db')
    cursor = CONNECT.cursor()

    for deleted_order_id in range(deleted_order_id):
        query = '''
        DELETE FROM orders
        WHERE order_id = ?
        '''

        cursor.execute(query, (deleted_order_id,))
    CONNECT.commit()
    CONNECT.close()

def remove_inventory_item(item_id_to_delete):
    CONNECT = sqlite3.connect('Example_Warehose.db')
    cursor = CONNECT.cursor()

    query = '''
    DELETE FROM item_inventory
    WHERE item_id = ?
    '''
    cursor.execute(query, (item_id_to_delete,))

    CONNECT.commit()
    CONNECT.close()

def drop_table(table_name):
    CONNECT = sqlite3.connect('Example_Warehose.db')
    cursor = CONNECT.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    CONNECT.commit()
    CONNECT.close()

# adding to inventory from incoming supply
def inventory_supply(item_numbers):

    items = []

    for i in range(item_numbers):
        supply = input("Please Enter the item you want to supply: ")
        quantity = int(input("Please enter the quantity for this item: "))

        item = {'item_name': supply, 'quantity': quantity}
        items.append(item)

        # ADDS THE INPUTED ITEMS TO THE INVENTORY DATABASE DIRECTLY
        add_to_inventory(items)
    return items

# CREATE THE ORDER AND ADD IT TO DB DIRECTLY WITH THE create_order() function at the end
def shop_create_order(item_numbers): 

    items = []
    order_name = input("Create a name for this order: ")

    for i in range(item_numbers):
        supply = input("Please Enter the item you want to supply: ")
        quantity = int(input("Please enter the quantity for this item: "))

        item = {'item_name': supply, 'quantity': quantity}
        items.append(item)

        # CREATES THE ORDER AND ADDS IT DIRECTLY TO THE DB
        create_order(order_name, items)
    return items