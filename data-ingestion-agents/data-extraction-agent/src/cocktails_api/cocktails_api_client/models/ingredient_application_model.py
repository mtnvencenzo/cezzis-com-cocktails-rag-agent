from enum import Enum


class IngredientApplicationModel(str, Enum):
    ADDITIONAL = "additional"
    BASE = "base"
    GARNISHMENT = "garnishment"
    MUDDLE = "muddle"

    def __str__(self) -> str:
        return str(self.value)
