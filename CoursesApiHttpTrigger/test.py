import azure.cosmos.errors as errors
import sys


from course_fetcher import CourseFetcher
from utils import (
    get_collection_link,
    get_cosmos_client)


client = get_cosmos_client()
collection_link = get_collection_link()

course_fetcher = CourseFetcher(client, collection_link)

# institution_id maps to public_ukpr
institution_id = '10000055'

# course_id maps to kis_course_id
course_id = 'AB37'

# mode maps to  mode.code
mode = '1'
version = '1'

result = course_fetcher.get_course(institution_id, course_id, mode, version)
print(result)
