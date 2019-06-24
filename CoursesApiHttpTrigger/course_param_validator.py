import logging

from .string_validator import StringValidator

def valid_course_params(params):

    # First check all params are present
    if not mandatory_params_present(
        ('institution_id', 'course_id', 'mode'), params):
        logging.error(f"Mandatory parameters missing from: {params}")
        return False

    if not valid_institution_id(params['institution_id']):
        logging.error(f"Invalid institution_id parameter: {params['institution_id']}")
        return False

    if not valid_course_id(params['course_id']):
        logging.error(f"Invalid course_id parameter: {params['course_id']}")
        return False

    if not valid_mode(params['mode']):
        return False

    if not valid_param("version", params['version'], 1, 3, r'\d{1,3}'):
        return False

    return True

def mandatory_params_present(mandatory_params, params):
    if all(k in params for k in mandatory_params):
        return True
    return False

def valid_institution_id(institution_id):
    """Test that institution looks reasonable."""

    # First check value passed in is a string
    if not StringValidator.is_valid_type(institution_id):
        logging.error("Invalid type for institution_id")
        return False

    string_validator = StringValidator(institution_id, min_length=8, max_length=8, regex=r'[\d]+$')

    # Check institution id is a valid length
    if not string_validator.is_valid_length():
        logging.error("Invalid length for institution_id: {institution_id}")
        return False
    
    # Now check the string comprises only digits 
    if not string_validator.valid_chars():
        logging.error(f"Invalid characters in institution_id: {institution_id}")
        return False

    return True


def valid_course_id(course_id):
    """Test that course id looks reasonable."""

    # Check value passed in is a string
    if not StringValidator.is_valid_type(course_id):
        logging.error(f"course_id is an invalid type - expecting string")
        return False

    # Check does the string length is valid 
    string_validator = StringValidator(course_id, min_length=0, max_length=30, regex=r'[\w-]+$')
    if not string_validator.is_valid_length():
        logging.error(f"course_id is invalid length {course_id}")
        return False
    
    # Check string contains valid characters 
    if not string_validator.valid_chars():
        logging.error(f"course_id contains invalid characters {course_id}")
        return False

    return True


def valid_mode(mode):
    """Test that mode looks reasonable."""

    # Check value passed in is a string
    if not StringValidator.is_valid_type(mode):
        logging.error(f"mode is an invalid type - expecting string")
        return False

    # Check does the string length is valid 
    string_validator = StringValidator(mode, min_length=1, max_length=1, regex=r'[123]$')
    if not string_validator.is_valid_length():
        logging.error(f"mode is invalid length {mode}")
        return False
    
    # Check string contains valid characters 
    if not string_validator.valid_chars():
        logging.error(f"mode contains invalid characters {mode}")
        return False

    return True


def valid_param(name, param, min_length, max_length, regex):
    """Test that the param looks reasonable."""

    # Check value passed in is a string
    if not StringValidator.is_valid_type(param):
        logging.error(f"{name} is an invalid type - expecting string")
        return False

    # Check the string length is valid 
    string_validator = StringValidator(param, min_length=min_length, max_length=max_length, regex=regex)
    if not string_validator.is_valid_length():
        logging.error(f"{name} is invalid length {param}")
        return False
    
    # Check string contains valid characters 
    if not string_validator.valid_chars():
        logging.error(f"{name} contains invalid characters {param}")
        return False

    return True