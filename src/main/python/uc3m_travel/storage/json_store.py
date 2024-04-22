import hashlib
from ..hotel_management_exception import HotelManagementException

class JsonStore():

    def __init__(self):

    def save_list_to_file(self):

    def load_list_from_file(self):

    def add_item(self, item):

    def find_item(self, key, value):
        self.load_list_from_file()
        for item in self._data_list:
            if item[key] == value:
                return item
        return None
    @property
    def hash(self):
        self.load_store()
        return hashlib.md5(self.__str__().encode()).hexdigest()

