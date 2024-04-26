from datetime import datetime
from .json_store import JsonStore
from ..hotel_management_config import JSON_FILES_PATH
from ..hotel_management_exception import HotelManagementException


class JsonStoreCheckout(JsonStore):
    class __JsonStoreCheckout(JsonStore):
        def __init__(self):
            self._file_name = JSON_FILES_PATH + "store_check_out.json"
            self._data_list = []

        def add_item(self, item):
            self.find_item_checkout(item["room_key"])
            self._data_list.append(item)

        def save_store(self, item):
            self.load_store()

            self.add_item(item)
            super().save_store()

        def find_item_checkout(self, value):
            print(self._file_name)
            found = self.find_item("room_key", value)
            if found is not None:
                raise HotelManagementException("Guest is already out")

        @staticmethod
        def validate_date_checkout(departure_date_timestamp):
            today = datetime.utcnow().date()
            if datetime.fromtimestamp(departure_date_timestamp).date() != today:
                raise HotelManagementException("Error: today is not the departure day")

    __instance = None

    def __new__(cls):
        if not JsonStoreCheckout.__instance:
            JsonStoreCheckout.__instance = JsonStoreCheckout.__JsonStoreCheckout()
        return JsonStoreCheckout.__instance
