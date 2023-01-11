import w3lib.html
import re
class common_utils(object):

    @staticmethod
    def format_string(to_normalise):
        normalised = w3lib.html.strip_html5_whitespace(to_normalise)
        return normalised

    @staticmethod
    def get_int_from_string(string_value):
        int_list = re.findall("[-+]?\d*\.\d+|\d+", string_value)
        if int_list:
            return int(int_list[0])
        else:
            return None


