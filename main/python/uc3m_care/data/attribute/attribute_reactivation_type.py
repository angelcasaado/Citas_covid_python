"""Attrobute new date"""
from uc3m_care.data.attribute.attribute import Attribute

# pylint: disable=too-few-public-methods


class ReactivationType(Attribute):
    """Classs for the attribute PhoneNumber"""
    _validation_pattern = r"(Normal|NewDate)"
    _validation_error_message = "Reactivation label is not valid"
