from .attribute import Attribute


class Localizer(Attribute):

    def __init__(self, localizer):
        super().__init__()
        self._attr_pattern = r'^[a-fA-F0-9]{32}$'
        self._error_message = "Invalid localizer"
        self._attr_value = self._validate(localizer)
