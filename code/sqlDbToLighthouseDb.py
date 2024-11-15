import json
from datetime import datetime

# Simulated SQL-like data as tuples
# Each tuple represents a flower's basic data (flower_id, name, color)
flowers = [
    (1, "Rose", "Red"),
    (2, "Lily", "White"),
    (3, "Tulip", "Yellow")
]

def migrate_basic_flowers_to_lighthouse(flowers):
    # Generate a migration timestamp
    migration_timestamp = datetime.now().isoformat()

    # Convert each flower to Lighthouse-compatible format
    lighthouse_data = [
        {
            "id": f"flower_{flower[0]}",  # Unique identifier based on flower_id
            "name": flower[1],
            "color": flower[2],
            "metadata": {
                "data_source": "lighthouse_sql",  # Indicates the source
                "timestamp_migration": migration_timestamp
            }
        } for flower in flowers
    ]

    return lighthouse_data

# Usage
lighthouse_formatted_data = migrate_basic_flowers_to_lighthouse(flowers)

# Pretty print the result
print(json.dumps(lighthouse_formatted_data, indent=4))
