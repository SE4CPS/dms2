import requests
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Data Extraction
def create_data_lake(api_url):
    try:
        # Fetch data from the API
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Data Lake: Combine data from all sources
        lake = []
        for flower in data["MongoDB"]["flowers"]:
            lake.append({**flower, "db": "MongoDB"})

        for relation in data["Neo4J"]["relationships"]:
            lake.append({**relation, "db": "Neo4J"})

        for flower, details in data["Redis"]["inventory"].items():
            lake.append({**details, "db": "Redis", "name": flower})

        for sale in data["SQL"]["flower_sales"]:
            lake.append({**sale, "db": "SQL"})

        print("Data Lake Created:")
        print(pd.DataFrame(lake))  # Display Data Lake
        return lake
    except Exception as e:
        print(f"Error creating data lake: {e}")
        return []

# Step 2: Data Transformation
def transform_data(lake):
    try:
        # Extract zip codes and count entries
        df = pd.DataFrame(lake)
        zip_counts = df['zip_code'].value_counts().reset_index()
        zip_counts.columns = ['zip_code', 'count']

        print("\nTransformed Data Warehouse:")
        print(zip_counts)  # Display Warehouse
        return zip_counts
    except Exception as e:
        print(f"Error transforming data: {e}")
        return pd.DataFrame()

# Step 3: Data Loading
def load_dashboard(data_warehouse):
    try:
        # Plot bar chart using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.bar(data_warehouse['zip_code'], data_warehouse['count'], color='skyblue')
        plt.title('Entries per Zip Code', fontsize=16)
        plt.xlabel('Zip Code', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('data_dashboard.png')  # Save chart as an image
        plt.show()
        print("Dashboard Loaded: Bar chart saved as 'data_dashboard.png'")
    except Exception as e:
        print(f"Error loading dashboard: {e}")

# Step 4: Main Process
def main():
    api_url = "http://127.0.0.1:5000/get_flower_data"  # API Endpoint

    # Create Data Lake
    lake = create_data_lake(api_url)
    if not lake:
        return

    # Transform Data into Warehouse
    warehouse = transform_data(lake)
    if warehouse.empty:
        return

    # Load Dashboard
    load_dashboard(warehouse)

if __name__ == "__main__":
    main()
