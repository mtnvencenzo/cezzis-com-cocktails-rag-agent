import sys

# from app_settings import settings
from cosmos_client import get_cosmos_client, initialize_database

# Initialize Cosmos DB client with error handling
cosmos_client = get_cosmos_client()

if not cosmos_client:
    print("Cosmos DB client is not initialized.", file=sys.stderr)
    sys.exit(1)

print("Cosmos DB client initialized successfully.")


[database, container] = initialize_database(cosmos_client)

if database and container:
    print(f"Connected to database: {database.id}, container: {container.id}")
else:
    print("Failed to connect to the database or container.", file=sys.stderr)
    sys.exit(1)