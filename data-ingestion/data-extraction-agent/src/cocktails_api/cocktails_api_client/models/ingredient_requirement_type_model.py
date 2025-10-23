from enum import Enum


class IngredientRequirementTypeModel(str, Enum):
    NONE = "none"
    OPTIONAL = "optional"
    REQUIRED = "required"

    def __str__(self) -> str:
        return str(self.value)
