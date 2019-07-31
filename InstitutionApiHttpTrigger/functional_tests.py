"""
This module contains functional tests for the Azure DataSet API
institutions endpoint.

The tests assume that an Azure CosmosDB container has been loaded with the
institution data from HESA in JSON format.

To run these tests:

    * export your Azure environment variables (see below)
    * type the following command:
        pytest -v functional_tests.py

Setting up your environment variables:
--------------------------------------
NOTE: Do NOT add any Azure config data to source control!

Set the following environment variables for the Azure environment
hosting the container with the Institution data.

export AzureCosmosDbUri=""
export AzureCosmosDbKey=""
export AzureCosmosDbDatabaseId=""
export AzureCosmosDbInstitutionsCollectionId=""

"""

import json
import unittest

import azure.functions as func

from . import main


class TestCourseEndPoint(unittest.TestCase):
    def test_endpoint_for_existing_course(self):

        # A course that exists in the HESA dataset
        institution_id = "10007857"

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}",
            params={"version": "1"},
            route_params={"institution_id": institution_id},
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 200)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Get the returned institution doc
        institution = json.loads(resp.get_body().decode("utf-8"))

        # Check it has the expected number of courses
        expected_total_number_of_courses = 413
        self.assertEqual(
            institution["institution"]["total_number_of_courses"],
            expected_total_number_of_courses,
        )

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

    def test_endpoint_for_non_existing_course(self):

        institution_id = "01135813"

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}",
            params={"version": "1"},
            route_params={"institution_id": institution_id},
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 404)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        self.assertEqual(error_msg["errors"][0]["error"], "Not Found")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["institution"],
            "Institution was not found.",
        )


# TODO add more tests
