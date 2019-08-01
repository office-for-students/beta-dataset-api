import unittest

from institution_fetcher import InstitutionFetcher


class TestTidyInstitution(unittest.TestCase):
    def test_rid_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"_rid": "_rid_test", "version": 1}

        output_course = InstitutionFetcher.tidy_institution(input_course)
        self.assertEqual(expected_course, output_course)

    def test_self_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"_self": "_self_test", "version": 1}

        output_course = InstitutionFetcher.tidy_institution(input_course)
        self.assertEqual(expected_course, output_course)

    def test_etag_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"_etag": "_etag_test", "version": 1}

        output_course = InstitutionFetcher.tidy_institution(input_course)
        self.assertEqual(expected_course, output_course)

    def test_attachments_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"_attachments": "_attachments_test", "version": 1}

        output_course = InstitutionFetcher.tidy_institution(input_course)
        self.assertEqual(expected_course, output_course)

    def test_ts_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"_ts": "_ts_test", "version": 1}

        output_course = InstitutionFetcher.tidy_institution(input_course)
        self.assertEqual(expected_course, output_course)

    def test_institution_id_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"institution_id": "121", "version": 1}

        output_course = InstitutionFetcher.tidy_institution(input_course)
        self.assertEqual(expected_course, output_course)

    def test_with_all_keys_to_be_deleted(self):
        expected_course = {"version": 1}
        input_course = {
            "_rid": "_rid_test",
            "_self": "_self_test",
            "_etag": "_etag_test",
            "_attachments": "_attachments_test",
            "_ts": "_ts_test",
            "institution_id": "111",
            "version": 1,
        }

        output_course = InstitutionFetcher.tidy_institution(input_course)
        self.assertEqual(expected_course, output_course)
