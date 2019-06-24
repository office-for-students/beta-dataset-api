"""
This module contains unittests for the Azure DataSet course 
function.

The tests assume that a container has been loaded with the
JSON course data. They could be extended to create
a container and load it with course data.

To run these tests:

    * export your Azure test environment variables (see below)
    * make sure the Python package nose is installed
    * type nosetests on the command line

Setting up your environment variables:
--------------------------------------
NOTE: Do NOT add any Azure config data to source control!

Run the export commands below with Azure test config
data set for the values of the environment variables.

export AzureCosmosDbUri=""
export AzureCosmosDbKey=""
export AzureCosmosDbDatabaseId=""
export AzureCosmosDbCollectionId=""

TODO: Update so reads values from local.settings.json
"""

import json
import unittest
from unittest import mock

import azure.functions as func

from . import main


class TestCourseEndPoint(unittest.TestCase):

    def test_endpoint_for_existing_course(self):
        """Call the endpoint for course that exists"""
        # A course that exists in the HESA dataset
        institution_id = '10000055'
        course_id = 'AB37'
        mode = '1'

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='GET',
            body=None,
            url=
            f'/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}',
            params={'version': '1'},
            route_params={
                'institution_id': institution_id,
                'course_id': course_id,
                'mode': mode
            })

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 200)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers['content-type'], 'application/json')

        # Do some checking of the returned course.
        course = json.loads(resp.get_body().decode('utf-8'))
        self.assertEqual(course['course']['institution']['public_ukprn'], f"{institution_id}")


    def test_endpoint_for_non_existing_course(self):
        """Call the endpoint for course that does not exist"""

        # A course that does not exists in the HESA dataset
        institution_id = '100000'
        course_id = 'BLAH'
        mode = '1'

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='GET',
            body=None,
            url=
            f'/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}',
            params={'version': '1'},
            route_params={
                'institution_id': institution_id,
                'course_id': course_id,
                'mode': mode
            })

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 404)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers['content-type'], 'application/json')

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode('utf-8'))
        print(error_msg)
        self.assertEqual(error_msg['errors'][0]["error"], "Not Found")
        self.assertEqual(error_msg['errors'][0]["error_values"][0]['404'], 'Not Found')


    # TODO add more tests
