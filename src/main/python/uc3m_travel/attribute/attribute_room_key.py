from .attribute import Attribute


class RoomKey(Attribute):

    def __init__(self, room_key):
        super().__init__()
        self._attr_pattern = r'^[a-fA-F0-9]{64}$'
        self._error_message = "Invalid room key format"
        self._attr_value = self._validate(room_key)
