import uuid
import random
import datetime
from pymongo import MongoClient
import faker

# Initialize the Faker library to generate random names and phone numbers
fake = faker.Faker()

# MongoDB connection string
MONGO_URI = "mongodb+srv://i40:dbms2@cluster0.lixbqmp.mongodb.net/lab3"
client = MongoClient(MONGO_URI)

# Specify the collection name using the last four digits of your student ID
collection_name = "5770_Vinay"  # Replace 'test2' with 'LAST_FOUR_DIGITS' if necessary

# Create the database and collection
db = client.lab3
collection = db[collection_name]

# Function to generate 1000 objects
def generate_objects(num_objects):
    objects = []
    for _ in range(num_objects):
        obj = {
            "uuid": str(uuid.uuid4()),  # Unique identifier
            "source_database": "MongoDB",
            "created_at": datetime.datetime.now(),  # Timestamp for creation
            "updated_at": datetime.datetime.now(),  # Timestamp for updates
            "name": fake.name(),  # Random name
            "age": random.randint(18, 80),  # Random age between 18 and 80
            "mobile_number": fake.phone_number()  # Random mobile number
        }
        objects.append(obj)
    return objects

# Generate objects and insert them into the collection
def main():
    objects = generate_objects(1000)
    result = collection.insert_many(objects)
    print(f"Inserted {len(result.inserted_ids)} objects into the collection.")

if __name__ == "__main__":
    main()
