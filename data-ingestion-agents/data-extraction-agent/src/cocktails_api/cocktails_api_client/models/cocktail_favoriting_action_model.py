from enum import Enum


class CocktailFavoritingActionModel(str, Enum):
    ADD = "add"
    REMOVE = "remove"

    def __str__(self) -> str:
        return str(self.value)
