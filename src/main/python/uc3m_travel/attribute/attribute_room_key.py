from .attribute import Attribute
from ..hotel_management_exception import HotelManagementException

class RoomKey(Attribute):

    def __init__(self, room_key):
        self._attr_pattern= r'^[a-fA-F0-9]{64}$'
        self._error_message = "Invalid room key format"
        self._attr_value= self._validate(room_key)