import logging
import re

class StringValidator:
    """Validates a string meets certain criteria"""

    def __init__(self, s, min_length, max_length, regex):
        self.s = s
        self.min_length = min_length
        self.max_length = max_length
        self.regex = regex 

    @staticmethod
    def is_valid_type(obj):
        return isinstance(obj, str)

    def is_valid_length(self):
        len_of_str = len(self.s)
        if self.min_length <= len_of_str <= self.max_length:
            return True
        else:
            logging.error(f"Invalid length {len_of_str}")
            return False
            

    def valid_chars(self):
        if re.match(self.regex, self.s):
            return True
        else:
            logging.error(f'Invalid characters in string {self.s} using regex {self.regex}')
            return False


    def represents_integer(self):
        # Does the string represent an integer value
        try: 
            int(self.s)
            return True
        except ValueError:
            return False
