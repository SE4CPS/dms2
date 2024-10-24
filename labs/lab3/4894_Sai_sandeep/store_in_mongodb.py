import uuid
import pymongo
from datetime import datetime

# MongoDB connection setup
uri = "mongodb+srv://i40:dbms2@cluster0.lixbqmp.mongodb.net/lab3"
client = pymongo.MongoClient(uri)

# Access the specific database and collection
db = client['lab3']
student_id_last_four = '4194'  
collection_name = f"4194_SaiSandeep"
collection = db[collection_name]

# Generate 1000 objects with UUID, timestamps, and additional attributes
objects = []
for _ in range(1000):
    obj = {
        "uuid": str(uuid.uuid4()),  # UUID for the object
        "source_db": "MongoDB",  # Source database identifier
        "created_at": datetime.now(),  # Timestamp for creation
        "updated_at": datetime.now(),  # Timestamp for updates
        "attribute1": "Sample Attribute 1",  # Additional attribute 1
        "attribute2": "Sample Attribute 2",  # Additional attribute 2
        "attribute3": "Sample Attribute 3"   # Additional attribute 3
    }
    objects.append(obj)

# Insert objects into the MongoDB collection
collection.insert_many(objects)

print(f"Inserted 1000 objects into the collection: {collection_name}")

# Close the connection to MongoDB
client.close()
