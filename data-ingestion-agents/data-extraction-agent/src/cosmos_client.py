import os
import sys

from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey, DatabaseProxy, ContainerProxy
from azure.identity import DefaultAzureCredential
import urllib3
from app_settings import settings, is_local_environment

# ------------------------------------------------
# Initialize Cosmos DB client with error handling
# ------------------------------------------------
def get_cosmos_client() -> CosmosClient | None:
    cosmos_client: CosmosClient

    if (settings.cosmos_connection_string):
        # Disablinge insecure request warnings for local development
        # For usage with the Cosmos DB Emulator
        if os.environ.get("ENV") == "local":
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            cosmos_client = CosmosClient.from_connection_string(settings.cosmos_connection_string, None, None) # type: ignore
        except AzureError as e:
            print(f"Failed to initialize Cosmos DB client from connection string: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Unexpected error during initialization from connection string: {e}", file=sys.stderr)
            return None
    else:
        try:
            credential = DefaultAzureCredential()
            cosmos_client = CosmosClient(settings.cosmos_account_endpoint, credential)
        except AzureError as e:
            print(f"Failed to initialize Cosmos DB client: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Unexpected error during initialization: {e}", file=sys.stderr)
            return None

    return cosmos_client
# ------------------------------------------------


def initialize_database(client: CosmosClient) -> tuple[DatabaseProxy, ContainerProxy]:
    try:
        if is_local_environment():
            database = client.create_database_if_not_exists(
                id=settings.cosmos_database_name,
                offer_throughput=400
            )
            container = database.create_container_if_not_exists(
                id=settings.cosmos_container_name,
                partition_key=PartitionKey(path="/id"),
                offer_throughput=None
            )
            return database, container
        else:
            database = client.get_database_client(settings.cosmos_database_name)
            container = database.get_container_client(settings.cosmos_container_name)
            return database, container
        
    except AzureError as e:
        print(f"Failed to initialize or create database '{settings.cosmos_database_name}': {e}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Unexpected error during database initialization: {e}", file=sys.stderr)
        raise