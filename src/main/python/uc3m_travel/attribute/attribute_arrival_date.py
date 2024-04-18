from .attribute import Attribute
from ..hotel_management_exception import HotelManagementException

class ArrivalDate(Attribute):

    def __init__(self, arrival_date):
        self._attr_pattern= r'^(([0-2]\d|-3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$'
        self._error_message = "Invalid date format"
        self._attr_value= self._validate(arrival_date)