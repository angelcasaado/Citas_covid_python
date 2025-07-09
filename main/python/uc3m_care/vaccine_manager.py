"""Module """

from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.vaccination_appointment import VaccinationAppointment

# pylint: disable-all


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    # pylint: disable=invalid-name
    class __VaccineManager:
        def __init__(self):
            pass

        # pylint: E265
        #pylint: disable=too-many-arguments# noqa
        # pylint: disable=no-self-use# noqa
        def request_vaccination_id(self, patient_id, name_surname, registration_type, phone_number, age):# noqa
            """Register the patinent into the patients file"""
            my_patient = VaccinePatientRegister(patient_id,
                                                    name_surname,# noqa
                                                    registration_type,# noqa
                                                    phone_number,# noqa
                                                    age)# noqa

            my_patient.save_patient()
            return my_patient.patient_sys_id

        def get_vaccine_date(self, input_file, date): # noqa
            """Gets an appointment for a registered patient"""
            my_sign = VaccinationAppointment.create_appointment_from_json_file(input_file, date)
            #save the date in store_date.json # noqa
            my_sign.save_appointment()
            return my_sign.date_signature

        def vaccine_patient(self, date_signature):# noqa
            """Register the vaccination of the patient"""
            appointment = VaccinationAppointment.get_appointment_from_date_signature(date_signature)
            return appointment.register_vaccination()

        def cancel_appointment(self, input_file):# noqa
            """Cancel de appointment received in the input file"""
            appointment = VaccinationAppointment.cancel_appointnmet_from_cancel_file(input_file)
            return appointment.date_signature


        def reactivate_appointment(self, FilePath):# noqa
            """Reactiva una cita"""
            date_signature = VaccinationAppointment.reactive_with_json(self, FilePath)
            return date_signature

    instance = None

    def __new__(cls):
        if not VaccineManager.instance:
            VaccineManager.instance = VaccineManager.__VaccineManager()
        return VaccineManager.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
