import json
import logging

import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import sys


class CourseFetcher:
    """Handles retrieving courses from Cosmos DB"""

    def __init__(self, client, collection_link):
        self.client = client
        self.collection_link = collection_link

    def get_course(self, institution_id, course_id, mode, version):
        """Retrieves a course document from Cosmos DB.

        Queries the Cosmos DB container for a course using the
        arguments passed in. If a course is found, it removes
        the additonal fields Cosmos DB added before returning it
        to the caller, otherwise it returns None.

        """

        logging.info(f'client {self.client}')
        logging.info(f'client {self.collection_link}')

        # Create an SQL query to retrieve the course document
        query = (
            "SELECT * from c "
            f"where c.course.institution.public_ukprn = '{institution_id}' "
            f"and c.course.kis_course_id = '{course_id}' "
            f"and c.course.mode.code = '{mode}' "
            f"and c.version = '{version}' ")

        logging.info(f'query: {query}')

        # TODO investigate our use of partitions and the partition key
        options = {'enableCrossPartitionQuery': True}

        # Query the course container using the sql query and options
        courses_list = list(
            self.client.QueryItems(self.collection_link, query, options))

        # If no course matched the arguments passed in return None
        if not len(courses_list):
            return None

        # We don't expect more than one course to be returned so log an
        # error if it is.
        if len(courses_list) > 1:
            # Something's wrong. There should only be one matching course.
            course_count = len(courses_list)
            logging.error(
                f'{course_count} courses were returned. There should be one.')

        course = courses_list[0]
        tidied_course = CourseFetcher.tidy_course(course)
        return json.dumps(tidied_course)

    @staticmethod
    def tidy_course(course):
        """Removes the key/value pairs Cosmos DB adds to the course"""

        keys_to_delete = ['_rid', '_self', '_etag', '_attachments', '_ts']
        for key in keys_to_delete:
            try:
                del course[key]
            except KeyError:
                logging.warning(
                    f"The expected Comsos DB key was not found: {key}")
        return course

