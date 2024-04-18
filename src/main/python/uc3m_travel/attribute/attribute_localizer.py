from .attribute import Attribute
from ..hotel_management_exception import HotelManagementException

class Localizer(Attribute):

    def __init__(self, localizer):
        self._attr_pattern= r'(SINGLE|DOUBLE|SUITE)'
        self._error_message = "Invalid roomtype value"
        self._attr_value= self._validate(num_days)