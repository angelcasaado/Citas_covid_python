""""Class for managing appointments based on Iso Dates"""
from datetime import datetime
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


# pylint: disable=all
class AppointmentIsoDate(Attribute):
    """"Class for managing appointments based on Iso Dates"""
    _validation_error_message = "Invalid iso date format"
    _validation_pattern = r"[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])"

    def _validate(self, attr_value: str) -> str:
        if isinstance(attr_value, str):
            attr_value = super()._validate(attr_value)
            try:
                appointment_date = datetime.fromisoformat(attr_value)
            except ValueError as value_error:
                raise VaccineManagementException("Invalid date value") from value_error

            if appointment_date.date() <= datetime.utcnow().date():
                raise VaccineManagementException("Appointment date must be later than today")
        else:
            raise VaccineManagementException(self._validation_error_message)
        return attr_value
