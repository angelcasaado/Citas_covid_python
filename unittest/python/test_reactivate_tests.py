"""Test reactivate """
from unittest import TestCase
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_PATH, JSON_FILES_RF2_PATH
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore
from uc3m_care import VaccinationJsonStore
from uc3m_care.storage.petition_store import PetitionStore
from datetime import datetime
# pylint: disable-all


class TestCancelAppointment(TestCase):

    @freeze_time("2022-07-08")
    def setUp(self) -> None:
        file_test = JSON_FILES_RF2_PATH + "test_ok_4.json"
        file_test_2 = JSON_FILES_RF2_PATH + "test_ok_3.json"
        file_test_3 = JSON_FILES_PATH + "/cancel_files/cancel_final_reactivate_test.json"
        file_test_4 = JSON_FILES_PATH + "/cancel_files/cancel_final_reactivate_test_2.json"
        file_test_5 = JSON_FILES_RF2_PATH + "test_ok_5.json"
        patient_store = PatientsJsonStore()
        date_store = AppointmentsJsonStore()
        vaccined_store = VaccinationJsonStore()
        peticiones = PetitionStore()
        patient_store.empty_json_file()
        date_store.empty_json_file()
        vaccined_store.empty_json_file()
        peticiones.empty_json_file()
        vaccine_manager = VaccineManager()
        vaccine_manager.request_vaccination_id("a729d963-e0dd-47d0-8bc6-b6c595ad0098", "m m", "Regular",
                "+44333456789", "124")# noqa
        vaccine_manager.request_vaccination_id("cde0bc01-5bc7-4c0c-90d6-94c9549e6abd",
                                               "minombre tiene dosblancos", "Regular",
                "+34333456789", "125")# noqa
        vaccine_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9", "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")# noqa

        vaccine_manager.get_vaccine_date(file_test, "2022-07-20")
        vaccine_manager.get_vaccine_date(file_test_2, "2022-07-20")
        vaccine_manager.get_vaccine_date(file_test_5, "2022-07-20")
        vaccine_manager.cancel_appointment(file_test_3)
        vaccine_manager.cancel_appointment(file_test_4)
        PetitionStore().delete_json_file()

    @freeze_time("2022-07-18")
    def test_ok_newDay(self):
        """Probamos cambiando la fecha"""
        manager = VaccineManager()
        hash_1 = PetitionStore().data_hash()
        path = JSON_FILES_PATH + "/reactivate/reactivate_ok.json"
        valor_devuelto = manager.reactivate_appointment(path)
        appointments = AppointmentsJsonStore()
        appointments.load()
        data_list = appointments._data_list
        self.assertEqual(len(data_list), 3)
        nuevo_date_signature = "658a6f1d4d1fd3185fb7303debdc04248e9ada1ff19ba7648ae38cde85fe65e1"
        # El valor que nos devuelve, tiene que ser el date_signature nuevo que se ha generado
        self.assertEqual(valor_devuelto, nuevo_date_signature)
        item_appointment = appointments.find_item(nuevo_date_signature)
        justnow = datetime.utcnow()
        petition_store = PetitionStore()
        store_petition_item = petition_store.find_item(nuevo_date_signature)
        fecha_vacunacion_en_peticion = store_petition_item["_VaccinationReactivate__fecha_vacunacion"]
        date_signature_peticion = store_petition_item["_VaccinationReactivate__date_signature"]
        self.assertEqual(item_appointment["_VaccinationAppointment__issued_at"], datetime.timestamp(justnow))
        self.assertEqual(item_appointment["_VaccinationAppointment__cancelled"], "active")
        self.assertEqual(item_appointment["_VaccinationAppointment__appointment_date"], 1660953600.0)
        self.assertEqual(item_appointment["_VaccinationAppointment__reason_to_cancel"], "")
        self.assertEqual(fecha_vacunacion_en_peticion, 1660953600.0)
        self.assertEqual(nuevo_date_signature, date_signature_peticion)
        hash_2 = PetitionStore().data_hash()
        self.assertFalse(hash_1 == hash_2)

    @freeze_time("2022-07-18")
    def test_ok_normal(self):
        """Probamos una reactivación de tipo normal"""
        manager = VaccineManager()
        hash_1 = PetitionStore().data_hash()
        path = JSON_FILES_PATH + "/reactivate/reactivate_ok_2.json"
        valor_devuelto = manager.reactivate_appointment(path)
        date_signature = "a14ff4cfeca79779e9c1096efe28efbd2845ccae9cbbb1ffc77e39bc6bc4e2d3"
        appointments = AppointmentsJsonStore()
        appointments.load()
        appointments_list = appointments._data_list
        self.assertEqual(len(appointments_list), 3)
        item_appointment = appointments.find_item(date_signature)
        item_petition = PetitionStore().find_item(date_signature)
        appointmen_in_petition = item_petition["_VaccinationReactivate__fecha_vacunacion"]
        self.assertEqual(item_appointment["_VaccinationAppointment__cancelled"], "active")
        self.assertEqual(item_appointment["_VaccinationAppointment__appointment_date"], 1658275200.0)
        self.assertEqual(item_appointment["_VaccinationAppointment__reason_to_cancel"], "")
        self.assertEqual(appointmen_in_petition, 1658275200.0)
        self.assertEqual(valor_devuelto, date_signature)
        hash_2 = PetitionStore().data_hash()
        self.assertFalse(hash_1 == hash_2)

    @freeze_time("2022-07-19")
    def test_date_was_active_normal(self):
        """Comprobamos una cita que este activa, y que ha cambiamos el date_signature además de la fecha"""
        manager = VaccineManager()
        date_signature = "982f4c73f42257db7e31f74c4d7d29ec6df8095b30d52928b54697046722f331"
        hash1 = PetitionStore().data_hash()
        path = JSON_FILES_PATH + "/reactivate/reactivate_ok_5.json"
        date_signare_devuelto = manager.reactivate_appointment(path)
        item = AppointmentsJsonStore().find_item(date_signature)
        item_petition = PetitionStore().find_item(date_signature)
        reason_to_cancel = item["_VaccinationAppointment__cancelled"]
        second_appointment = item["_VaccinationAppointment__appointment_date"]
        message = item["_VaccinationAppointment__reason_to_cancel"]
        appointmen_in_petition = item_petition["_VaccinationReactivate__fecha_vacunacion"]
        hash2 = PetitionStore().data_hash()
        self.assertEqual(second_appointment, 1658275200.0)
        self.assertEqual(appointmen_in_petition, 1658275200.0)
        self.assertEqual(date_signature, date_signare_devuelto)
        self.assertEqual(reason_to_cancel, "active")
        self.assertEqual(message, "")
        self.assertFalse(hash1 == hash2)

    @freeze_time("2022-07-19")
    def test_date_was_active_newDate(self):
        """Comprobamos una cita que este activa se le cambie fecha"""
        hash1 = PetitionStore().data_hash()
        manager = VaccineManager()
        signature_expected = "4bf4f9e63f393b0014329bc89814b69140a1b48f6c4082c078432b2a4253db6e"
        path = JSON_FILES_PATH + "/reactivate/reactivate_ok_6.json"
        valor_devuelto = manager.reactivate_appointment(path)
        self.assertEqual(valor_devuelto, signature_expected)
        item = AppointmentsJsonStore().find_item(signature_expected)
        second_signature = item["_VaccinationAppointment__date_signature"]
        second_appointment = item["_VaccinationAppointment__appointment_date"]
        message = item["_VaccinationAppointment__reason_to_cancel"]
        hash2 = PetitionStore().data_hash()
        # Ahora el date_signature ha cambiado y la fecha tambien
        self.assertEqual(second_appointment, 1692489600.0)
        self.assertEqual(second_signature, signature_expected)
        self.assertEqual(message, "")
        self.assertTrue(hash1 != hash2)

    @freeze_time("2022-07-18")
    def test_no_ok_date_0(self):
        """Probamos fecha "2022-07-18 (valor límite)"""
        manager = VaccineManager()
        expected_value = "Appointment date must be later than today"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/reactivate_no_ok_0.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-18")
    def test_ok_date(self):
        """Probamos con la fecha posterior a hoy (la primera válida) 2022-07-19"""
        manager = VaccineManager()
        manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/reactivate_ok_date.json")
        # Como vemos no salta error

    @freeze_time("2022-07-18")
    def test_no_ok_date_1(self):
        """Probamos fecha "2022-07-18 ya no válida por el dia de hoy"""
        manager = VaccineManager()
        expected_value = "Invalid iso date format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/reactivate_no_ok_1.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-18")
    def test_no_ok_date_2(self):
        """Probamos fecha "2022-7-22"""
        manager = VaccineManager()
        expected_value = "Invalid iso date format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/reactivate_no_ok_2.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-18")
    def test_no_ok_date_3(self):
        """Probamos fecha "2022/07/32"""
        manager = VaccineManager()
        expected_value = "Invalid iso date format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/reactivate_no_ok_3.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-18")
    def test_no_ok_date_4(self):
        """Probamos fecha 2022-13-18"""
        manager = VaccineManager()
        expected_value = "Invalid iso date format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/reactivate_no_ok_4.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-18")
    def test_input_file_no_exist(self):
        """Probamos a darle una direccion que no existe"""
        manager = VaccineManager()
        expected_value = "File is not found"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/NO_EXISTE.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-18")
    def test_appointment_doesnt_exist(self):
        """La cita no existe"""
        manager = VaccineManager()
        expected_value = "La cita no existe"
        store_appointment = AppointmentsJsonStore()
        store_appointment.delete_json_file()
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/reactivate_ok_2.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-20")
    def test_appointment_was_vaccined(self):
        """Intentamos recuperar una cita de un paciente que ya ha sido vacunado"""
        manager = VaccineManager()
        date_signature_del_paciente = "982f4c73f42257db7e31f74c4d7d29ec6df8095b30d52928b54697046722f331"
        manager.vaccine_patient(date_signature_del_paciente)
        expected_value = "El paciente ya está vacunado"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/reactivate_ok_3.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-20")
    def test_appointment_is_timed_out(self):
        """Intentamos recuperar una cita caducada, para ello hemos cambiado la fecha congelada, contamos con que
        el día en el que nos encontramos cuenta ya como caducado"""
        manager = VaccineManager()
        expected_value = "La cita ha caducado"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/reactivate_ok_2.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-18")
    def test_cancelled_was_final(self):
        """Probamos a restaurar una cita que fue borrada de manera definitiva"""
        manager = VaccineManager()
        expected_value = "La cita se borró de manera definitiva"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/reactivate_ok_4.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-18")
    def test_2(self):
        """Deletion nodo 1"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/empty.json")
        self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-07-18")
    def test_3(self):
        """Duplication nodo 1"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_0.json")
        self.assertEqual(c_m.exception.message, expected_value)
        # No nos tiene que devolver un error, ya que el propio json y python elimina los repetidos

    @freeze_time("2022-07-18")
    def test_4(self):
        """Deletion nodo 5"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_0.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_6(self):
        """Duplication nodo 5"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/duplication_0.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_7(self):
        """Deletion nodo 3"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong signature label"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_1.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_8(self):
        """Duplication nodo 3"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_1.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_9(self):
        """Deletion nodo 11"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_2.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_10(self):
        """Duplication nodo 11"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_2.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_11(self):
        """Modification nodo 5"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/mod_0.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_12(self):
        """Modification nodo 11"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/mod_1.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_13(self):
        """Deletion nodo 6"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_3.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_14(self):
        """Duplication nodo 6"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_3.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_15(self):
        """Deletion nodo 7"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_4.json")
        self.assertEqual(c_m.exception.message, expected_value)

    # pylint: disable= Trailing whitespace
    def test_16(self):
        """Duplication nodo 7"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_4.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_17(self):
        """Deletion nodo 8"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_5.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_18(self):
        """Duplication nodo 8"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_5.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_19(self):
        """Deletion nodo 9"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_6.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_20(self):
        """Duplication nodo 9"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_6.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_21(self):
        """Deletion nodo 10"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_7.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_22(self):
        """Duplication nodo 10"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_7.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_23(self):
        """Deletion nodo 12"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_8.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_24(self):
        """Duplication nodo 12"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_8.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_25(self):
        """Deletion nodo 13"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_9.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_26(self):
        """Duplication nodo 13"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_9.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_27(self):
        """Deletion nodo 14"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_10.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_28(self):
        """Duplication nodo 14"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_10.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_29(self):
        """Deletion nodo 16"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_11.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_30(self):
        """Duplication nodo 16"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_11.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_31(self):
        """Deletion nodo 17"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_12.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_32(self):
        """Duplication nodo 17"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_12.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_33(self):
        """Deletion nodo 18"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_13.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_34(self):
        """Duplication nodo 18"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_13.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_35(self):
        """Deletion nodo 20"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_14.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_36(self):
        """Duplication nodo 20"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_14.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_37(self):
        """Deletion nodo 21"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_15.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_38(self):
        """Duplication nodo 21"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_15.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_39(self):
        """Deletion nodo 22"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_16.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_40(self):
        """Duplication nodo 22"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_16.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_41(self):
        """Deletion nodo 23"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_17.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_42(self):
        """Duplication nodo 23"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_17.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_43(self):
        """Deletion nodo 24"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong signature label"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_18.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_44(self):
        """Duplication nodo 24"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong signature label"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_18.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_45(self):
        """Deletion nodo 25"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_19.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_46(self):
        """Duplication nodo 25"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_19.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_47(self):
        """Modification nodo 24"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong signature label"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/mod_2.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_48(self):
        """Deletion nodo 27"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_20.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_49(self):
        """Duplication nodo 27"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_20.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_50(self):
        """Deletion nodo 28"""
        manager = VaccineManager()
        expected_value = "date_signature format is not valid"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_21.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_51(self):
        """Duplication nodo 28"""
        manager = VaccineManager()
        expected_value = "date_signature format is not valid"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_21.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_52(self):
        """Modification nodo 28"""
        manager = VaccineManager()
        expected_value = "date_signature format is not valid"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/mod_3.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_53(self):
        """Deletion nodo 29"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_22.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_54(self):
        """Duplication nodo 29"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_22.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_55(self):
        """Deletion nodo 30"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_23.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_56(self):
        """Duplication nodo 30"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_23.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_57(self):
        """Deletion nodo 31"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong reactivation type label"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_24.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_58(self):
        """Duplication nodo 31"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong reactivation type label"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_24.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_59(self):
        """Modification nodo 31"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong reactivation type label"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/mod_4.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_60(self):
        """Deletion nodo 32"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_25.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_61(self):
        """Duplication nodo 32"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_25.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_62(self):
        """Deletion nodo 34"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_26.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_63(self):
        """Duplication nodo 34"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_26.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_64(self):
        """Deletion nodo 35"""
        manager = VaccineManager()
        expected_value = "Reactivation label is not valid"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_27.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_65(self):
        """Duplication nodo 35"""
        manager = VaccineManager()
        expected_value = "Reactivation label is not valid"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_27.json")

        self.assertEqual(c_m.exception.message, expected_value)

    def test_66(self):
        """Modification nodo 35"""
        manager = VaccineManager()
        expected_value = "Reactivation label is not valid"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/mod_5.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_67(self):
        """Deletion nodo 36"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_28.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_68(self):
        """Duplication nodo 36"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_28.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_69(self):
        """Deletion nodo 37"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_29.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_70(self):
        """Duplication nodo 37"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_29.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_71(self):
        """Deletion nodo 38"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong day label"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_30.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_72(self):
        """Duplication nodo 38"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong day label"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_30.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_73(self):
        """Modification nodo 38"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong day label"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/mod_6.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_74(self):
        """Deletion nodo 39"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_31.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_75(self):
        """Duplication nodo 39"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_31.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_76(self):
        """Deletion nodo 41"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_32.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_77(self):
        """Duplication nodo 41"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_32.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_78(self):
        """Deletion nodo 42"""
        manager = VaccineManager()
        expected_value = "Invalid iso date format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_33.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_79(self):
        """Duplication nodo 42"""
        manager = VaccineManager()
        expected_value = "Invalid iso date format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_33.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_80(self):
        """Deletion nodo 43"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/deletion_34.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_81(self):
        """Duplication nodo 43"""
        manager = VaccineManager()
        expected_value = "JSON Decode Error - Wrong JSON Format"
        with self.assertRaises(VaccineManagementException) as c_m:
            manager.reactivate_appointment(JSON_FILES_PATH + "/reactivate/arbol/dup_34.json")
        self.assertEqual(c_m.exception.message, expected_value)

    def test_random(self):
        """Reiniciamos archivos"""
        pass
