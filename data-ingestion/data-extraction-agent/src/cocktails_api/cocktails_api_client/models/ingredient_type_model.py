from enum import Enum


class IngredientTypeModel(str, Enum):
    BEER = "beer"
    BITTERS = "bitters"
    CHAMPAGNE = "champagne"
    DILUTION = "dilution"
    FLOWERS = "flowers"
    FRUIT = "fruit"
    HERB = "herb"
    JUICE = "juice"
    LIQUEUR = "liqueur"
    PROTEIN = "protein"
    SAUCE = "sauce"
    SPIRIT = "spirit"
    SYRUP = "syrup"
    VEGETABLE = "vegetable"
    WINE = "wine"

    def __str__(self) -> str:
        return str(self.value)
