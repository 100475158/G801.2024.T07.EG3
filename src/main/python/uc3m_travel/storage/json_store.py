import hashlib
from ..hotel_management_exception import HotelManagementException
import json
from ..hotel_management_config import JSON_FILES_PATH

class JsonStore():


    def __init__(self, file_name):
        self._file_name =file_name
        self._data_list=[]
        self.load_store()


    def save_store(self):
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise HotelManagementException("Wrong file  or file path") from exception


    def add_item(self, item):
        self._data_list.append(item.__dict__)

    def find_item(self, key, value):
        for item in self._data_list:
            if value == item[key]:
                print("found", item)
                return item
        return None
    def load_store(self):
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return self._data_list


    def read_input_file(self, file_input, error):
        try:
            with open(file_input, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as exception:
            raise HotelManagementException(error) from exception
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






