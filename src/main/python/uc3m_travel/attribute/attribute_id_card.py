from .attribute import Attribute
from ..hotel_management_exception import HotelManagementException


class IdCard(Attribute):

    def __init__(self, id_card):
        super().__init__()
        self._attr_pattern = r'^[0-9]{8}[A-Z]{1}$'
        self._error_message = "Invalid IdCard format"
        self._attr_value = self._validate(id_card)

    def _validate(self, id_card):
        super()._validate(id_card)
        letters_verification = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
                                "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
                                "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
                                "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        numbers_dni = int(id_card[0:8])
        dni_module = str(numbers_dni % 23)
        if id_card[8] != letters_verification[dni_module]:
            raise HotelManagementException("Invalid IdCard letter")
        return id_card
