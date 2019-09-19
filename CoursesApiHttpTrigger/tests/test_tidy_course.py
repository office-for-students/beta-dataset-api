import unittest
import os
import sys
import inspect

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from course_fetcher import CourseFetcher


class TestTidyCourse(unittest.TestCase):
    def test_rid_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"_rid": "_rid_test", "version": 1}

        output_course = CourseFetcher.tidy_course(input_course)
        self.assertEqual(expected_course, output_course)

    def test_self_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"_self": "_self_test", "version": 1}

        output_course = CourseFetcher.tidy_course(input_course)
        self.assertEqual(expected_course, output_course)

    def test_etag_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"_etag": "_etag_test", "version": 1}

        output_course = CourseFetcher.tidy_course(input_course)
        self.assertEqual(expected_course, output_course)

    def test_attachments_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"_attachments": "_attachments_test", "version": 1}

        output_course = CourseFetcher.tidy_course(input_course)
        self.assertEqual(expected_course, output_course)

    def test_ts_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"_ts": "_ts_test", "version": 1}

        output_course = CourseFetcher.tidy_course(input_course)
        self.assertEqual(expected_course, output_course)

    def test_institution_id_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"institution_id": "121", "version": 1}

        output_course = CourseFetcher.tidy_course(input_course)
        self.assertEqual(expected_course, output_course)

    def test_course_id_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"course_id": "231g31rkj", "version": 1}

        output_course = CourseFetcher.tidy_course(input_course)
        self.assertEqual(expected_course, output_course)

    def test_course_mode_is_deleted(self):
        expected_course = {"version": 1}
        input_course = {"course_mode": "1", "version": 1}

        output_course = CourseFetcher.tidy_course(input_course)
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
            "course_id": "4r4t5",
            "course_mode": "1",
            "version": 1,
        }

        output_course = CourseFetcher.tidy_course(input_course)
        self.assertEqual(expected_course, output_course)
