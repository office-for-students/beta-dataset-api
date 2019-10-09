import unittest
import os
import sys
import inspect

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from course_param_validator import valid_course_params


class TestValidCourseParams(unittest.TestCase):
    def test_when_all_params_are_valid(self):
        input_params = {
            "institution_id": "10000233",
            "course_id": "KA1003",
            "mode": "1",
        }

        output_result = valid_course_params(input_params)
        self.assertTrue(output_result)

    def test_when_institution_id_is_missing(self):
        input_params = {"course_id": "KA1003", "mode": "1"}

        output_result = valid_course_params(input_params)
        self.assertFalse(output_result)

    def test_when_course_id_is_missing(self):
        input_params = {"institution_id": "10000233", "mode": "1"}

        output_result = valid_course_params(input_params)
        self.assertFalse(output_result)

    def test_when_course_id_is_missing(self):
        input_params = {
            "institution_id": "10000233",
            "course_id": "KA1003",
            "version": "1",
        }

        output_result = valid_course_params(input_params)
        self.assertFalse(output_result)

    def test_when_course_id_contains_hyphen(self):
        input_params = {
            "institution_id": "10000233",
            "course_id": "KA1-003",
            "mode": "1",
            "version": "1",
        }

        output_result = valid_course_params(input_params)
        self.assertTrue(output_result)

    def test_when_course_id_contains_tilda(self):
        input_params = {
            "institution_id": "10000233",
            "course_id": "KA1~003",
            "mode": "1",
            "version": "1",
        }

        output_result = valid_course_params(input_params)
        self.assertTrue(output_result)

    def test_when_course_id_contains_left_circular_brace(self):
        input_params = {
            "institution_id": "10000233",
            "course_id": "KA1(003",
            "mode": "1",
            "version": "1",
        }

        output_result = valid_course_params(input_params)
        self.assertTrue(output_result)

    def test_when_course_id_contains_right_circular_brace(self):
        input_params = {
            "institution_id": "10000233",
            "course_id": "KA1)003",
            "mode": "1",
            "version": "1",
        }

        output_result = valid_course_params(input_params)
        self.assertTrue(output_result)

    def test_when_course_id_contains_exclamation_mark(self):
        input_params = {
            "institution_id": "10000233",
            "course_id": "KA1!003",
            "mode": "1",
            "version": "1",
        }

        output_result = valid_course_params(input_params)
        self.assertTrue(output_result)

    def test_when_course_id_contains_dollar_sign(self):
        input_params = {
            "institution_id": "10000233",
            "course_id": "KA1$003",
            "mode": "1",
            "version": "1",
        }

        output_result = valid_course_params(input_params)
        self.assertTrue(output_result)