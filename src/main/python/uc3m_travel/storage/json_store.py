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
                print("found", item)
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

    def read_input_file(self, file_input):
        try:
            with open(file_input, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as exception:
            raise HotelManagementException("Error: file input not found") from exception
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return input_list

    def read_input_data_from_file(self, input_list):
        try:
            my_localizer = input_list["Localizer"]
            my_id_card = input_list["IdCard"]
        except KeyError as exception:
            raise HotelManagementException("Error - Invalid Key in JSON") from exception
        return my_id_card, my_localizer

    def find_reservation(self, my_localizer, store_list):
        for item in store_list:
            if my_localizer == item["_HotelReservation__localizer"]:
                return item
        raise HotelManagementException("Error: localizer not found")
class JsonParser():
    """Subclase de JsonStore"""
    _JSON_KEYS = []
    _ERROR_MESSAGES = "JSON Decode Error - Wrong JSON Format"
    _json_content = None

    def __init__(self, imput_file):
        self._input_file = imput_file
        self._json_content = self.load_json_content()
        self.validate_json_keys()

