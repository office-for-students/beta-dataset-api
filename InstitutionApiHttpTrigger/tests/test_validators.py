import unittest

from validators import mandatory_params_present


class TestMandatoryParamsPresent(unittest.TestCase):
    def test_with_mandatory_params_preset(self):
        mandatory_params = ("institution_id",)
        params = {"institution_id": "10001234"}
        self.assertTrue(mandatory_params_present(mandatory_params, params))


# TODO Test more of the functionality

if __name__ == "__main__":
    unittest.main()
