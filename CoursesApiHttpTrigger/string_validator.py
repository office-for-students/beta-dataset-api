import logging
import re


class StringValidator:
    """Checks a string meets certain criteria
    
    Checks string meets caller's specified criteria
    in terms of type, length, and permitted chars. 
    """

    def __init__(self, s, min_length, max_length, regex):
        self.s = s
        self.min_length = min_length
        self.max_length = max_length
        self.regex = regex

    @staticmethod
    def is_valid_type(obj):
        return isinstance(obj, str)

    def is_valid_length(self):
        return self.min_length <= len(self.s) <= self.max_length

    def valid_chars_only(self):
        return re.match(self.regex, self.s) is not None