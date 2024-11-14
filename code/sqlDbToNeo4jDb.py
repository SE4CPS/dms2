import json
from datetime import datetime

# Simulated Neo4j data
# Nodes for flowers
neo4j_flowers = [
    {"id": 1, "name": "Rose", "color": "Red"},
    {"id": 2, "name": "Lily", "color": "White"},
    {"id": 3, "name": "Tulip", "color": "Yellow"}
]

# Nodes for flower properties
neo4j_flower_properties = [
    {"id": 1, "fragrance": "Strong", "season": "Spring"},
    {"id": 2, "fragrance": "Mild", "season": "Summer"},
    {"id": 3, "fragrance": "None", "season": "Spring"}
]

# Relationships between flowers and their properties
# Each relationship links a flower `id` to a properties `id`
neo4j_relationships = [
    {"flower_id": 1, "property_id": 1},
    {"flower_id": 2, "property_id": 2},
    {"flower_id": 3, "property_id": 3}
]

def migrate_neo4j_to_mongodb(neo4j_flowers, neo4j_flower_properties, neo4j_relationships):
    # Generate a timestamp for the migration
    timestamp = datetime.now().isoformat()
    
    # Step 1: Convert properties nodes to a dictionary with metadata
    properties_dict = {
        prop["id"]: {
            "id": f"flower_property_{prop['id']}",  # Unique identifier based on Neo4j node id
            "fragrance": prop.get("fragrance"),
            "season": prop.get("season"),
            "metadata": {
                "data_source": "neo4j",
                "timestamp_migration": timestamp
            }
        } for prop in neo4j_flower_properties
    }
    
    # Step 2: Create a dictionary to map each flower to its related property
    relationships_dict = {rel["flower_id"]: rel["property_id"] for rel in neo4j_relationships}
    
    # Step 3: Merge flowers with properties using relationships and add metadata
    mongo_data = [
        {
            "id": f"flower_{flower['id']}",  # Unique identifier based on Neo4j node id
            "name": flower.get("name"),
            "color": flower.get("color"),
            "properties": properties_dict.get(relationships_dict.get(flower["id"], {}), {}),
            "metadata": {
                "data_source": "neo4j",
                "timestamp_migration": timestamp
            }
        } for flower in neo4j_flowers
    ]
    
    return mongo_data

# Usage
mongo_formatted_data = migrate_neo4j_to_mongodb(neo4j_flowers, neo4j_flower_properties, neo4j_relationships)

# Pretty print the result
print(json.dumps(mongo_formatted_data, indent=4))
