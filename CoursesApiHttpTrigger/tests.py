"""
This module contains unittests for the Azure function.
To run these tests, setup your environment variables and
type nosetests on the command line.

"""
import json
import unittest
from unittest import mock

import azure.functions as func

from . import main


class TestCourseEndPoint(unittest.TestCase):

    def test_endpoint_with_real_course_arguments(self):

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
                'institution_id': '10000055',
                'course_id': 'AB37',
                'mode': '1'
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
        print('info:', course['course']['institution']['public_ukprn'])
        self.assertEqual(course['course']['institution']['public_ukprn'], f"{institution_id}")

    # TODO add more tests
