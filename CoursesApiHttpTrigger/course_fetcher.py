import json
import logging

import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import sys

class CourseFetcher:

    def __init__(self, client, collection_link):
        self.client = client
        self.collection_link = collection_link

    def get_course(self, institution_id, course_id, mode, version):

        logging.info(f'get_course {institution_id}')
        logging.info(f'client {self.client}')
        logging.info(f'client {self.collection_link}')

        query = ("SELECT * from c "
                 f"where c.course.institution.public_ukprn = '{institution_id}' "
                 f"and c.course.kis_course_id = '{course_id}' "
                 f"and c.course.mode.code = '{mode}' "
                 f"and c.version = '{version}' ")

        logging.info(f'query: {query}')

        # TODO investigate partitions and choosing the partition key
        options = { 'enableCrossPartitionQuery': True }

        results_list = list(self.client.QueryItems(self.collection_link, query, options))
        if not(len(results_list)):
            return None

        # TODO: alert here if more than one result
        return json.dumps(results_list[0])

