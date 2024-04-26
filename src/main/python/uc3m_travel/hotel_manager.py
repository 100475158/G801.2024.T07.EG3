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
from .storage.reservation_json_store import ReservationJsonStore
from .storage.json_store import JsonStore
from .storage.checkout_json_store import JsonStoreCheckout
from .storage.stay_json_store import JsonStoreCheckin
class HotelManager:
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""
        def __init__(self):
            pass
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
            reservation_store = ReservationJsonStore()
            reservation_store.add_item(my_reservation)
            reservation_store.save_store()

            return my_reservation.localizer


        def guest_arrival(self, file_input:str)->str:
            """manages the arrival of a guest with a reservation"""
            my_checkin = HotelStay.create_guest_arrival_from_file(file_input)

            #Ahora lo guardo en el almacen nuevo de checkin
            # escribo el fichero Json con todos los datos

            my_store_checkin= JsonStoreCheckin()

            # leo los datos del fichero si existe , y si no existe creo una lista vacia
            my_store_checkin.load_store()

            # comprobar que no he hecho otro ckeckin antes
            item = my_store_checkin.find_item("_HotelStay__room_key", my_checkin.room_key)
            if item != None:
                raise HotelManagementException ("ckeckin  ya realizado")

            #añado los datos de mi reserva a la lista , a lo que hubiera
            my_store_checkin.add_item(my_checkin)

            my_store_checkin.save_store()

            return my_checkin.room_key



        def guest_checkout(self, room_key:str)->bool:
            """manages the checkout of a guest"""
            room_key= RoomKey(room_key).value
            #check thawt the roomkey is stored in the checkins file
            file_store = JSON_FILES_PATH + "store_check_in.json"
            #Mirar si es igual al read que ya hay y si no lo extraemos a la clase hija

            checkout1 = JsonStoreCheckout()
            room_key_list = checkout1.read_input_file(file_store, "Error: store checkin not found")

            # comprobar que esa room_key es la que me han dado
            #cuando creemos find checkin de la f2 podremos extraerlo
            checkin1 = JsonStoreCheckin()
            departure_date_timestamp = checkin1.validate_room_key(room_key, room_key_list)

            today = datetime.utcnow().date()
            if datetime.fromtimestamp(departure_date_timestamp).date() != today:
                raise HotelManagementException("Error: today is not the departure day")

            my_checkout= JsonStoreCheckout()
            room_key_list=my_checkout.load_store()

            my_checkout.find_item_checkout(room_key)


            room_checkout = {"room_key": room_key, "checkout_time": datetime.timestamp(datetime.utcnow())}

            room_key_list.append(room_checkout)

            my_checkout.save_store()

            return True

            """file_store_checkout = JSON_FILES_PATH + "store_check_out.json"
            room_key_list = self.read_file(file_store_checkout)

            for checkout in room_key_list:
                if checkout["room_key"] == room_key:
                    raise HotelManagementException("Guest is already out")

            room_checkout = {"room_key":  room_key, "checkout_time":datetime.timestamp(datetime.utcnow())}


            my_co = JsonStoreCheckout()
            my_co.load_store()
            my_co.add_item(room_checkout)
            my_co.save_store()"""



    __instance = None
    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance= HotelManager.__HotelManager()
        return HotelManager.__instance