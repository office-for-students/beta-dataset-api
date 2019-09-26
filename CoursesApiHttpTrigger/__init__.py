import logging
import os
import traceback
import azure.functions as func

from .course_fetcher import CourseFetcher


from SharedCode.utils import (
    get_collection_link,
    get_cosmos_client,
    get_http_error_response_json,
)
from SharedCode.dataset_helper import DataSetHelper

from .course_param_validator import valid_course_params


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Implements the REST API endpoint for getting course documents.

    The endpoint implemented is:
        /institutions/{institution_id}/courses/{course_id}/modes/{mode}

    The API is fully documented in a swagger document in the same repo
    as this module.
    """

    try:
        logging.info("Process a request for a course.")
        logging.info(f"url: {req.url}")
        logging.info(f"route_params: {req.route_params}")

        # Put all the parameters together
        params = dict(req.route_params)
        dsh = DataSetHelper()
        version = dsh.get_highest_successful_version_number()

        #
        # The params are used in DB queries, so let's do
        # some basic sanitisation of them.
        #
        if not valid_course_params(params):
            logging.error(f"valid_course_params returned false for {params}")
            return func.HttpResponse(
                get_http_error_response_json(
                    "Bad Request", "Parameter Error", "Invalid parameter passed"
                ),
                headers={"Content-Type": "application/json"},
                status_code=400,
            )

        logging.info("The parameters look good")

        # Intialise a CourseFetcher
        client = get_cosmos_client()
        collection_link = get_collection_link(
            "AzureCosmosDbDatabaseId", "AzureCosmosDbCoursesCollectionId"
        )
        course_fetcher = CourseFetcher(client, collection_link)

        # Get the course
        course = course_fetcher.get_course(version=version, **params)

        if course:
            return func.HttpResponse(
                course, headers={"Content-Type": "application/json"}, status_code=200
            )
        else:
            return func.HttpResponse(
                get_http_error_response_json(
                    "Not Found", "course", "Course was not found."
                ),
                headers={"Content-Type": "application/json"},
                status_code=404,
            )

    except Exception as e:
        logging.error(traceback.format_exc())

        # Raise so Azure sends back the HTTP 500
        raise e
