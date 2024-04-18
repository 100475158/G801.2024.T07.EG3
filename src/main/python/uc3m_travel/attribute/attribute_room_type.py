from .attribute import Attribute
from ..hotel_management_exception import HotelManagementException

class RoomType(Attribute):

    def __init__(self, room_type):
        self._attr_pattern= r'(SINGLE|DOUBLE|SUITE)'
        self._error_message = "Invalid roomtype value"
        self._attr_value= self._validate(room_type)