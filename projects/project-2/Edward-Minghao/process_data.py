import json

from flask import Flask, jsonify
import requests


app = Flask(__name__)

def fetch_data_from_server(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully fetched data from {url}")
        return response.json()
    else:
        print(f"Error: Unable to fetch data(Status code: {response.status_code})")
        return {}

def create_data_lake(data):
    lake = []
    for flower in data.get("MongoDB", {}).get("flowers", []):
        lake.append({"db": "MongoDB", "flower": flower})
    for relationship in data.get("Neo4J", {}).get("relationships", []):
        lake.append({"db": "Neo4J", "flower": relationship})
    for key, value in data.get("Redis", {}).get("inventory", {}).items():
        value["name"] = key
        lake.append({"db": "Redis", "flower": value})
    for sale in data.get("SQL", {}).get("flower_sales", []):
        lake.append({"db": "SQL", "flower": sale})
    return lake

@app.route("/get_data_from_lake", methods=["GET"])
def get_data_from_lake():
    from etl import get_data_from_mongodb, get_data_from_redis, get_data_from_neo4j, get_data_from_sql

    data = {
        "MongoDB": get_data_from_mongodb(),
        "Neo4J": get_data_from_neo4j(),
        "SQL": get_data_from_sql(),
        "Redis": get_data_from_redis(),
    }

    return jsonify(data)

def save_data_lake_to_js(lake):
    with open("lake.js", "w") as f:
        f.write(f"const lake = {json.dumps(lake, indent=2)};\n")


def main():
    url = "http://127.0.0.1:5000/get_flower_data"
    data = fetch_data_from_server(url)

    if not data:
        print("No flowers data")
        return

    data_lake = create_data_lake(data)
    print("Data lake Created")
    #print(json.dumps(data_lake, indent=2))

    save_data_lake_to_js(data_lake)
    print("Data lake Saved")


if __name__ == "__main__":
    from threading import Thread

    def run_flask():
        app.run(debug=True, use_reloader=False, port=5001)

    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    main()