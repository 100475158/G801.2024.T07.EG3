import hashlib
import json

from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException



class JsonStore:

    _data_list = []
    _file_name = ""
    def __init__(self):
        pass

    def save_reservation(self, my_reservation):
        file_store = JSON_FILES_PATH + "store_reservation.json"
        # leo los datos del fichero si existe , y si no existe creo una lista vacia
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        # compruebo que esta reserva no esta en la lista
        for item in data_list:
            if my_reservation.localizer == item["_HotelReservation__localizer"]:
                raise HotelManagementException("Reservation already exists")
        if my_reservation.id_card == item["_HotelReservation__id_card"]:
            raise HotelManagementException("This ID card has another reservation")
        # añado los datos de mi resena a 1a listan lo que hubiera data_list-append(my_reservation._-dict__)
        # escribo la lista en el fichero
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file or file path") from ex

    def save_checkin(self, checkin_data):
        file_store = JSON_FILES_PATH + "store_check_in.json"
        try:
            with open(file_store, "r", encoding="utf-8") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

        for item in data_list:
            if checkin_data['localizer'] == item['localizer']:
                raise HotelManagementException("Check-in already exists")

        data_list.append(checkin_data)

        try:
            with open(file_store, "w", encoding="utf-8") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file or file path") from ex

    def save_checkout(self, checkout_data):
        file_store = JSON_FILES_PATH + "store_check_out.json"
        try:
            with open(file_store, "r", encoding="utf-8") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # Aquí también podrías comprobar si ya existe una salida con la misma room_key
        for item in data_list:
            if checkout_data['room_key'] == item['room_key']:
                raise HotelManagementException("Checkout already exists")

        data_list.append(checkout_data)

        try:
            with open(file_store, "w", encoding="utf-8") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file or file path") from ex

    def add_item(self, item):
        ...

    def save_list_to_file(self):
        ...

    def load_list_from_file(self):
        ...

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

    def load_store(self):
        ...