import re
from ..hotel_management_exception import HotelManagementException


class Attribute:
    """Parent class for attributes..."""

    def __init__(self):
        """"Constructor for attributes..."""
        self._attr_pattern = r""
        self._error_message = ""
        self._attr_value = ""

    def _validate(self, attr_value):
        coincide = re.compile(self._attr_pattern)
        regex_matches = coincide.fullmatch(attr_value)
        if not regex_matches:
            raise HotelManagementException(self._error_message)
        return attr_value

    @property
    def value(self):
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = self._validate(attr_value)
