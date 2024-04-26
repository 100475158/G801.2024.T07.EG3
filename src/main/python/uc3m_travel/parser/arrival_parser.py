from ..hotel_management_exception import HotelManagementException
import json
from .json_parser import JsonParser

class ArrivalParser(JsonParser):
    _JSON_KEYS = ["Localizer","IdCard"]
    _ERROR_MESSAGES = "Error - Invalid Key in JSON"
    _json_content = None
