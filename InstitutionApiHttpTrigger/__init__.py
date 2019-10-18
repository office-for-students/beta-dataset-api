import logging
import os
import traceback

import azure.functions as func


from SharedCode.utils import (
    get_collection_link,
    get_cosmos_client,
    get_http_error_response_json,
)
from SharedCode.dataset_helper import DataSetHelper

from .institution_fetcher import InstitutionFetcher
from .validators import valid_institution_params


cosmosdb_uri = os.environ["AzureCosmosDbUri"]
cosmosdb_key = os.environ["AzureCosmosDbKey"]
cosmosdb_database_id = os.environ["AzureCosmosDbDatabaseId"]
cosmosdb_inst_collection_id = os.environ["AzureCosmosDbInstitutionsCollectionId"]
cosmosdb_dataset_collection_id = os.environ["AzureCosmosDbDataSetCollectionId"]

# Intialise a cosmos db client
client = get_cosmos_client(cosmosdb_uri, cosmosdb_key)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Implements the REST API endpoint for getting an institution document.

    The endpoint implemented is:
        /institutions/{institution_id}/

    The API is documented in a swagger document.
    """

    try:
        logging.info("Process a request for an institution resource.")
        logging.info(f"url: {req.url}")
        logging.info(f"route_params: {req.route_params}")

        params = dict(req.route_params)
        logging.info(f"Parameters: {params}")

        if not valid_institution_params(params):
            logging.error(f"valid_institution_params returned false for {params}")
            return func.HttpResponse(
                get_http_error_response_json(
                    "Bad Request", "Parameter Error", "Invalid parameter passed"
                ),
                headers={"Content-Type": "application/json"},
                status_code=400,
            )

        inst_collection_link = get_collection_link(cosmosdb_database_id, cosmosdb_inst_collection_id)
        dataset_collection_link = get_collection_link(cosmosdb_database_id, cosmosdb_dataset_collection_id)

        # Initialise dataset helper - used for retrieving latest dataset version
        dsh = DataSetHelper(client, dataset_collection_link)
        version = dsh.get_highest_successful_version_number()

        # Intialise an InstitutionFetcher
        institution_fetcher = InstitutionFetcher(client, inst_collection_link)
        institution = institution_fetcher.get_institution(version=version, **params)

        if institution:
            logging.info(f"Found a institution {institution}")
            return func.HttpResponse(
                institution,
                headers={"Content-Type": "application/json"},
                status_code=200,
            )

        return func.HttpResponse(
            get_http_error_response_json(
                "Not Found", "institution", "Institution was not found."
            ),
            headers={"Content-Type": "application/json"},
            status_code=404,
        )

    except Exception as e:
        logging.error(traceback.format_exc())

        # Raise so Azure sends back the HTTP 500
        raise e
