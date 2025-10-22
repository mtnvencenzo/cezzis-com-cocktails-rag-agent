import sys

from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import urllib3
from app_settings import AppSettings

settings = AppSettings()

# Validate required configuration
if not settings.cosmos_account_endpoint:
    raise ValueError("COSMOS_ACCOUNT_ENDPOINT environment variable is required")
if not settings.cosmos_database_name:
    raise ValueError("COSMOS_DATABASE_NAME environment variable is required")
if not settings.cosmos_container_name:
    raise ValueError("COSMOS_CONTAINER_NAME environment variable is required")

    
# Initialize Cosmos DB client with error handling
client: CosmosClient

if (settings.cosmos_connection_string):
    # only used for development purposes when using the emulator
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        client = CosmosClient.from_connection_string(settings.cosmos_connection_string, None, None) # type: ignore
    except AzureError as e:
        print(f"Failed to initialize Cosmos DB client from connection string: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during initialization from connection string: {e}", file=sys.stderr)
        sys.exit(1)
else:
    try:
        credential = DefaultAzureCredential()
        client = CosmosClient(settings.cosmos_account_endpoint, credential)
    except AzureError as e:
        print(f"Failed to initialize Cosmos DB client: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during initialization: {e}", file=sys.stderr)
        sys.exit(1)


