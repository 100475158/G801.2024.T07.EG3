from .attribute import Attribute
from ..hotel_management_exception import HotelManagementException

class Localizer(Attribute):

    def __init__(self, localizer):
        self._attr_pattern= r'^[a-fA-F0-9]{32}$'
        self._error_message = "Invalid localizer"
        self._attr_value= self._validate(localizer)