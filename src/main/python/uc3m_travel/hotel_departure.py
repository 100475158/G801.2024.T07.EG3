from datetime import datetime
from uc3m_travel.hotel_management_exception import HotelManagementException

class HotelDeparture:
    def __init__(self,room_key):
        self.__roomkey = room_key
        self.__checkout_time = datetime.timestamp(datetime.utcnow())
        self.is_today_departure()

    def is_today_departure(self, departure_date_timestamp):
        today= datetime.utcnow().date()
        if datetime.fromtimestamp(departure_date_timestamp).date() !=today:
            raise HotelManagementException("Error:today is not the departure day")
