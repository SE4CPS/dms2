from flask import Flask, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Simulated MongoDB data
def fetch_mongodb_data():
    return [
        {"name": "Rose", "color": "Red", "price": 10, "stock": 100, "zip_code": "10001"},
        {"name": "Tulip", "color": "Yellow", "price": 7, "stock": 150, "zip_code": "10002"},
        {"name": "Orchid", "color": "Purple", "price": 15, "stock": 80, "zip_code": "10003"},
        {"name": "Sunflower", "color": "Yellow", "price": 5, "stock": 200, "zip_code": "10004"},
        {"name": "Daisy", "color": "White", "price": 3, "stock": 300, "zip_code": "10005"}
    ]

# Simulated Neo4J data
def fetch_neo4j_data():
    return [
        {"flower": "Rose", "related_to": "Gift Bouquet", "zip_code": "10001"},
        {"flower": "Tulip", "related_to": "Spring Collection", "zip_code": "10002"},
        {"flower": "Orchid", "related_to": "Exotic Collection", "zip_code": "10003"},
        {"flower": "Sunflower", "related_to": "Summer Collection", "zip_code": "10004"},
        {"flower": "Daisy", "related_to": "Wedding Bouquet", "zip_code": "10005"}
    ]

# Simulated Redis data
def fetch_redis_data():
    return {
        "Rose": {"quantity": 100, "last_restock": "2023-10-01", "zip_code": "10001"},
        "Tulip": {"quantity": 150, "last_restock": "2023-10-03", "zip_code": "10002"},
        "Orchid": {"quantity": 80, "last_restock": "2023-10-05", "zip_code": "10003"},
        "Sunflower": {"quantity": 200, "last_restock": "2023-10-07", "zip_code": "10004"},
        "Daisy": {"quantity": 300, "last_restock": "2023-10-09", "zip_code": "10005"}
    }

# Simulated SQL data
def fetch_sql_data():
    return [
        {"name": "Rose", "units_sold": 50, "revenue": 500, "zip_code": "10001"},
        {"name": "Tulip", "units_sold": 70, "revenue": 490, "zip_code": "10002"},
        {"name": "Orchid", "units_sold": 30, "revenue": 450, "zip_code": "10003"},
        {"name": "Sunflower", "units_sold": 90, "revenue": 450, "zip_code": "10004"},
        {"name": "Daisy", "units_sold": 120, "revenue": 360, "zip_code": "10005"}
    ]

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the ETL API! Access combined data at /data or view the dashboard at /dashboard."

@app.route('/data', methods=['GET'])
def get_combined_data():
    data = {
        "MongoDB": fetch_mongodb_data(),
        "Neo4J": fetch_neo4j_data(),
        "Redis": fetch_redis_data(),
        "SQL": fetch_sql_data()
    }
    return jsonify(data)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return send_file('dashboard.html')

# Serve the main.js file directly
@app.route('/main.js', methods=['GET'])
def serve_js():
    return send_from_directory(os.getcwd(), 'main.js')

if __name__ == '__main__':
    app.run(debug=True)
