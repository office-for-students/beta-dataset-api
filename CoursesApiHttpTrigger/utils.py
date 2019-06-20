import azure.cosmos.cosmos_client as cosmos_client

def get_cosmos_client():
    cosmosdb_uri = "https://unistats-az-cosdb.documents.azure.com:443"
    cosmosdb_key = "nP3OSRGya4F6OOHS9u1qIO9qZAMSHEh0ZZjnzsmxoK69pnJPrdGKhVQjnz1Qd0FJxmTaTPmUtPlcaCoUkPBpDg=="
    master_key = 'masterKey'

    return cosmos_client.CosmosClient(url_connection=cosmosdb_uri, auth={master_key: cosmosdb_key})


def get_collection_link():
    cosmosdb_database_id = "phil-unistats"
    cosmosdb_collection_id = "courses"
    return 'dbs/' + cosmosdb_database_id + '/colls/' + cosmosdb_collection_id



