from .attribute import Attribute
from ..hotel_management_exception import HotelManagementException


class NumDays(Attribute):

    def __init__(self, attr_value):
        self._attr_pattern = r""
        self._error_message = ""
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        try:
            days = int(attr_value)
        except ValueError as exception:
            raise HotelManagementException("Invalid num_days datatype") from exception
        if days < 1 or days > 10:
            raise HotelManagementException("Numdays should be in the range 1-10")
        return attr_value
