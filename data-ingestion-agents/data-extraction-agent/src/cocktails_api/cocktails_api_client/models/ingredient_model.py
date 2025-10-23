from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ingredient_application_model import IngredientApplicationModel
from ..models.ingredient_requirement_type_model import IngredientRequirementTypeModel
from ..models.ingredient_type_model import IngredientTypeModel
from ..models.preparation_type_model import PreparationTypeModel
from ..models.uof_m_type_model import UofMTypeModel

T = TypeVar("T", bound="IngredientModel")


@_attrs_define
class IngredientModel:
    name: str
    """ The name of the ingredient """
    uo_m: UofMTypeModel
    """ The unit of measure when using this ingredient in a cocktail recipe """
    requirement: IngredientRequirementTypeModel
    """ Whether or not this ingredient is required ('Required' or 'Optional') """
    display: str
    """ Gets the complete display value for the ingredient including units and measurments """
    units: float
    """ The number of units to use in relation to the UoM (unit of measure) in the cocktail recipe """
    preparation: PreparationTypeModel
    """ Any preparation that should be made with this ingredient """
    suggestions: str
    """ Suggestion when using this ingredient """
    types: list[IngredientTypeModel]
    """ The ingredient types that this ingredient is in relation to the cocktail recipe """
    applications: list[IngredientApplicationModel]
    """ The ingredient applications that this ingredient is in relation to the cocktail recipe """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        uo_m = self.uo_m.value

        requirement = self.requirement.value

        display = self.display

        units = self.units

        preparation = self.preparation.value

        suggestions = self.suggestions

        types = []
        for types_item_data in self.types:
            types_item = types_item_data.value
            types.append(types_item)

        applications = []
        for applications_item_data in self.applications:
            applications_item = applications_item_data.value
            applications.append(applications_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "uoM": uo_m,
                "requirement": requirement,
                "display": display,
                "units": units,
                "preparation": preparation,
                "suggestions": suggestions,
                "types": types,
                "applications": applications,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        uo_m = UofMTypeModel(d.pop("uoM"))

        requirement = IngredientRequirementTypeModel(d.pop("requirement"))

        display = d.pop("display")

        units = d.pop("units")

        preparation = PreparationTypeModel(d.pop("preparation"))

        suggestions = d.pop("suggestions")

        types = []
        _types = d.pop("types")
        for types_item_data in _types:
            types_item = IngredientTypeModel(types_item_data)

            types.append(types_item)

        applications = []
        _applications = d.pop("applications")
        for applications_item_data in _applications:
            applications_item = IngredientApplicationModel(applications_item_data)

            applications.append(applications_item)

        ingredient_model = cls(
            name=name,
            uo_m=uo_m,
            requirement=requirement,
            display=display,
            units=units,
            preparation=preparation,
            suggestions=suggestions,
            types=types,
            applications=applications,
        )

        ingredient_model.additional_properties = d
        return ingredient_model

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
