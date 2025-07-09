"""Tests for cancel_appointment method"""
import unittest
from unittest import TestCase
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_PATH, JSON_FILES_RF2_PATH
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore
# pylint: disable-all

param_list_nok = [("REV 1",
                   "clave_date_signature_duplicada.json",
                   "JSON Decode Error - Wrong label"),
                    ("REV 3",
                     "clave_date_signature_eliminada.json",
                     "JSON Decode Error - Wrong label"),
                    ("REV 4",
                     "opening_brace_modified.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 5",
                     "clave_date_signature_modificada.json",
                     "JSON Decode Error - Wrong label"),
                    ("REV 6",
                     "reason_duplicado.json",
                     "JSON Decode Error - Wrong label"),
                    ("REV 7",
                     "closing_brace_modified.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 8",
                     "reason_eliminado.json",
                     "JSON Decode Error - Wrong label"),
                    ("REV 9",
                     "colon_date_signature_duplidado.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 10",
                     "reason_modificado.json",
                     "JSON Decode Error - Wrong label"),
                    ("REV 11",
                     "colon_date_signature_eliminado.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 12",
                     "reason_value_eliminado.json",
                     "Reason invalid"),
                    ("REV 13",
                     "colon_date_signature_modificada.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 14",
                     "reason_value_modificado.json",
                     "Reason invalid"),
                    ("REV 15",
                     "coma_date_signature_duplicado.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 16",
                     "remove.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 17",
                     "coma_date_signature_eliminado.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 18",
                     "remove_ending_brace.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 19",
                     "coma_date_signature_modificado.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 20",
                     "remove_date_signature_line.json",
                     "JSON Decode Error - Wrong label"),
                    ("REV 21",
                     "comilla2_date_signature_duplidada.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 22",
                     "remove_reason_line.json",  "JSON Decode Error - Wrong JSON Format"),
                    ("REV 23",
                     "comilla2_date_signature_eliminada.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 24",
                     "remove_cancellation_line_valid.json",
                     "JSON Decode Error - Wrong label"),
                    ("REV 25",
                     "comilla2_date_signature_modificada.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 26",
                     "cancellation_duplicado.json",
                     "JSON Decode Error - Wrong label"),
                    ("REV 27",
                     "comilla2_valor_date_signature_duplicado.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 28",
                     "cancellation_eliminado.json",
                     "JSON Decode Error - Wrong label"),
                    ("REV 29",
                     "comilla2_valor_date_signature_eliminado.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 30",
                     "cancellation_modificado.json",
                     "JSON Decode Error - Wrong label"),
                    ("REV 31",
                     "comilla2_valor_date_signature_modificado.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 32",
                     "cancellation_value_duplicado.json",
                     "Cancellation type is not valid"),
                    ("REV 33",
                     "comilla_date_signature_duplidada.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 34",
                     "cancellation_value_eliminado.json",
                     "Cancellation type is not valid"),
                    ("REV 35",
                     "comilla_date_signature_eliminada.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 37",
                     "comilla_date_signature_modificada.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 38",
                     "cancellation_value_modificado.json",
                     "Cancellation type is not valid"),
                    ("REV 39",
                     "comilla_valor_date_signature_duplicado.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 41",
                     "comilla_valor_date_signature_eliminado.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 42",
                     "root_duplicated.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 43",
                     "comilla_valor_date_signature_modificada.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 44",
                     "root_empty.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 45",
                     "duplicate.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 46",
                     "valor_date_signature_duplicado.json",
                     "date_signature format is not valid"),
                    ("REV 47",
                     "duplicate_ending_brace.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 48",
                     "valor_date_signature_eliminado.json",
                     "date_signature format is not valid"),
                    ("REV 50",
                     "valor_date_signature_modificado.json",
                     "date_signature format is not valid")
                  ]# noqa


