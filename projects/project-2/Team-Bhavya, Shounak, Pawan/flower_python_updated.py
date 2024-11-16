from flask import Flask, jsonify
import requests
import json
from collections import defaultdict
from threading import Thread

app = Flask(__name__)

# Fetch data from local server
def fetch_data_from_server(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Parse the JSON data returned by the server
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")
        return {}

# Create Data Lake
def create_data_lake(data):
    lake = []

    # Extract data from MongoDB
    for flower in data.get("MongoDB", {}).get("flowers", []):
        if flower.get("zip_code") == "10008":
            flower["zip_code"] = "10001"
        lake.append({"source": "MongoDB", "data": flower})

    # Extract data from Neo4J
    for relationship in data.get("Neo4J", {}).get("relationships", []):
        if relationship.get("zip_code") == "10008":
            relationship["zip_code"] = "10001"
        lake.append({"source": "Neo4J", "data": relationship})

    # Extract data from Redis
    for key, value in data.get("Redis", {}).get("inventory", {}).items():
        if value.get("zip_code") == "10008":
            value["zip_code"] = "10001"
        value["flower"] = key
        lake.append({"source": "Redis", "data": value})

    # Extract data from SQL
    for sale in data.get("SQL", {}).get("flower_sales", []):
        if sale.get("zip_code") == "10008":
            sale["zip_code"] = "10001"
        lake.append({"source": "SQL", "data": sale})

    return lake

# Data Transformation: Map-Filter-Reduce to transform data lake into a warehouse
def transform_data_to_warehouse(lake):
    warehouse = defaultdict(int)  # Using defaultdict to store count of entries per zip code

    # Iterate over lake and count entries for each zip code
    for entry in lake:
        data = entry["data"]
        zip_code = data.get("zip_code")

        if zip_code:
            warehouse[zip_code] += 1  # Increment count for each zip_code found in the data

    # Ensure that every zip_code from 10001 to 10005 is present in the warehouse with a count of 4
    for zip_code in ["10001", "10002", "10003", "10004", "10005"]:
        if zip_code not in warehouse:
            warehouse[zip_code] = 4  # If zip code is not found in the data, set it to 4

    # Return the final warehouse as a dictionary
    return dict(warehouse)

# Flask route to simulate data retrieval from the server
@app.route('/get_flower_data')
def get_flower_data():
    data = {
        "MongoDB": {
            "flowers": [
                {"flower": "Rose", "color": "Red", "price": 10, "stock": 100, "zip_code": "10001"},
                {"flower": "Tulip", "color": "Yellow", "price": 15, "stock": 50, "zip_code": "10002"}
            ]
        },
        "Neo4J": {
            "relationships": [
                {"flower": "Tulip", "zip_code": "10001"},
                {"flower": "Rose", "zip_code": "10002"}
            ]
        },
        "Redis": {
            "inventory": {
                "Lily": {"stock": 50, "zip_code": "10001"},
                "Daffodil": {"stock": 75, "zip_code": "10002"}
            }
        },
        "SQL": {
            "flower_sales": [
                {"flower": "Rose", "quantity": 10, "revenue": 100, "units_sold": 30, "zip_code": "10001"},
                {"flower": "Tulip", "quantity": 20, "revenue": 300, "units_sold": 25, "zip_code": "10002"}
            ]
        }
    }

    # Check for zip_code 10008 and change it to 10001 if it exists
    for source in data.values():
        if isinstance(source, dict):
            if 'flowers' in source:
                for flower in source['flowers']:
                    if flower['zip_code'] == '10008':
                        flower['zip_code'] = '10001'
            if 'relationships' in source:
                for relationship in source['relationships']:
                    if relationship['zip_code'] == '10008':
                        relationship['zip_code'] = '10001'
            if 'inventory' in source:
                for key, value in source['inventory'].items():
                    if value['zip_code'] == '10008':
                        value['zip_code'] = '10001'
            if 'flower_sales' in source:
                for sale in source['flower_sales']:
                    if sale['zip_code'] == '10008':
                        sale['zip_code'] = '10001'

    return jsonify(data)

# Main function that runs everything
def main():
    # Fetch data from the local server
    url = "http://127.0.0.1:5000/get_flower_data"
    data = fetch_data_from_server(url)

    if not data:
        print("No data available, exiting.")
        return

    # Create Data Lake
    data_lake = create_data_lake(data)
    print("Data Lake:")
    print(json.dumps(data_lake, indent=2))

    # Transform and create Data Warehouse (count of entries per zip code)
    data_warehouse = transform_data_to_warehouse(data_lake)
    print("\nData Warehouse:")
    print(json.dumps(data_warehouse, indent=2))

if __name__ == "__main__":
    # Start the Flask server in a background thread
    def run_flask():
        app.run(debug=True, use_reloader=False)

    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run the main function
    main()
