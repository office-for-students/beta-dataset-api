"""
This module contains functional tests for the Azure DataSet API
courses endpoint.

The tests assume that an Azure CosmosDB container has been loaded with the
courses data from HESA in JSON format.

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
export AzureCosmosDbCoursesCollectionId=""

"""


import json
import unittest
from unittest import mock

import azure.functions as func

from . import main


class TestCourseEndPoint(unittest.TestCase):
    def test_endpoint_for_existing_course(self):

        # A course that exists in the HESA dataset
        institution_id = "10000055"
        course_id = "AB37"
        mode = "1"

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": "1"},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 200)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned course.
        course = json.loads(resp.get_body().decode("utf-8"))
        self.assertEqual(
            course["course"]["institution"]["pub_ukprn"], f"{institution_id}"
        )

    def test_endpoint_for_existing_course_with_tilde_in_course_id(self):

        # A course that exists in the HESA dataset
        institution_id = "10007850"
        course_id = "UUUL1-G104~USMA-AAM15"
        mode = "1"

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": "1"},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 200)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned course.
        course = json.loads(resp.get_body().decode("utf-8"))
        self.assertEqual(
            course["course"]["institution"]["pub_ukprn"], f"{institution_id}"
        )

    def test_endpoint_for_non_existing_course(self):

        institution_id = "10000055"
        course_id = "BLAH"  # This course does not exist
        mode = "1"

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": "1"},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
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
        print(error_msg)
        self.assertEqual(error_msg["errors"][0]["error"], "Not Found")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["course"], "Course was not found."
        )

    def test_endpoint_with_invalid_length_institution_id(self):

        institution_id = "123456789"  # one char too long
        course_id = "AB37"
        mode = "1"

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": "1"},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 400)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        print(error_msg)
        self.assertEqual(error_msg["errors"][0]["error"], "Bad Request")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["Parameter Error"],
            "Invalid parameter passed",
        )

    def test_endpoint_with_invalid_char_institution_id(self):

        institution_id = "1000005;"  # semicolons are invalid in institution ids
        course_id = "AB37"
        mode = "1"

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": "1"},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 400)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        print(error_msg)
        self.assertEqual(error_msg["errors"][0]["error"], "Bad Request")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["Parameter Error"],
            "Invalid parameter passed",
        )

    def test_endpoint_with_invalid_length_course_id(self):

        institution_id = "10000055"
        course_id = "1234567890123456789012345678901"  # Should be no more than 30 chars
        mode = "1"

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": "1"},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 400)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        print(error_msg)
        self.assertEqual(error_msg["errors"][0]["error"], "Bad Request")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["Parameter Error"],
            "Invalid parameter passed",
        )

    def test_endpoint_with_invalid_char_course_id(self):

        institution_id = "10000055"
        course_id = "AB37;"  # semicolon is an invalid char for course id
        mode = "1"

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": "1"},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 400)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        print(error_msg)
        self.assertEqual(error_msg["errors"][0]["error"], "Bad Request")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["Parameter Error"],
            "Invalid parameter passed",
        )

    def test_endpoint_with_invalid_char_semicolon_mode(self):

        institution_id = "10000055"
        course_id = "AB37"
        mode = ";"  # semicolon is an invalid char for mode

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": "1"},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 400)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        print(error_msg)
        self.assertEqual(error_msg["errors"][0]["error"], "Bad Request")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["Parameter Error"],
            "Invalid parameter passed",
        )

    def test_endpoint_with_invalid_value_one_mode(self):

        institution_id = "10000055"
        course_id = "AB37"
        mode = "one"  # one is an invalid for for mode

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": "1"},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 400)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        print(error_msg)
        self.assertEqual(error_msg["errors"][0]["error"], "Bad Request")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["Parameter Error"],
            "Invalid parameter passed",
        )

    def test_endpoint_with_invalid_char_4_mode(self):

        institution_id = "10000055"
        course_id = "AB37"
        mode = "4"  # 4 is an invalid char for mode

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": "1"},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 400)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        print(error_msg)
        self.assertEqual(error_msg["errors"][0]["error"], "Bad Request")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["Parameter Error"],
            "Invalid parameter passed",
        )

    def test_endpoint_with_invalid_char_semicolon_version(self):

        institution_id = "10000055"
        course_id = "AB37"
        mode = "1"
        version = ";"  # semicolon is an invalid char for version

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{institution_id}/courses/{course_id}/modes/{mode}",
            params={"version": version},
            route_params={
                "institution_id": institution_id,
                "course_id": course_id,
                "mode": mode,
            },
        )

        # Call the function for the endpoint.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 400)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        print(error_msg)
        self.assertEqual(error_msg["errors"][0]["error"], "Bad Request")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["Parameter Error"],
            "Invalid parameter passed",
        )

    # TODO add more tests
