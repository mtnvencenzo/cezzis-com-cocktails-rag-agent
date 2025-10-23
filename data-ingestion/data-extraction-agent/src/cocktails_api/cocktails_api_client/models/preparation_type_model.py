from enum import Enum


class PreparationTypeModel(str, Enum):
    CHILLED = "chilled"
    FRESHLYGRATED = "freshlyGrated"
    FRESHLYSQUEEZED = "freshlySqueezed"
    FRESHPRESSED = "freshPressed"
    NONE = "none"
    PEELEDANDJUICED = "peeledAndJuiced"
    QUARTERED = "quartered"

    def __str__(self) -> str:
        return str(self.value)
