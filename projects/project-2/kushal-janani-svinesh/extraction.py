from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

data_lake_entries = []

def refresh_data_lake():
    global data_lake_entries
    try:
        response = requests.get("http://127.0.0.1:5000/get_flower_data")
        response.raise_for_status()
        response_data = response.json()

        data_lake_entries = []

        # Process MongoDB Data
        for flower_data in response_data.get("MongoDB", {}).get("flowers", []):
            flower_entry = {"source": "MongoDB"}
            flower_entry.update(flower_data)
            data_lake_entries.append(flower_entry)

        # Process Neo4J Data
        for relationship in response_data.get("Neo4J", {}).get("relationships", []):
            relationship_entry = {"source": "Neo4J"}
            relationship_entry.update(relationship)
            data_lake_entries.append(relationship_entry)

        # Process Redis Data
        for flower_name, inventory_details in response_data.get("Redis", {}).get("inventory", {}).items():
            redis_entry = {"source": "Redis", "flower": flower_name}
            redis_entry.update(inventory_details)
            data_lake_entries.append(redis_entry)

        # Process SQL Data
        for sale_data in response_data.get("SQL", {}).get("flower_sales", []):
            sale_entry = {"source": "SQL"}
            sale_entry.update(sale_data)
            data_lake_entries.append(sale_entry)

        print("var lake = " + json.dumps(data_lake_entries, indent=4))
    except requests.RequestException as error:
        data_lake_entries = []
        error_info = {"source": "error", "message": f"Unable to retrieve data: {str(error)}"}
        data_lake_entries.append(error_info)
        print("Error Occurred:")
        print(json.dumps(data_lake_entries, indent=4))

@app.route('/data_lake', methods=['GET'])
def get_data_lake():
    if not data_lake_entries:
        refresh_data_lake()
    return jsonify(data_lake_entries)

@app.route('/refresh_data_lake', methods=['POST'])
def post_refresh_data_lake():
    refresh_data_lake()
    return jsonify({"message": "Data Lake has been refreshed successfully!", "data_lake": data_lake_entries})

if __name__ == '__main__':
    refresh_data_lake()
    app.run(debug=True, port=5500)
