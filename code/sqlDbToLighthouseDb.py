import json
from datetime import datetime

# Simulated SQL-like data as tuples
# Each tuple represents a flower's basic data
flowers = [
    (1, "Rose", "Red"),
    (2, "Lily", "White"),
    (3, "Tulip", "Yellow")
]

def migrate_basic_flowers_to_mongodb(flowers):
    # Generate a migration timestamp
    migration_timestamp = datetime.now().isoformat()
    
    # Convert each flower to MongoDB-compatible format with only basic data and metadata
    mongo_data = [
        {
            "id": f"flower_{flower[0]}",  # Unique identifier based on flower_id
            "species": flower[1],
            "color": flower[2],
            "metadata": {
                "data_source": "lighthouse_sql",
                "timestamp_migration": migration_timestamp
            }
        } for flower in flowers
    ]
    
    return mongo_data

# Usage
mongo_formatted_data = migrate_basic_flowers_to_mongodb(flowers)

# Pretty print the result
print(json.dumps(mongo_formatted_data, indent=4))
