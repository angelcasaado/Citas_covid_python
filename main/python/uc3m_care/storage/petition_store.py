"""Clase petition store"""
from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH


class PetitionStore:
    """Implmentation of the singleton pattern"""
    #pylint: disable=invalid-name # noqa
    class __PetitionStore(JsonStore):
        """Subclass of JsonStore for managing the VaccinationLog"""
        _FILE_PATH = JSON_FILES_PATH + "store_petition.json"
        _ID_FIELD = "_VaccinationReactivate__date_signature"

    instance = None

    def __new__(cls):
        if not PetitionStore.instance:
            PetitionStore.instance = PetitionStore.__PetitionStore()
        return PetitionStore.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
