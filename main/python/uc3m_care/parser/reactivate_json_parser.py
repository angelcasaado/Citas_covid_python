"""Subclass of JsonParer for parsing inputs of get_vaccine_date"""
from uc3m_care.parser.json_parser import JsonParser
# pylint: disable-all


class ReactivateJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs of get_vaccine_date"""
    DATE_SIGNATURE_KEY = "date_signature"
    REACTIVATION_KEY = "reactivation_type"
    DATE_KEY = "new_date"
    BAD_DATE_SIGNATURE_LABEL_ERROR = "JSON Decode Error - Wrong signature label"
    BAD_REACTIVATION_KEY_LABEL_ERROR = "JSON Decode Error - Wrong reactivation type label"
    BAD_OPTION_LABEL_ERROR = "JSON Decode Error - Wrong day label"

    _JSON_KEYS = [DATE_SIGNATURE_KEY,
                   REACTIVATION_KEY,
                   DATE_KEY]# noqa
    _ERROR_MESSAGES = [BAD_DATE_SIGNATURE_LABEL_ERROR,
                        BAD_REACTIVATION_KEY_LABEL_ERROR,
                        BAD_OPTION_LABEL_ERROR]# noqa