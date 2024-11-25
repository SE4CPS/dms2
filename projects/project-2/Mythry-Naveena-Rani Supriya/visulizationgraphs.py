import requests
from functools import reduce
import matplotlib.pyplot as plt

# Step 1: Fetch Data from Localhost
def fetch_data_from_localhost():
    url = "http://localhost:5000/get_flower_data"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from localhost")
        return {}

# Step 2: Create Data Lake
def create_data_lake(data):
    lake = []

    # Flatten MongoDB data
    if "MongoDB" in data:
        lake.extend(data["MongoDB"]["flowers"])

    # Flatten Neo4J data
    if "Neo4J" in data:
        lake.extend(data["Neo4J"]["relationships"])

    # Flatten Redis data
    if "Redis" in data:
        redis_data = data["Redis"]["inventory"]
        lake.extend([
            {"zip_code": details["zip_code"], "source": "Redis", "flower": key}
            for key, details in redis_data.items()
        ])

    # Flatten SQL data
    if "SQL" in data:
        lake.extend(data["SQL"]["flower_sales"])

    return lake

# Step 3: Transform Data Using Map-Filter-Reduce
def transform_data_lake_to_warehouse(lake):
    # Map: Extract zip codes
    mapped_data = list(map(lambda x: x["zip_code"], lake))

    # Filter: Ensure only valid zip codes
    filtered_data = list(filter(lambda x: x.isdigit(), mapped_data))

    # Reduce: Count occurrences of each zip code
    warehouse = reduce(
        lambda acc, zip_code: {**acc, zip_code: acc.get(zip_code, 0) + 1},
        filtered_data,
        {}
    )

    return warehouse

# Step 4: Visualize Data Warehouse
def visualize_warehouse(warehouse):
    # Prepare data for visualization
    zip_codes = list(warehouse.keys())
    counts = list(warehouse.values())

    # Create a bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(zip_codes, counts, color='skyblue')

    # Add labels and title
    plt.xlabel("Zip Code")
    plt.ylabel("Count of Entries")
    plt.title("Count of Entries per Zip Code in Data Warehouse")
    plt.xticks(rotation=45)

    # Show the bar chart
    plt.tight_layout()
    plt.show()

# Step 5: Main Function
def main():
    # Fetch data
    data = fetch_data_from_localhost()

    if not data:
        print("No data available for processing.")
        return

    # Create data lake
    lake = create_data_lake(data)
    print("Data Lake:")
    print(lake)

    # Transform data lake to warehouse
    warehouse = transform_data_lake_to_warehouse(lake)
    print("\nData Warehouse:")
    print(warehouse)

    # Visualize the data warehouse
    visualize_warehouse(warehouse)

if __name__ == "__main__":
    main()
