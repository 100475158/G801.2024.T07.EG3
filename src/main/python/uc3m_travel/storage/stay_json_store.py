import json

from .json_store import JsonStore
from ..hotel_management_config import JSON_FILES_PATH
from ..hotel_management_exception import HotelManagementException

class JsonStoreCheckin(JsonStore):
    def __init__(self):
        self._file_name = JSON_FILES_PATH + "store_check_in.json"
        self._data_list=[]


