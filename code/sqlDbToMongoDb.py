import json
from datetime import datetime

# SQL data tables as tuples
flowers = [
    (1, "Rose", "Red"),
    (2, "Lily", "White"),
    (3, "Tulip", "Yellow")
]

flower_properties = [
    (1, "Strong", "Spring"),
    (2, "Mild", "Summer"),
    (3, "None", "Spring")
]

def migrate_sql_to_mongodb(flowers, flower_properties):
    # Generate a timestamp for the migration
    timestamp = datetime.now().isoformat()
    
    # Step 1: Convert flower_properties to a dictionary with unique ids and metadata for quick lookup
    properties_dict = {
        prop[0]: {
            "id": f"flower_property_{prop[0]}",  # Unique identifier based on table name and flower_id
            "fragrance": prop[1],
            "season": prop[2],
            "metadata": {
                "data_source": "sqldb",
                "timestamp_migration": timestamp
            }
        } for prop in flower_properties
    }
    
    # Step 2: Merge flowers with properties using flower_id and create MongoDB-compatible format with metadata
    mongo_data = list(map(lambda flower: {
        "id": f"flower_{flower[0]}",  # Unique identifier based on table name and primary key
        "name": flower[1],
        "color": flower[2],
        "properties": properties_dict.get(flower[0], {}),
        "metadata": {
            "data_source": "sqldb",
            "timestamp_migration": timestamp
        }
    }, flowers))
    
    return mongo_data

# Usage
mongo_formatted_data = migrate_sql_to_mongodb(flowers, flower_properties)

# Pretty print the result
print(json.dumps(mongo_formatted_data, indent=4))
