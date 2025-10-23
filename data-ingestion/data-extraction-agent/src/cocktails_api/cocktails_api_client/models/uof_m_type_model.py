from enum import Enum


class UofMTypeModel(str, Enum):
    BARSPOON = "barspoon"
    CUPS = "cups"
    DASHES = "dashes"
    DISCRETION = "discretion"
    ITEM = "item"
    NONE = "none"
    OUNCES = "ounces"
    SPLASH = "splash"
    TABLESPOON = "tablespoon"
    TEASPOON = "teaspoon"
    TOPOFF = "topoff"
    TOTASTE = "toTaste"

    def __str__(self) -> str:
        return str(self.value)
