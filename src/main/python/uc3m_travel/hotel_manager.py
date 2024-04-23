"""Module for the hotel manager"""
import re
import json
from datetime import datetime

from uc3m_travel.attribute.attribute_credit_card import CreditCard
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from freezegun import freeze_time
from .attribute.attribute_id_card import IdCard
from .attribute.attribute_localizer import Localizer
from .attribute.attribute_room_key import RoomKey
"""from .attribute.json_store import JsonStore"""

class HotelManager:
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""
        def __init__(self):
            pass



        def read_data_from_json(self, file):
            """reads the content of a json file with two fields: CreditCard and phoneNumber"""
            try:
                with open(file, encoding='utf-8') as json_file:
                    json_data = json.load(json_file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Wrong file or file path") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
            try:
                credit_card = json_data["CreditCard"]
                phone_number = json_data["phoneNumber"]
                reservation = HotelReservation(id_card="12345678Z",
                                       credit_card_number=credit_card,
                                       name_surname="John Doe",
                                       phone_number=phone_number,
                                       room_type="single",
                                       num_days=3,
                                       arrival="20/01/2024")
            except KeyError as exception:
                raise HotelManagementException("JSON Decode Error - Invalid JSON Key") from exception
            if not CreditCard(credit_card):
                raise HotelManagementException("Invalid credit card number")
            # Close the file
            return reservation

        # pylint: disable=too-many-arguments
        def room_reservation(self,
                             credit_card:str,
                             name_surname:str,
                             id_card:str,
                             phone_number:str,
                             room_type:str,
                             arrival_date: str,
                             num_days:int)->str:
            """manges the hotel reservation: creates a reservation and saves it into a json file"""



            my_reservation = HotelReservation(id_card=id_card,
                                              credit_card_number=credit_card,
                                              name_surname=name_surname,
                                              phone_number=phone_number,
                                              room_type=room_type,
                                              arrival=arrival_date,
                                              num_days=num_days)
            """reservation_store= JsonStore()
            # escribo el fichero Json con todos los datos
            reservation_store.save_reservation(my_reservation)"""
            file_store = JSON_FILES_PATH + "store_reservation.json"

            #leo los datos del fichero si existe , y si no existe creo una lista vacia
            data_list = self.load_store(file_store)

            #compruebo que esta reserva no esta en la lista
            self.find_item(data_list, my_reservation)
            #añado los datos de mi reserva a la lista , a lo que hubiera
            data_list.append(my_reservation.__dict__)

            #escribo la lista en el fichero
            self.save_store(data_list, file_store)

            return my_reservation.localizer

        def save_store(self, data_list, file_store):
            try:
                with open(file_store, "w", encoding="utf-8", newline="") as file:
                    json.dump(data_list, file, indent=2)
            except FileNotFoundError as exception:
                raise HotelManagementException("Wrong file  or file path") from exception

        def find_item(self, data_list, my_reservation):
            for item in data_list:
                if my_reservation.localizer == item["_HotelReservation__localizer"]:
                    raise HotelManagementException("Reservation already exists")
                if my_reservation.id_card == item["_HotelReservation__id_card"]:
                    raise HotelManagementException("This ID card has another reservation")

        def load_store(self, file_store):
            try:
                with open(file_store, "r", encoding="utf-8", newline="") as file:
                    data_list = json.load(file)
            except FileNotFoundError:
                data_list = []
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
            return data_list

        def guest_arrival(self, file_input:str)->str:
            """manages the arrival of a guest with a reservation"""
            my_checkin = self.create_guest_arrival_from_file(file_input)

            #Ahora lo guardo en el almacen nuevo de checkin
            # escribo el fichero Json con todos los datos
            file_store = JSON_FILES_PATH + "store_check_in.json"

            # leo los datos del fichero si existe , y si no existe creo una lista vacia
            try:
                with open(file_store, "r", encoding="utf-8", newline="") as file:
                    room_key_list = json.load(file)
            except FileNotFoundError as exception:
                room_key_list = []
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception

            # comprobar que no he hecho otro ckeckin antes
            for item in room_key_list:
                if my_checkin.room_key == item["_HotelStay__room_key"]:
                    raise HotelManagementException ("ckeckin  ya realizado")

            #añado los datos de mi reserva a la lista , a lo que hubiera
            room_key_list.append(my_checkin.__dict__)

            self.save_store(room_key_list, file_store)

            return my_checkin.room_key

        def create_guest_arrival_from_file(self, file_input):
            input_list = self.read_input_file(file_input)
            # comprobar valores del fichero
            my_id_card, my_localizer = self.read_input_data_from_file(input_list)
            new_reservation = HotelReservation.create_reservation_from_arrival(my_id_card, my_localizer)
            # compruebo si hoy es la fecha de checkin
            reservation_format = "%d/%m/%Y"
            date_obj = datetime.strptime(new_reservation.arrival, reservation_format)
            if date_obj.date() != datetime.date(datetime.utcnow()):
                raise HotelManagementException("Error: today is not reservation date")
            # genero la room key para ello llamo a Hotel Stay
            my_checkin = HotelStay(idcard=my_id_card, numdays=int(new_reservation.num_days),
                                   localizer=my_localizer, roomtype=new_reservation.room_type)
            return my_checkin

        def create_reservation_from_arrival(self, my_id_card, my_localizer):
            IdCard(my_id_card)
            Localizer(my_localizer)
            # self.validate_localizer() hay que validar"""
            # buscar en almacen
            store_list = self.load_reservation_store()
            # compruebo si esa reserva esta en el almacen
            new_reserva = self.find_reservation(
                my_localizer, store_list)
            if my_id_card != new_reserva["_HotelReservation__id_card"]:
                raise HotelManagementException("Error: Localizer is not correct for this IdCard")
            # regenerar clave y ver si coincide
            reservation_date = datetime.fromtimestamp(new_reserva["_HotelReservation__reservation_date"])
            with freeze_time(reservation_date):
                new_reservation = HotelReservation(
                    credit_card_number=new_reserva["_HotelReservation__credit_card_number"],
                    id_card=new_reserva["_HotelReservation__id_card"],
                    num_days=new_reserva["_HotelReservation__num_days"],
                    room_type=new_reserva["_HotelReservation__room_type"],
                    arrival=new_reserva["_HotelReservation__arrival"],
                    name_surname=new_reserva["_HotelReservation__name_surname"],
                    phone_number=new_reserva["_HotelReservation__phone_number"])
            if new_reservation.localizer != my_localizer:
                raise HotelManagementException("Error: reservation has been manipulated")
            return new_reservation

        def find_reservation(self, my_localizer, store_list):
            for item in store_list:
                if my_localizer == item["_HotelReservation__localizer"]:
                    return item
            raise HotelManagementException("Error: localizer not found")

        def load_reservation_store(self):
            file_store = JSON_FILES_PATH + "store_reservation.json"
            # leo los datos del fichero , si no existe deber dar error porque el almacen de reservaa
            # debe existir para hacer el checkin
            try:
                with open(file_store, "r", encoding="utf-8", newline="") as file:
                    store_list = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Error: store reservation not found") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
            return store_list

        def read_input_data_from_file(self, input_list):
            try:
                my_localizer = input_list["Localizer"]
                my_id_card = input_list["IdCard"]
            except KeyError as exception:
                raise HotelManagementException("Error - Invalid Key in JSON") from exception
            return my_id_card, my_localizer

        def read_input_file(self, file_input):
            try:
                with open(file_input, "r", encoding="utf-8", newline="") as file:
                    input_list = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Error: file input not found") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
            return input_list

        def guest_checkout(self, room_key:str)->bool:
            """manages the checkout of a guest"""
            RoomKey(room_key)
            """self.validate_roomkey(room_key)"""
            #check thawt the roomkey is stored in the checkins file
            file_store = JSON_FILES_PATH + "store_check_in.json"
            try:
                with open(file_store, "r", encoding="utf-8", newline="") as file:
                    room_key_list = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Error: store checkin not found") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception

            # comprobar que esa room_key es la que me han dado
            found = False
            for item in room_key_list:
                if room_key == item["_HotelStay__room_key"]:
                    departure_date_timestamp = item["_HotelStay__departure"]
                    found = True
            if not found:
                raise HotelManagementException ("Error: room key not found")

            today = datetime.utcnow().date()
            if datetime.fromtimestamp(departure_date_timestamp).date() != today:
                raise HotelManagementException("Error: today is not the departure day")

            file_store_checkout = JSON_FILES_PATH + "store_check_out.json"
            try:
                with open(file_store_checkout, "r", encoding="utf-8", newline="") as file:
                    room_key_list = json.load(file)
            except FileNotFoundError as exception:
                room_key_list = []
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception

            for checkout in room_key_list:
                if checkout["room_key"] == room_key:
                    raise HotelManagementException("Guest is already out")

            room_checkout={"room_key":  room_key, "checkout_time":datetime.timestamp(datetime.utcnow())}

            room_key_list.append(room_checkout)

            self.save_store(room_key_list, file_store_checkout)

            return True


    __instance = None
    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance= HotelManager.__HotelManager()
        return HotelManager.__instance
