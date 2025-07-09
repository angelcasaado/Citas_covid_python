"""Classs for the attribute FullName"""
from uc3m_care.data.attribute.attribute import Attribute

# pylint: disable=too-few-public-methods


class Reason(Attribute):
    """Classs for the attribute FullName"""
    _validation_pattern = r"^[a-zA-Z0-9\s]{2,100}$"
    _validation_error_message = "Reason invalid"
