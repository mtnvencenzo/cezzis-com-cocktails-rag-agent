from enum import Enum


class GlasswareTypeModel(str, Enum):
    COCKTAILGLASS = "cocktailGlass"
    COLLINS = "collins"
    COPPERMUG = "copperMug"
    COUPE = "coupe"
    DOUBLEROCKS = "doubleRocks"
    FIZZ = "fizz"
    FLUTE = "flute"
    HIGHBALL = "highball"
    HOLLOWEDPINEAPPLE = "hollowedPineapple"
    HURRICANE = "hurricane"
    JULEPTIN = "julepTin"
    LOWBALL = "lowball"
    NONE = "none"
    PINTGLASS = "pintGlass"
    ROCKS = "rocks"
    SCORPIONBOWL = "scorpionBowl"
    SHOTGLASS = "shotGlass"
    SNIFTER = "snifter"
    TIKIMUG = "tikiMug"
    WINEGLASS = "wineGlass"

    def __str__(self) -> str:
        return str(self.value)
