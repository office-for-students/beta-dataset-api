import logging
import os
import traceback

import azure.functions as func

from .institution_fetcher import InstitutionFetcher

from .utils import get_collection_link, get_cosmos_client, get_http_error_response_json

from validators import valid_institution_params


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Implements the REST API endpoint for getting an institution document.

    The endpoint implemented is:
        /institutions/{institution_id}/

    The API is documented in a swagger document.
    """

    try:
        logging.info("Process a request for an institution resource.")
        logging.info(f"url: {req.url}")
        logging.info(f"params: {req.params}")
        logging.info(f"route_params: {req.route_params}")

        # Put all the parameters together
        params = dict(req.route_params)
        version = req.params.get("version", "1")
        params["version"] = version
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

        logging.info("The parameters look good")

        # Intialise an InstitutionFetcher
        client = get_cosmos_client()
        collection_link = get_collection_link()
        institution_fetcher = InstitutionFetcher(client, collection_link)

        # Get the institution
        institution = institution_fetcher.get_institution(**params)

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
