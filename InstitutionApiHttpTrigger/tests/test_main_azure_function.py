"""
This module contains unittests for the DataSet API get institution endpoint

"""

import json
import unittest

import azure.functions as func

from InstitutionApiHttpTrigger import main


class TestMainAzureFunction(unittest.TestCase):
    def test_with_invalid_institution_id(self):

        # Set an invalid institution_id string with 9 chars
        invalid_institution_id = "100000551"

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=None,
            url=f"/api/institutions/{invalid_institution_id}",
            params={"version": "1"},
            route_params={"institution_id": invalid_institution_id},
        )

        # Call the main Azure Function entry point with the request.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 400)

        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        self.assertEqual(error_msg["errors"][0]["error"], "Bad Request")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["Parameter Error"],
            "Invalid parameter passed",
        )


# TODO add more tests
