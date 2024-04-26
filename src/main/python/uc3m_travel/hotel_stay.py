""" Class HotelStay (GE2.2) """
from datetime import datetime
import hashlib
from .attribute.attribute_id_card import IdCard
from .attribute.attribute_localizer import Localizer
from .hotel_management_exception import HotelManagementException
from .hotel_reservation import HotelReservation
from .parser.arrival_parser import ArrivalParser


class HotelStay:
    """Class for representing hotel stays"""

    def __init__(self,
                 idcard: str,
                 localizer: str,
                 numdays: int,
                 roomtype: str):
        """constructor for HotelStay objects"""
        self.__alg = "SHA-256"
        self.__idcard = IdCard(idcard).value
        self.__localizer = Localizer(localizer).value
        self.__type = roomtype
        justnow = datetime.utcnow()
        self.__arrival = datetime.timestamp(justnow)
        # timestamp is represented in seconds.milliseconds
        # to add the number of days we must express num_days in seconds
        self.__departure = self.__arrival + (numdays * 24 * 60 * 60)
        self.__room_key = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string(self):
        """Composes the string to be used for generating the key for the room"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",localizer:" + \
            self.__localizer + ",arrival:" + str(self.__arrival) + \
            ",departure:" + str(self.__departure) + "}"

    @property
    def id_card(self):
        """Property that represents the product_id of the patient"""
        return self.__idcard

    @id_card.setter
    def id_card(self, value):
        self.__idcard = value

    @property
    def localizer(self):
        """Property that represents the order_id"""
        return self.__localizer

    @localizer.setter
    def localizer(self, value):
        self.__localizer = value

    @property
    def arrival(self):
        """Property that represents the phone number of the client"""
        return self.__arrival

    @property
    def room_key(self):
        """Returns the sha256 signature of the date"""
        return self.__room_key

    @property
    def departure(self):
        """Returns the issued at value"""
        return self.__departure

    @departure.setter
    def departure(self, value):
        """returns the value of the departure date"""
        self.__departure = value

    @staticmethod
    def create_guest_arrival_from_file(file_input):
        arrival_create = ArrivalParser(file_input)
        my_id_card = arrival_create.json_content["IdCard"]
        my_localizer = arrival_create.json_content["Localizer"]
        new_reservation = HotelReservation.create_reservation_from_arrival(my_id_card, my_localizer)

        reservation_format = "%d/%m/%Y"
        date_obj = datetime.strptime(new_reservation.arrival, reservation_format)
        if date_obj.date() != datetime.date(datetime.utcnow()):
            raise HotelManagementException("Error: today is not reservation date")

        my_checkin = HotelStay(idcard=my_id_card, numdays=int(new_reservation.num_days),
                               localizer=my_localizer, roomtype=new_reservation.room_type)
        return my_checkin
