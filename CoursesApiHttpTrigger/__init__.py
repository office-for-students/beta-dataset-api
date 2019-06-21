import logging
import os

import azure.functions as func

from .course_fetcher import CourseFetcher

from .utils import (get_collection_link, get_cosmos_client, get_not_found_json)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Implements the REST API endpoint for getting course documents. 

    The endpoint implemented is:
        /institutions/{institution_id}/courses/{course_id}/modes/{mode} 

    The API is fully documented in a swagger document within the same repo
    as this module - https://github.com/office-for-students/beta-dataset-api
    """

    logging.info('Process a request for a course.')
    logging.info(f"url: {req.url}")
    logging.info(f"params: {req.params}")
    logging.info(f"route_params: {req.route_params}")

    # Put all the parameters together
    params = dict(req.route_params)
    version = req.params.get('version', '1')
    params['version'] = version
    logging.info(f"Parameters: {params}")

    # TODO if not validate(params):
    #   return bad request error

    # Intialise a CourseFetcher
    client = get_cosmos_client()
    collection_link = get_collection_link()
    course_fetcher = CourseFetcher(client, collection_link)

    # Get the course
    course = course_fetcher.get_course(**params)

    logging.info(type(course))
    logging.info(course)

    if course:
        return func.HttpResponse(course,
                                 headers={"Content-Type": "application/json"},
                                 status_code=200)
    else:
        return func.HttpResponse(get_not_found_json(),
                                 headers={"Content-Type": "application/json"},
                                 status_code=400)
