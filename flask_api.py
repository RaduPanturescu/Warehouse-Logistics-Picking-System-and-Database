
from flask import Flask, jsonify, request
from querry import *
from actions import *
from functools import wraps
from api_key import *

app = Flask(__name__)

# === SECURITY: API KEY AUTHENTICATION === #
# Define a list of valid API keys (for demonstration purposes)


# Decorator to secure endpoints
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the API key from the request headers
        api_key = request.headers.get('X-API-Key')
        if api_key not in VALID_API_KEYS:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function


# Root Endpoint
@app.route('/')
def home():
    return "Welcome to the Warehouse API"


# ********** GET REQUESTS **********
@app.route('/inventory', methods=['GET'])
#@require_api_key  ---> use this argument to secure the endpoint
def check_inventory_API():
    # calling the query functions for the DB
    return check_inventory()

@app.route('/orders', methods=['GET'])
def check_orders_API():
    # calling the query functions for the DB
    return querry_order()
    

@app.route('/order-items', methods=['GET'])
def querry_order_items_API():
    # calling the query functions for the DB
    return querry_order_items()


@app.route('/database-list', methods=['GET'])
def check_all_active_db_API():
    # calling the query functions for the DB
    return check_all_active_db()

# ********** POST REQUESTS **********

# Add items to inventory   ????????
@app.route('/inventory/add', methods=['POST'])
@require_api_key  # Secure this endpoint
def add_inventory():
    data = request.json  # Get JSON data from the request
    items = data.get('items')  # Extract the list of items
    if not items:
        return jsonify({"error": "No items provided"}), 400

    # Call your add_to_inventory function
    add_to_inventory(items)
    return jsonify({"message": "Inventory updated successfully"})

# ********** ERROR HANDLING **********

# Run the Flask API
if __name__ == '__main__':
    app.run(debug = True)


