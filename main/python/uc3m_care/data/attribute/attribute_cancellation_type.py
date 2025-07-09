"""Classs for the attribute PhoneNumber"""
from uc3m_care.data.attribute.attribute import Attribute

# pylint: disable=too-few-public-methods


class CancellationType(Attribute):
    """Classs for the attribute PhoneNumber"""
    _validation_pattern = r"(active|Temporal|Final)"
    _validation_error_message = "Cancellation type is not valid"
