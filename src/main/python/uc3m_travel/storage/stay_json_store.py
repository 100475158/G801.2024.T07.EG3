import json

from .json_store import JsonStore
from ..hotel_management_config import JSON_FILES_PATH
from ..hotel_management_exception import HotelManagementException

class JsonStoreCheckin(JsonStore):
    def __init__(self):
        self._file_name = JSON_FILES_PATH + "store_check_in.json"
        self._data_list=[]

    def validate_room_key(self, room_key, room_key_list):
        found = False
        for item in room_key_list:
            if room_key == item["_HotelStay__room_key"]:
                departure_date_timestamp = item["_HotelStay__departure"]
                found = True
        if not found:
            raise HotelManagementException("Error: room key not found")
        return departure_date_timestamp

    def checkin_exists(self, item):
        if item != None:
            raise HotelManagementException("ckeckin  ya realizado")