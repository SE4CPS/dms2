import json
from datetime import datetime

# Simulated data, similar to SQL example, for Redis
redis_flowers = {
    "flower_1": {"name": "Rose", "color": "Red"},
    "flower_2": {"name": "Lily", "color": "White"},
    "flower_3": {"name": "Tulip", "color": "Yellow"}
}

redis_flower_properties = {
    "flower_property_1": {"fragrance": "Strong", "season": "Spring"},
    "flower_property_2": {"fragrance": "Mild", "season": "Summer"},
    "flower_property_3": {"fragrance": "None", "season": "Spring"}
}

def migrate_redis_to_mongodb(redis_flowers, redis_flower_properties):
    # Generate a timestamp for the migration
    timestamp = datetime.now().isoformat()

    # Step 1: Convert Redis flower_properties to a dictionary with metadata added
    properties_dict = {
        key: {
            "id": key,  # Redis key as unique identifier
            "fragrance": prop.get("fragrance"),
            "season": prop.get("season"),
            "metadata": {
                "data_source": "redis",
                "timestamp_migration": timestamp
            }
        } for key, prop in redis_flower_properties.items()
    }

    # Step 2: Merge Redis flowers with properties using IDs and add metadata
    mongo_data = [
        {
            "id": key,  # Redis key as unique identifier
            "name": flower.get("name"),
            "color": flower.get("color"),
            "properties": properties_dict.get(f"flower_property_{key.split('_')[1]}", {}),
            "metadata": {
                "data_source": "redis",
                "timestamp_migration": timestamp
            }
        } for key, flower in redis_flowers.items()
    ]

    return mongo_data

# Usage
mongo_formatted_data = migrate_redis_to_mongodb(redis_flowers, redis_flower_properties)

# Pretty print the result
print(json.dumps(mongo_formatted_data, indent=4))
