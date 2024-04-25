from .json_store import JsonStore
from ..hotel_management_config import JSON_FILES_PATH
from ..hotel_management_exception import HotelManagementException

class JsonStoreCheckout(JsonStore):
    def __init__(self):
        self._file_name = JSON_FILES_PATH + "store_check_out.json"
        self._data_list=[]

    def add_item(self, item):
        print(self._file_name)
        found = self.find_item("room_key", item["room_key"])
        if found is not None:
            raise HotelManagementException("Guest is already out")
        self._data_list.append(item)


