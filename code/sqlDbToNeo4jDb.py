import json
from datetime import datetime

# Simulated SQL-like data (tuples for flowers and properties)
flowers_sql = [
    (1, "Rose", "Red"),
    (2, "Lily", "White"),
    (3, "Tulip", "Yellow")
]

flower_properties_sql = [
    (1, "Strong", "Spring"),
    (2, "Mild", "Summer"),
    (3, "None", "Spring")
]

# Relationships between flowers and their properties
relationships_sql = [
    (1, 1),  # flower_id 1 is related to flower_property_id 1
    (2, 2),  # flower_id 2 is related to flower_property_id 2
    (3, 3)   # flower_id 3 is related to flower_property_id 3
]

def migrate_sql_to_neo4j(flowers_sql, flower_properties_sql, relationships_sql):
    # Generate a timestamp for the migration
    timestamp = datetime.now().isoformat()
    
    # Step 1: Convert flower properties to a dictionary with metadata
    properties_dict = {
        prop[0]: {  # flower_property_id as the key
            "id": f"flower_property_{prop[0]}",  # Unique identifier for Neo4j
            "fragrance": prop[1],
            "season": prop[2],
            "metadata": {
                "data_source": "sql",
                "timestamp_migration": timestamp
            }
        } for prop in flower_properties_sql
    }
    
    # Step 2: Create a mapping of relationships between flowers and properties
    relationships_dict = {rel[0]: rel[1] for rel in relationships_sql}
    
    # Step 3: Merge flower nodes with flower properties using relationships
    neo4j_data = [
        {
            "id": f"flower_{flower[0]}",  # Unique identifier for Neo4j
            "name": flower[1],
            "color": flower[2],
            "properties": properties_dict.get(relationships_dict.get(flower[0]), {}),
            "metadata": {
                "data_source": "sql",
                "timestamp_migration": timestamp
            }
        } for flower in flowers_sql
    ]
    
    return neo4j_data

# Usage
neo4j_formatted_data = migrate_sql_to_neo4j(flowers_sql, flower_properties_sql, relationships_sql)

# Pretty print the result
print(json.dumps(neo4j_formatted_data, indent=4))
