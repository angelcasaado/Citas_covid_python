"""Subclass of JsonParer for parsing inputs of get_vaccine_date"""
from uc3m_care.parser.json_parser import JsonParser
# pylint: disable-all


class CancelJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs of get_vaccine_date"""
    DATE_SIGNATURE_KEY = "date_signature"
    CANCELLATION_KEY = "cancelation_type"
    REASON_KEY = "reason"
    BAD_CANCELLATION_LABEL_ERROR = "JSON Decode Error - Wrong label"
    BAD_DATE_SIGNATURE_LABEL_ERROR = "JSON Decode Error - Wrong label"
    BAD_REASON_LABEL_ERROR = "JSON Decode Error - Wrong label"

    _JSON_KEYS = [DATE_SIGNATURE_KEY,
                   CANCELLATION_KEY,
                   REASON_KEY]# noqa
    _ERROR_MESSAGES = [BAD_DATE_SIGNATURE_LABEL_ERROR,
                        BAD_CANCELLATION_LABEL_ERROR,
                        BAD_REASON_LABEL_ERROR]# noqa
