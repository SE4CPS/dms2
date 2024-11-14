import uuid

def get_uuid():
    # Generate a random UUID (UUID4)
    return str(uuid.uuid4())

print(get_uuid())
