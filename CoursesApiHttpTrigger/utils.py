import json
import os

import azure.cosmos.cosmos_client as cosmos_client


def get_cosmos_client():
    """Initialises and returns a Cosmos client."""

    # Get the relevant environment variables
    cosmosdb_uri = os.environ['AzureCosmosDbUri']
    cosmosdb_key = os.environ['AzureCosmosDbKey']
    master_key = 'masterKey'

    # Initialise anf return the Cosmos client
    return cosmos_client.CosmosClient(url_connection=cosmosdb_uri,
                                      auth={master_key: cosmosdb_key})


def get_collection_link():
    """Builds and returns the link for the course collection container."""

    cosmosdb_database_id = os.environ['AzureCosmosDbDatabaseId']
    cosmosdb_collection_id = os.environ['AzureCosmosDbCollectionId']
    return 'dbs/' + cosmosdb_database_id + '/colls/' + cosmosdb_collection_id


def get_not_found_json():
    """Returns a JSON object indicating 404 Not Found"""
    outer = {}
    outer["errors"] = []
    outer["errors"].append({
        'error': 'Not Found',
        'error_values': [{
            '404': 'Not Found'
        }]
    })
    return json.dumps(outer)
