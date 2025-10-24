import sys

# from app_settings import settings
from cocktails_api.cocktails_api_client.client import Client
from cocktails_api.cocktails_api_client.models.cocktail_rs import CocktailRs
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


api_client = Client(base_url="https://api.cezzis.com/prd/cocktails")

# ...existing code...

from cocktails_api.cocktails_api_client.api.cocktails.get_cocktail import sync_detailed

# Example: Retrieve a cocktail by ID
response = sync_detailed(
    client=api_client,
    id="pegu-club",
    x_key="x361#{=j]@m3d><oi#3t4a5z"
)

if response.status_code == 200:
    cocktail_data = response.parsed

    if (cocktail_data is not None) and isinstance(cocktail_data, CocktailRs):
        print("Cocktail retrieved successfully:")
        print("ID:", cocktail_data.item.id)
        print("Title:", cocktail_data.item.descriptive_title)

else:
    print("Failed to retrieve cocktail:", response.status_code)