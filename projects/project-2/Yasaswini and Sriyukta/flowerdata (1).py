import requests
from collections import Counter

# Function to fetch data from the data lake
def fetch_flower_data():
    try:
        # Fetch data from localhost:5000/get_flower_data
        url = "http://localhost:5000/get_flower_data"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        db = response.json()  # Parse the JSON response into a Python dictionary

        # Step 1: Print Data Lake (Raw Data)
        print("Data Lake (Raw Data):")
        print(db)  # This prints the entire raw data from the data lake
        print("\n")

        # Step 2: Extract all zip codes (Map step)
        all_zip_codes = []

        # Extract zip codes from MongoDB
        mongo_zip_codes = [flower['zip_code'] for flower in db['MongoDB']['flowers']]
        all_zip_codes.extend(mongo_zip_codes)

        # Extract zip codes from Neo4J
        neo4j_zip_codes = [relationship['zip_code'] for relationship in db['Neo4J']['relationships']]
        all_zip_codes.extend(neo4j_zip_codes)

        # Extract zip codes from Redis
        redis_zip_codes = [item['zip_code'] for item in db['Redis']['inventory'].values()]
        all_zip_codes.extend(redis_zip_codes)

        # Extract zip codes from SQL
        sql_zip_codes = [sale['zip_code'] for sale in db['SQL']['flower_sales']]
        all_zip_codes.extend(sql_zip_codes)

        # Step 3: Count the occurrences of each zip code (Reduce step)
        warehouse = dict(Counter(all_zip_codes))

  # Output the warehouse object
        print("Warehouse Object (Zip Code Count):")
        print(warehouse)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching flower data: {e}")

# Call the function to fetch and process the data
fetch_flower_data()