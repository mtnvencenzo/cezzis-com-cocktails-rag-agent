from enum import Enum


class CocktailDataIncludeModel(str, Enum):
    DESCRIPTIVETITLE = "descriptiveTitle"
    MAINIMAGES = "mainImages"
    SEARCHTILES = "searchTiles"

    def __str__(self) -> str:
        return str(self.value)
