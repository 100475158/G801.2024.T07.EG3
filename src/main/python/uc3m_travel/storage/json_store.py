import hashlib
from ..hotel_management_exception import HotelManagementException
import json
from ..hotel_management_config import JSON_FILES_PATH

class JsonStore():
    __file_name= ""
    __data_list=[]

    def __init__(self, file_name):
        self.__file_name =file_name
        self.__data_list=[]
        self.load_store()


    def save_store(self):
        try:
            with open(self.__file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self.__data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise HotelManagementException("Wrong file  or file path") from exception


    def add_item(self, item):
        self.__data_list.append(item.__dict__)

    def find_item(self, key, value):
        for item in self.__data_list:
            if value == item[key]:
                return item
        return None
    def load_store(self):
        try:
            with open(self.__file_name, "r", encoding="utf-8", newline="") as file:
                self.__data_list = json.load(file)
        except FileNotFoundError:
            self.__data_list = []
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception

