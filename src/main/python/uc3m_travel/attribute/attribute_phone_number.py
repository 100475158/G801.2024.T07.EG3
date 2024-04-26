from .attribute import Attribute


class PhoneNumber(Attribute):

    def __init__(self, phone_number):
        self._attr_pattern = r'^(\+)[0-9]{9}'
        self._error_message = "Invalid phone number format"
        self._attr_value = self._validate(phone_number)