class TestCancelAppointment(TestCase):
    """test class for open_door"""
    # pylint: disable=no-member

    @freeze_time("2022-03-08")
    def setUp(self) -> None:
        """Removing the Stores and creating required AccessRequest for testing"""
        # first af all, i introduce all value tha I need for the structural testing
        # remove the old storeKeys
        # print("Setup")
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        my_manager.get_vaccine_date(file_test, "2022-03-18")

    @freeze_time("2022-03-17")
    def test_parametrized_cases_tests(self):
        """Parametrized cases"""
        my_manager = VaccineManager()
        for test_id, file_test, result in param_list_nok:
            file_name = JSON_FILES_PATH + "cancel_files/" + file_test
            print("Param:" + test_id + "-")
            with self.assertRaises(VaccineManagementException) as c_m:
                my_manager.cancel_appointment(file_name)
            self.assertEqual(c_m.exception.message, result)

    @freeze_time("2022-03-17")
    def test_cancel_invalid_regex(self):
        """path: regex is not valid , key length is 63 chars"""
        my_file = JSON_FILES_PATH + "cancel_files/" + "cancel_appointment_invalid.json"
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(my_file)
        self.assertEqual("date_signature format is not valid", c_m.exception.message)

    @freeze_time("2022-03-17")
    def test_cancel_invalid_cancellation(self):
        """path: cancellation is not valid """
        my_file = JSON_FILES_PATH + "cancel_files/" + "cancel_cancellation_type_invalid.json"
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(my_file)
        self.assertEqual("Cancellation type is not valid", c_m.exception.message)

    @freeze_time("2022-03-17")
    def test_cancel_invalid_reason(self):
        """path: cancellation is not valid """
        my_file = JSON_FILES_PATH + "cancel_files/" + "cancel_reason_invalid.json"
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(my_file)
        self.assertEqual("Reason invalid", c_m.exception.message)

    @freeze_time("2022-03-17")
    def test_cancel_temporal_ok(self):
        """path: regex ok , key is found , key is not expired, guest"""
        my_file = JSON_FILES_PATH + "cancel_files/" + "cancel_temporal.json"
        my_manager = VaccineManager()
        result = my_manager.cancel_appointment(my_file)
        self.assertEqual("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", result)
        keys_store = AppointmentsJsonStore()
        cancelled_key = keys_store.find_item(
            "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(cancelled_key["_VaccinationAppointment__cancelled"], "Temporal")

    @freeze_time("2022-03-17")
    def test_cancel_final_ok(self):
        """path:  key is found , key is not expired, guest"""
        my_file = JSON_FILES_PATH + "cancel_files/" + "cancel_final.json"
        my_manager = VaccineManager()
        result = my_manager.cancel_appointment(my_file)
        self.assertEqual("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", result)
        keys_store = AppointmentsJsonStore()
        cancelled_key = keys_store.find_item(
            "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(cancelled_key["_VaccinationAppointment__cancelled"], "Final")

    @freeze_time("2022-03-18")
    def test_cancel_invalid_date_signature_expired_today(self):
        """Testing the cancellation of an expired key"""
        my_file = JSON_FILES_PATH + "cancel_files/"+"cancel_final.json"
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(my_file)
        self.assertEqual("The appointment cannot be cancelled today", c_m.exception.message)

    @freeze_time("2022-03-19")
    def test_cancel_invalid_date_signature_expired_tomorrow(self):
        """Testing the cancellation of an expired key"""
        my_file = JSON_FILES_PATH + "cancel_files/" + "cancel_final.json"
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(my_file)
        self.assertEqual("The appointment cannot be cancelled today", c_m.exception.message)

    @freeze_time("2022-03-17")
    def test_cancel_invalid_date_signature_already_cancelled(self):
        """"Testing the cancellation of an invalid key"""
        my_file = JSON_FILES_PATH + "cancel_files/" + "cancel_temporal.json"
        my_manager = VaccineManager()
        my_manager.cancel_appointment(my_file)
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(my_file)
        self.assertEqual("Vaccine already cancelled",
                         c_m.exception.message)


if __name__ == '__main__':
    unittest.main()
