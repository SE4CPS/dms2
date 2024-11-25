from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

data_lake_project2 = []

def update_data_lake():
    global data_lake_project2
    try:
        response = requests.get("http://127.0.0.1:5000/get_flower_data")
        response.raise_for_status()
        fetched_data = response.json()
        
        data_lake_project2.clear()

        for flower in fetched_data.get("MongoDB", {}).get("flowers", []):
            flat_flower = {"db": "MongoDB"}
            flat_flower.update(flower)
            data_lake_project2.append(flat_flower)

        for relationship in fetched_data.get("Neo4J", {}).get("relationships", []):
            flat_relationship = {"db": "Neo4J"}
            flat_relationship.update(relationship)
            data_lake_project2.append(flat_relationship)

        for flower, details in fetched_data.get("Redis", {}).get("inventory", {}).items():
            flat_details = {"db": "Redis", "flower": flower}
            flat_details.update(details)
            data_lake_project2.append(flat_details)

        for sale in fetched_data.get("SQL", {}).get("flower_sales", []):
            flat_sale = {"db": "SQL"}
            flat_sale.update(sale)
            data_lake_project2.append(flat_sale)

        print("var lake = " + json.dumps(data_lake_project2, indent=4))  
    except requests.RequestException as e:
        data_lake_project2.clear()  
        error_message = {"db": "error", "message": f"Failed to fetch data: {str(e)}"}
        data_lake_project2.append(error_message)
        print("Data Lake Error:")
        print(json.dumps(data_lake_project2, indent=4)) 

@app.route('/data_lake', methods=['GET'])
def display_data_lake():
    if not data_lake_project2:
        update_data_lake()
    return jsonify(data_lake_project2)

@app.route('/refresh_data_lake', methods=['POST'])
def refresh_data_lake():
    update_data_lake()
    return jsonify({"message": "Data Lake updated successfully!", "data_lake": data_lake_project2})

if __name__ == '__main__':
    update_data_lake()
    app.run(debug=True, port=5500)
