import os

import azure.cosmos.cosmos_client as cosmos_client

def get_cosmos_client():
    cosmosdb_uri = os.environ['AzureCosmosDbUri']
    cosmosdb_key = os.environ['AzureCosmosDbKey']
    master_key = 'masterKey'

    return cosmos_client.CosmosClient(url_connection=cosmosdb_uri, auth={master_key: cosmosdb_key})


def get_collection_link():
    cosmosdb_database_id = os.environ['AzureCosmosDbDatabaseId']
    cosmosdb_collection_id = os.environ['AzureCosmosDbCollectionId']
    return 'dbs/' + cosmosdb_database_id + '/colls/' + cosmosdb_collection_id






