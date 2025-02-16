import sqlite3
from flask import jsonify

# === QUERRY DATABASE === #
def querry_order_items():
    CONNECT = sqlite3.connect('Example_Warehose.db')
    cursor = CONNECT.cursor()

    query = '''
    SELECT order_id, item_name, quantity 
    FROM order_items
    '''

    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print(f"""-------------------------------------------\n
        Order ID: {row[0]}, Item: {row[1]}, Quantity: {row[2]}""")

    CONNECT.close()

    return jsonify(result)

def querry_order():
    CONNECT = sqlite3.connect('Example_Warehose.db')
    cursor = CONNECT.cursor()

    query = '''SELECT order_id, timestamp FROM orders'''

    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        print(f"""-------------------------------------\n
        Order ID: {row[0]}, Timestamp: {row[1]}""")
    CONNECT.close()

    return jsonify(result)

def check_inventory():
    CONNECT = sqlite3.connect('Example_Warehose.db')
    cursor = CONNECT.cursor()

    query = '''SELECT item_id, item_name, quantity FROM item_inventory'''
    cursor.execute(query)
    result = cursor.fetchall()

    # Convert the result to a list of dictionaries
    inventory = []
    for row in result:
        inventory.append({
            'item_id': row[0],
            'item_name': row[1],
            'quantity': row[2]
        })
    CONNECT.close()

    return jsonify(inventory)


def check_all_active_db():
    # Connect to the SQLite database
    CONNECT = sqlite3.connect('Example_Warehose.db')
    cursor = CONNECT.cursor()

    # Query to list all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Print the table names
    print("Tables in the database:")
    for table in tables:
        print(table[0])

    # Close the connection
    CONNECT.close()

    return jsonify(tables)