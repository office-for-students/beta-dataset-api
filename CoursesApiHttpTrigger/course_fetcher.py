import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import sys

class CourseFetcher:

    def __init__(self, client, collection_link):
        self.client = client
        self.collection_link = collection_link

    def get_course(self, institution_id, course_id, mode, version):

        query = ("SELECT * from c "
                 f"where c.course.institution.public_ukprn = '{institution_id}' "
                 f"and c.course.kis_course_id = '{course_id}' "
                 f"and c.course.mode.code = '{mode}' "
                 f"and c.version = '{version}' ")

        print(query)

        # TODO investigate partitions and choosing the partition key
        options = { 'enableCrossPartitionQuery': True }

        result_list = list(self.client.QueryItems(self.collection_link, query, options))
        print(len(result_list))
        return result_list[0]

