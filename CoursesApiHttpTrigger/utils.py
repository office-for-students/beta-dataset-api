import json
import os

import azure.cosmos.cosmos_client as cosmos_client


def get_cosmos_client():
    """Initialises and returns a Cosmos client."""

    # Get the relevant environment variables
    cosmosdb_uri = os.environ['AzureCosmosDbUri']

    # This should use the read only key (least privilege)
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


def get_http_error_response_json(error_title, error_key, error_value):
    """Returns a JSON object indicating an Http Error"""
    outer = {}
    outer["errors"] = []
    outer["errors"].append({
        'error': error_title,
        'error_values': [{
            error_key: error_value
        }]
    })
    return json.dumps(outer)