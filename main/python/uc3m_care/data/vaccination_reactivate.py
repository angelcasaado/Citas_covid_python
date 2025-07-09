"""Contains the class Vaccination Appointment"""
from datetime import datetime
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.attribute.attribute_reactivation_type import ReactivationType
from uc3m_care.data.attribute.attribute_iso_date import AppointmentIsoDate
# pylint: disable-all


class VaccinationReactivate:
    """Class VaccinationReactivate"""
    def __init__(self, date_signature, reactivation_type, fecha_vacunacion):
        self.__fecha_en_la_que_se_solicita = datetime.timestamp(datetime.today())
        self.__date_signature = DateSignature(date_signature).value
        self.__reactivation_type = ReactivationType(reactivation_type).value
        self.__fecha_vacunacion = datetime.fromisoformat(AppointmentIsoDate(fecha_vacunacion).value).timestamp()
