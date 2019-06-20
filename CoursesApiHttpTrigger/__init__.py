import logging
import os

import azure.functions as func

from .course_fetcher import CourseFetcher

from .utils import (
    get_collection_link,
    get_cosmos_client)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('id')
    logging.info(f"url is {req.url}")
    logging.info(f"params is {req.params}")
    logging.info(f"route_params is {req.route_params}")
    logging.info(type(req.route_params))
    
    params = dict(req.route_params)
    params['version'] = '1'

    #return func.HttpResponse("Hello")
    # For now set version to "1"

    client = get_cosmos_client()
    collection_link = get_collection_link()

    course_fetcher = CourseFetcher(client, collection_link)
    course = course_fetcher.get_course(**params)
    logging.info(type(course))
    logging.info(course)

    if course:
        return func.HttpResponse(course, status_code=200)
    else:
        return func.HttpResponse(
             "No course found",
             status_code=400
        )
