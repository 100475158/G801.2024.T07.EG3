"""Module for the hotel manager"""
from datetime import datetime
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from .attribute.attribute_room_key import RoomKey
from .storage.reservation_json_store import ReservationJsonStore
from .storage.checkout_json_store import JsonStoreCheckout
from .storage.stay_json_store import JsonStoreCheckin


class HotelManager:
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""

        def __init__(self):
            pass

        @staticmethod
        def room_reservation(credit_card: str,
                             name_surname: str,
                             id_card: str,
                             phone_number: str,
                             room_type: str,
                             arrival_date: str,
                             num_days: int) -> str:
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

        @staticmethod
        def guest_arrival(file_input: str) -> str:
            """manages the arrival of a guest with a reservation"""
            my_checkin = HotelStay.create_guest_arrival_from_file(file_input)
            my_store_checkin = JsonStoreCheckin()
            my_store_checkin.load_store()
            my_store_checkin.save_store(my_checkin)

            return my_checkin.room_key

        @staticmethod
        def guest_checkout(room_key: str) -> bool:
            """manages the checkout of a guest"""
            room_key = RoomKey(room_key).value
            file_store = JSON_FILES_PATH + "store_check_in.json"
            my_checkout = JsonStoreCheckout()
            room_key_list_1 = my_checkout.read_input_file(file_store, "Error: store checkin not found")
            # comprobar que esa room_key es la que me han dado
            # cuando creemos find checkin de la f2 podremos extraerlo
            checkin1 = JsonStoreCheckin()
            departure_date_timestamp = checkin1.validate_room_key(room_key, room_key_list_1)

            my_checkout.validate_date_checkout(departure_date_timestamp)

            room_checkout = {"room_key": room_key, "checkout_time": datetime.timestamp(datetime.utcnow())}
            my_checkout.save_store(room_checkout)

            return True

    __instance = None

    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance
