import requests
from functools import reduce
import matplotlib.pyplot as plt

# Step 1: Fetch data from the endpoint
def fetch_data_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()  # Parse JSON response
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return {}

# Step 2: Flatten the data lake
def flatten_data_lake(data_lake):
    flat_data = []

    # Flatten MongoDB data
    if "MongoDB" in data_lake:
        flat_data.extend(data_lake["MongoDB"]["flowers"])

    # Flatten Neo4J data
    if "Neo4J" in data_lake:
        flat_data.extend(data_lake["Neo4J"]["relationships"])

    # Flatten Redis data
    if "Redis" in data_lake:
        for item in data_lake["Redis"]["inventory"].values():
            flat_data.append(item)

    # Flatten SQL data
    if "SQL" in data_lake:
        flat_data.extend(data_lake["SQL"]["flower_sales"])

    return flat_data

# Step 3: Transform data using Map-Filter-Reduce
def transform_data_with_mfr(flat_data):
    # Map: Extract "zip_code" from each entry
    mapped = list(map(lambda entry: entry["zip_code"], filter(lambda e: "zip_code" in e, flat_data)))
    
    # Reduce: Count occurrences of each "zip_code"
    reduced = reduce(lambda acc, zip_code: {**acc, zip_code: acc.get(zip_code, 0) + 1}, mapped, {})
    
    return reduced

# Step 4: Visualize data using a bar chart
def visualize_warehouse_data(warehouse):
    # Extract zip codes and counts for plotting
    zip_codes = list(warehouse.keys())
    counts = list(warehouse.values())

    # Create bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(zip_codes, counts, color='skyblue', edgecolor='black')
    plt.title("Entry Count by Zip Code", fontsize=16)
    plt.xlabel("Zip Code", fontsize=14)
    plt.ylabel("Count", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Show the chart
    plt.show()

# Main function to execute the ETL process
def main():
    # URL to fetch data
    api_url = "http://localhost:5000/get_flower_data"
    
    # Fetch data and populate the data lake
    data_lake = fetch_data_from_api(api_url)
    if not data_lake:
        print("Failed to create data lake.")
        return

    print("Data Lake:")
    print(data_lake)  # Display the raw data lake

    # Flatten the data lake into a single list of objects
    flat_data = flatten_data_lake(data_lake)

    print("\nFlattened Data:")
    print(flat_data)  # Display the flattened data

    # Transform the data using Map-Filter-Reduce
    warehouse = transform_data_with_mfr(flat_data)

    print("\nWarehouse:")
    print(warehouse)  # Display the transformed data

    # Visualize the warehouse data
    visualize_warehouse_data(warehouse)

if __name__ == "__main__":
    main()
