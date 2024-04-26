from .json_store import JsonStore
from ..hotel_management_config import JSON_FILES_PATH
from ..hotel_management_exception import HotelManagementException


class JsonStoreCheckin(JsonStore):
    class __JsonStoreCheckin(JsonStore):
        def __init__(self):
            self._file_name = JSON_FILES_PATH + "store_check_in.json"
            self._data_list = []

        def save_store(self, item):
            found = self.find_item("_HotelStay__room_key", item.room_key)
            self.checkin_exists(found)
            self.add_item(item)
            super().save_store()

        @staticmethod
        def validate_room_key(room_key, room_key_list):
            found = False
            for item in room_key_list:
                if room_key == item["_HotelStay__room_key"]:
                    departure_date_timestamp: object = item["_HotelStay__departure"]
                    found = True
            if not found:
                raise HotelManagementException("Error: room key not found")
            return departure_date_timestamp

        @staticmethod
        def checkin_exists(item):
            if item is not None:
                raise HotelManagementException("ckeckin  ya realizado")

    __instance = None

    def __new__(cls):
        if not JsonStoreCheckin.__instance:
            JsonStoreCheckin.__instance = JsonStoreCheckin.__JsonStoreCheckin()
        return JsonStoreCheckin.__instance
